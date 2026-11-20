"""Exact two-phase primal simplex, dual simplex and integer Gomory cuts."""
from fractions import Fraction as Q
from math import lcm, floor, ceil
from dataclasses import dataclass

@dataclass
class Event:
    title: str
    rows: tuple
    basis: tuple
    names: tuple
    status: str='running'
    x: tuple=()
    objective: object=None
    iteration: int=0
    cuts: int=0
    pivot: object=None

class ResourceLimit(Exception):pass

def solve(problem,integer=False,integer_goal=False,limit=2000):
    fallback=False
    try:
        for e in _solve(problem,integer,integer_goal,limit):
            if integer and e.status=='limit':fallback=True;break
            yield e
    except ResourceLimit:
        if integer:fallback=True
        else:yield Event('Достигнут лимит размера точных чисел',(),(),(),status='limit')
    if fallback:
        yield Event('Лимит отсечений · переход к ветвям и границам',(),(),())
        yield from branch_and_bound(problem,integer_goal,min(limit,500))

def branch_and_bound(problem,integer_goal,limit):
    from model import Problem
    data=[]
    for row,b,s in zip(problem.A,problem.b,problem.signs):
        scale=lcm(*(v.denominator for v in row));row=tuple(v*scale for v in row);b*=scale
        if s=='<':s='<=';b=Q(ceil(b)-1)
        elif s=='>':s='>=';b=Q(floor(b)+1)
        data.append((row,b,s))
    root=Problem(problem.c,[d[0] for d in data],[d[1] for d in data],[d[2] for d in data],problem.sense,problem.name,problem.names)
    stack=[root];best=None;nodes=0
    while stack:
        if nodes>=limit:yield Event('Достигнут лимит узлов ветвления',(),(),(),status='limit');return
        p=stack.pop();nodes+=1;e=None
        try:
            for e in _solve(p,False,False,limit=2000):pass
        except ResourceLimit:yield Event('Лимит точной арифметики в подзадаче',(),(),(),status='limit');return
        if e.status=='infeasible':continue
        if e.status!='optimal':
            yield Event('Статус целочисленной подзадачи не установлен',(),(),(),status='undetermined');return
        yield Event(f'Ветви и границы · подзадача {nodes}',e.rows,e.basis,e.names,x=e.x,objective=e.objective,iteration=nodes)
        if best and (e.objective>=best.objective if problem.sense=='min' else e.objective<=best.objective):continue
        j=next((j for j,v in enumerate(e.x) if v.denominator!=1),None)
        if j is None and (not integer_goal or e.objective.denominator==1):best=e;continue
        coeff=tuple(Q(int(k==j)) for k in range(len(p.c))) if j is not None else p.c
        value=e.x[j] if j is not None else e.objective
        for row,b in [(tuple(-v for v in coeff),Q(-ceil(value))),(coeff,Q(floor(value)))]:
            stack.append(Problem(p.c,(*p.A,row),(*p.b,b),(*p.signs,'<='),p.sense,p.name,p.names))
    if best:
        if not problem.feasible(best.x,True,integer_goal):raise ArithmeticError('План ветвления не прошёл проверку.')
        yield Event('Оптимум доказан ветвями и границами',best.rows,best.basis,best.names,'optimal',best.x,best.objective,nodes)
    else:yield Event('Целочисленные ограничения несовместны',(),(),(),status='infeasible')

