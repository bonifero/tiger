from dataclasses import dataclass
from fractions import Fraction as Q

def number(value):
    text=str(value).strip().replace(',', '.').replace('_',' ')
    if ' ' in text:
        whole, rest=text.split()
        return Q(whole)+(-1 if whole.startswith('-') else 1)*Q(rest)
    return Q(text)

@dataclass(frozen=True)
class Problem:
    c: tuple
    A: tuple
    b: tuple
    signs: tuple
    sense: str='max'
    name: str='Новая задача'
    variable_names: tuple=()

    def __post_init__(self):
        object.__setattr__(self,'c',tuple(map(number,self.c)))
        object.__setattr__(self,'A',tuple(tuple(map(number,r)) for r in self.A))
        object.__setattr__(self,'b',tuple(map(number,self.b)))
        object.__setattr__(self,'signs',tuple(self.signs))
        if not 1<=len(self.c)<=100 or not 1<=len(self.b)<=200: raise ValueError('Допустимо 1–100 переменных и 1–200 ограничений.')
        if len(self.A)!=len(self.b) or len(self.signs)!=len(self.b) or any(len(r)!=len(self.c) for r in self.A): raise ValueError('Неверные размеры матрицы.')
        if self.sense not in ('min','max') or any(s not in ('<=','=','>=','<','>') for s in self.signs): raise ValueError('Неверный знак или направление оптимизации.')
        if self.variable_names and len(self.variable_names)!=len(self.c): raise ValueError('Неверное число имён переменных.')

    @property
    def names(self): return self.variable_names or tuple(f'x{i+1}' for i in range(len(self.c)))

    def feasible(self,x,integer=False,integer_goal=False):
        if len(x)!=len(self.c) or any(v<0 for v in x): return False
        if integer and any(v.denominator!=1 for v in x): return False
        if integer_goal and sum(a*v for a,v in zip(self.c,x)).denominator!=1: return False
        for row,rhs,s in zip(self.A,self.b,self.signs):
            lhs=sum(a*v for a,v in zip(row,x))
            if not {'<=':lhs<=rhs,'>=':lhs>=rhs,'=':lhs==rhs,'<':lhs<rhs,'>':lhs>rhs}[s]: return False
        return True
