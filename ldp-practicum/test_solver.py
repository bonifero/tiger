import json
import random
import tempfile
import unittest
from pathlib import Path
from fractions import Fraction as Q
from model import Problem,number
from simplex import solve
from presets import PRESETS
from formats import save,load

def result(p,ip=False,goal=False):return list(solve(p,ip,goal,limit=800))[-1]

class SolverTests(unittest.TestCase):
    def test_presets(self):
        for p,expected in zip(PRESETS,[67,2905,5500000,165,None,2800,18800]):
            with self.subTest(p=p.name):
                e=result(p,True)
                self.assertEqual(e.status,'infeasible' if expected is None else 'optimal')
                if expected is not None:self.assertEqual(e.objective,expected);self.assertTrue(p.feasible(e.x,True))
    def test_numeric_regressions(self):
        self.assertEqual(number('-3 2/5'),-Q(17,5));self.assertEqual(number('0,125'),Q(1,8))
        p=Problem([1],[[1]],['2.5'],['<='])
        self.assertEqual(result(p,True).x,(Q(2),))
        p=Problem([1],[[1]],['1.5'],['<'])
        self.assertEqual(result(p,True).x,(Q(1),))
        with self.assertRaises(ValueError):result(p)
        p=Problem(['0.5'],[[1]],[3],['<='])
        self.assertEqual(result(p,True).objective,Q(3,2));self.assertEqual(result(p,True,True).objective,1)
    def test_statuses(self):
        self.assertEqual(result(Problem([1],[[1],[-1]],[1,-2],['<=','<='])).status,'infeasible')
        self.assertEqual(result(Problem([1],[[-1]],[0],['<='])).status,'unbounded')
        self.assertEqual(result(Problem([1],[[2]],[1],['=']),True).status,'infeasible')
        self.assertEqual(result(Problem([1],[[0],[1]],[0,2],['=','<='])).objective,2)
        self.assertEqual(result(Problem([0,1],[[2,0]],[1],['=']),True).status,'undetermined')
    def test_files(self):
        with tempfile.TemporaryDirectory() as d:
            for suffix in ('json','ini'):
                p=PRESETS[2];path=Path(d)/('case.'+suffix);save(path,p);q=load(path)
                self.assertEqual((p.c,p.A,p.b,p.signs,p.sense),(q.c,q.A,q.b,q.signs,q.sense))
                save(path,PRESETS[0]);self.assertEqual(load(path).A,PRESETS[0].A)
    def test_research_cases(self):
        path=Path(__file__).resolve().parent/'tests_data/research_cases.json'
        if not path.exists():self.skipTest('Research fixtures are not present in this standalone checkout')
        signs={-2:'<',-1:'<=',0:'=',1:'>=',2:'>'}
        for case in json.loads(path.read_text(encoding='utf-8'))['cases']:
            m=case['model'];ip=case['method']=='omdCutting'
            p=Problem(m['c'],m['A'],m['b'],[signs[s] for s in m.get('signs',[-1]*len(m['b']))],m['sense'])
            with self.subTest(file=case['file']):
                if any(s in ('<','>') for s in p.signs):
                    if not ip:
                        with self.assertRaises(ValueError):result(p)
                    else:
                        e=result(p,True);self.assertEqual(e.status,'optimal');self.assertTrue(p.feasible(e.x,True))
                    continue
                e=result(p,ip);oracle=case['expected']['integer' if ip else 'lp']
                if oracle['status']==0:self.assertEqual(e.status,'optimal');self.assertAlmostEqual(float(e.objective),oracle['objective'],places=5)
                elif oracle['status']==2:self.assertEqual(e.status,'infeasible')
                elif oracle['status']==3:self.assertEqual(e.status,'unbounded')
                else:self.assertIn(e.status,('infeasible','unbounded','undetermined'))
    def test_against_independent_oracle(self):
        from scipy.optimize import linprog,milp,Bounds,LinearConstraint
        import numpy as np
        rng=random.Random(2701)
        completed=0;limited=0
        for i in range(80):
            n=rng.randint(1,4);m=rng.randint(1,4)
            A=[[rng.randint(-3,7) for _ in range(n)] for _ in range(m)]+[[int(j==k) for j in range(n)] for k in range(n)]
            b=[rng.randint(0,20) for _ in range(m)]+[rng.randint(1,8) for _ in range(n)]
            c=[rng.randint(-5,9) for _ in range(n)];p=Problem(c,A,b,['<=']*len(b),'max' if i%2 else 'min')
            target=np.array(c)*(1 if p.sense=='min' else -1)
            for ip in (False,True):
                oracle=milp(target,integrality=np.ones(n),bounds=Bounds(0,np.inf),constraints=LinearConstraint(A,-np.inf,b),options={'mip_rel_gap':0}) if ip else linprog(target,A_ub=A,b_ub=b,bounds=(0,None),method='highs')
                e=result(p,ip)
                with self.subTest(i=i,ip=ip):
                    if e.status=='limit':
                        self.assertTrue(ip);limited+=1;continue
                    self.assertEqual(e.status,'optimal');self.assertTrue(p.feasible(e.x,ip))
                    self.assertAlmostEqual(float(e.objective),float(oracle.fun)*(1 if p.sense=='min' else -1),places=6)
                    completed+=1
        print(f'Independent comparisons: {completed} matched, {limited} reached explicit limit')
        self.assertGreaterEqual(completed,140)

if __name__=='__main__':unittest.main()