def _solve(problem,integer=False,integer_goal=False,limit=2000):
    n0=len(problem.c); costs=list(problem.c); data=[]
    for row,b,s in zip(problem.A,problem.b,problem.signs):
        row=list(row)
        if s in ('<','>') and not integer: raise ValueError('Строгие неравенства для непрерывной задачи не поддерживаются: используйте <= или >=.')
        if integer:
            scale=lcm(*(a.denominator for a in row))
            row=[a*scale for a in row];b*=scale
            if s=='<': b=Q(ceil(b)-1);s='<='
            elif s=='>': b=Q(floor(b)+1);s='>='
            elif s=='<=': b=Q(floor(b))
            elif s=='>=': b=Q(ceil(b))
            elif b.denominator!=1:
                yield Event('Целочисленное равенство несовместно',(),(),(),status='infeasible');return
        if b<0:
            row=[-v for v in row];b=-b;s={'<=':'>=','>=':'<=','=':'='}[s]
        data.append([row,b,s])
    names=list(problem.names)
    if integer and integer_goal:
        for row,_,_ in data: row.extend([Q(0),Q(0)])
        scale=lcm(*(v.denominator for v in costs))
        data.append([[v*scale for v in costs]+[Q(-scale),Q(scale)],Q(0),'='])
        costs.extend([Q(0),Q(0)]);names.extend(['F+','F−'])
    rows=[list(row)+[b] for row,b,_ in data];basis=[];art=set()
    def column(name):
        names.append(name)
        for r in rows:r.insert(-1,Q(0))
        return len(names)-1
    for i,(_,_,s) in enumerate(data):
        if s!='=':
            j=column(f's{i+1}');rows[i][j]=Q(1 if s=='<=' else -1)
        if s=='<=':basis.append(j)
        else:
            j=column(f'a{i+1}');rows[i][j]=Q(1);basis.append(j);art.add(j)
    count=0;cuts=0
    def objective(c):
        z=[-v for v in c]+[Q(0)]
        for r,j in zip(rows,basis):
            v=z[j]
            z=[a-v*b for a,b in zip(z,r)]
        return z
    def pivot(i,j,z):
        nonlocal count
        d=rows[i][j];rows[i]=[v/d for v in rows[i]]
        for k in range(len(rows)):
            if k!=i:
                d=rows[k][j];rows[k]=[a-d*b for a,b in zip(rows[k],rows[i])]
        d=z[j];z[:]=[a-d*b for a,b in zip(z,rows[i])];basis[i]=j;count+=1
        if any(abs(v.numerator).bit_length()>256 or v.denominator.bit_length()>256 for r in rows for v in r):raise ResourceLimit()
    def event(title,z,status='running',p=None):
        x=[Q(0)]*len(names)
        for r,j in zip(rows,basis):x[j]=r[-1]
        value=sum(a*b for a,b in zip(problem.c,x[:n0]))
        return Event(title,tuple(tuple(r) for r in rows+[z]),tuple(basis),tuple(names),status,tuple(x[:n0]),value,count,cuts,p)
    def primal(z,title):
        while True:
            if count>=limit:return 'limit'
            entering=next((j for j,v in enumerate(z[:-1]) if v<0),None)
            if entering is None:return 'optimal'
            candidates=[i for i,r in enumerate(rows) if r[entering]>0]
            if not candidates:return 'unbounded'
            i=min(candidates,key=lambda i:(rows[i][-1]/rows[i][entering],basis[i]))
            pivot(i,entering,z)
            yield event(title,z,p=(i,entering))
    if art:
        z=objective([Q(-1) if j in art else Q(0) for j in range(len(names))])
        yield event('Фаза I · поиск допустимого базиса',z)
        status=yield from primal(z,'Фаза I · симплекс-шаг')
        if status=='limit':yield event('Достигнут лимит шагов',z,'limit');return
        if z[-1]!=0:yield event('Ограничения несовместны',z,'infeasible');return
        for i in reversed(range(len(rows))):
            if basis[i] in art:
                j=next((j for j,v in enumerate(rows[i][:-1]) if j not in art and v),None)
                if j is None:rows.pop(i);basis.pop(i)
                else:pivot(i,j,z)
        keep=[j for j in range(len(names)) if j not in art]
        rows[:]=[[r[j] for j in keep]+[r[-1]] for r in rows]
        basis[:]=[keep.index(j) for j in basis];names[:]=[names[j] for j in keep]
    direction=1 if problem.sense=='max' else -1
    z=objective([direction*costs[j] if j<len(costs) else Q(0) for j in range(len(names))])
    yield event('Фаза II · исходная целевая функция',z)
    integer_columns=[True]*len(names)
    while True:
        status=yield from primal(z,'Симплекс-шаг')
        if status!='optimal':
            title='Целевая функция не ограничена' if status=='unbounded' else 'Достигнут лимит шагов'
            if status=='unbounded' and integer and not problem.feasible(event('',z).x,True,integer_goal):
                status='undetermined';title='LP-релаксация не ограничена; статус целочисленной задачи не установлен'
            yield event(title,z,status);return
        if not integer:break
        i=next((i for i,r in enumerate(rows) if integer_columns[basis[i]] and r[-1].denominator!=1),None)
        if i is None:break
        if count+cuts>=limit:yield event('Достигнут лимит отсечений',z,'limit');return
        # Mixed-integer Gomory: cut slacks are continuous. Treating every
        # subsequent slack as integer would incorrectly discard feasible x.
        f=rows[i][-1]-floor(rows[i][-1]);ratio=f/(1-f);cut=[]
        for j,a in enumerate(rows[i][:-1]):
            if integer_columns[j]:
                part=a-floor(a);v=part if part<=f else ratio*(1-part)
            else:v=a if a>=0 else -ratio*a
            cut.append(-v)
        cut.append(-f)
        for r in rows:r.insert(-1,Q(0))
        z.insert(-1,Q(0));names.append(f'g{cuts+1}')
        integer_columns.append(False)
        cut.insert(-1,Q(1));rows.append(cut);basis.append(len(names)-1);cuts+=1
        yield event('Добавлено отсечение Гомори',z)
        while any(r[-1]<0 for r in rows):
            if count+cuts>=limit:yield event('Достигнут лимит шагов',z,'limit');return
            i=min((i for i,r in enumerate(rows) if r[-1]<0),key=lambda i:basis[i])
            js=[j for j,v in enumerate(rows[i][:-1]) if v<0]
            if not js:yield event('Целочисленные ограничения несовместны',z,'infeasible');return
            j=min(js,key=lambda j:(z[j]/(-rows[i][j]),j))
            pivot(i,j,z);yield event('Двойственный симплекс-шаг',z,p=(i,j))
    result=event('Оптимальное решение найдено',z,'optimal')
    if not problem.feasible(result.x,integer,integer_goal):raise ArithmeticError('Конечный план не прошёл проверку исходных ограничений.')
    yield result
