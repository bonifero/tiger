import configparser
import itertools
import json
import os
import tempfile
from pathlib import Path
from model import Problem, number

SIGNS={-2:'<',-1:'<=',0:'=',1:'>=',2:'>'}

def as_dict(p):
    return dict(version=1,name=p.name,c=list(map(str,p.c)),A=[list(map(str,r)) for r in p.A],b=list(map(str,p.b)),signs=p.signs,sense=p.sense,variable_names=p.names)

def from_dict(d):
    return Problem(d['c'],d['A'],d['b'],d['signs'],d.get('sense','max'),d.get('name','Задача'),tuple(d.get('variable_names',())))

def load(path):
    path=Path(path)
    if path.suffix.lower()!='.ini':return from_dict(json.loads(path.read_text(encoding='utf-8-sig')))
    conf=configparser.ConfigParser(interpolation=None)
    try:text=path.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:text=path.read_text(encoding='cp1251')
    conf.read_string(text)
    get=lambda s,k,f:conf.get(s,k,fallback=str(f))
    n=int(get('Task parameters','Variables',1));m=int(get('Task parameters','Conditions',1))
    if not 1<=n<=100 or not 1<=m<=200:raise ValueError('Недопустимые размеры INI.')
    count=int(get('Variable index','Count',1))
    if not 1<=count<=3:raise ValueError('Допустимо 1–3 индекса.')
    ranges=[int(get('Variable index',str(i+1),1)) for i in range(count)]
    if any(v<1 or v>100 for v in ranges):raise ValueError('Неверные диапазоны индексов.')
    names=tuple('x'+','.join(map(str,idx)) for idx in itertools.product(*(range(1,v+1) for v in ranges)))
    if len(names)!=n:raise ValueError('Число переменных не совпадает с произведением диапазонов индексов.')
    return Problem([get('Aim function',str(j+1),0) for j in range(n)],
                   [[get('Condition array',f'{i+1}, {j+1}',0) for j in range(n)] for i in range(m)],
                   [get('Limit vector',str(i+1),0) for i in range(m)],
                   [SIGNS[int(get('Limit signs',str(i+1),get('Task parameters','Default Sign',0)))] for i in range(m)],
                   'min' if get('Task parameters','Optimum','optMin')=='optMin' else 'max',path.stem,names)

def save(path,p,integer=False,integer_goal=False):
    path=Path(path)
    if path.suffix.lower()=='.ini':
        if len(p.c)>20 or len(p.b)>20:raise ValueError('Старый LDPTechs принимает не более 20 переменных и 20 ограничений. Сохраните большую задачу в JSON.')
        conf=configparser.ConfigParser(interpolation=None);conf.optionxform=str
        conf['Task parameters']={'Method':'omdCutting' if integer else 'omdSimplex','Optimum':'optMax' if p.sense=='max' else 'optMin','NumKind':'frkFrac','Variables':str(len(p.c)),'Conditions':str(len(p.b)),'Default Sign':'0'}
        conf['Debug and Log']={'By Step':'False'};conf['Variable kinds']={'0':'vkdInt' if integer_goal else 'vkdReal'}
        conf['Variable index']={'Count':'1','1':str(len(p.c))}
        conf['Aim function']={str(j+1):str(v) for j,v in enumerate(p.c)}
        conf['Limit vector']={str(i+1):str(v) for i,v in enumerate(p.b)}
        conf['Limit signs']={str(i+1):str(next(k for k,v in SIGNS.items() if v==s)) for i,s in enumerate(p.signs)}
        conf['Condition array']={f'{i+1}, {j+1}':str(v) for i,r in enumerate(p.A) for j,v in enumerate(r)}
        import io
        stream=io.StringIO();conf.write(stream);text=stream.getvalue()
    else:text=json.dumps({**as_dict(p),'integer':integer,'integer_goal':integer_goal},ensure_ascii=False,indent=2)
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.',dir=path.resolve().parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8',newline='') as f:f.write(text);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def settings(path):
    path=Path(path)
    if path.suffix.lower()!='.ini':
        d=json.loads(path.read_text(encoding='utf-8-sig'));return bool(d.get('integer',False)),bool(d.get('integer_goal',False))
    conf=configparser.ConfigParser(interpolation=None)
    try:text=path.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:text=path.read_text(encoding='cp1251')
    conf.read_string(text)
    return conf.get('Task parameters','Method',fallback='omdSimplex')=='omdCutting',conf.get('Variable kinds','0',fallback='vkdInt')=='vkdInt'
