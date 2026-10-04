#!/usr/bin/env python3
"""Exact reversible circuit checks and reproducible thermodynamic figure data.

Only Python's standard library is required. The complete 1029-configuration
permutation is checked for bijectivity and energy conservation. Stationarity
and the repeated-visit checks use Fraction arithmetic. Floating point is used
only for logarithms, the finite Gibbs example, and the plotted curve.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import exp, log
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def entropy(p) -> float:
    return -sum(float(x) * log(float(x)) for x in p if x)


def gibbs(beta: float):
    a = [exp(-beta*j) for j in range(7)]
    z = sum(a)
    p = [x/z for x in a]
    return p, sum(j*p[j] for j in range(7)), entropy(p)


def engine() -> dict:
    b1,b2 = log(2),log(4)
    _,u1,s1 = gibbs(b1)
    _,u2,s2 = gibbs(b2)
    target=(s1+s2)/2
    lo,hi=b1,b2
    for _ in range(100):
        mid=(lo+hi)/2
        if gibbs(mid)[2] > target:
            lo=mid
        else:
            hi=mid
    bf=(lo+hi)/2
    _,uf,sf=gibbs(bf)
    w=u1+u2-2*uf
    p1,_,_=gibbs(b1)
    p2,_,_=gibbs(b2)
    pf,_,_=gibbs(bf)
    divergence=sum(p1[i]*p2[j]*log(p1[i]*p2[j]/(pf[i]*pf[j]))
                   for i,j in product(range(7),repeat=2))
    assert w > 0 and abs(bf*w-divergence) < 1e-12
    return dict(beta1=b1,beta2=b2,energy1=u1,energy2=u2,
                entropy1=s1,entropy2=s2,beta_final=bf,energy_final=uf,
                entropy_final=sf,work=w,relative_entropy=divergence,
                midpoint_energy=(u1+u2)/2)


def clock_gate(state):
    """The paper's full basis permutation, with clock labels 1, 2, 3."""
    s,a,b,k=state
    triple=(s,a,b)
    if k==3:
        if triple==(1,1,1):
            triple=(0,1,2)
        elif triple==(0,1,2):
            triple=(1,1,1)
    s,a,b=triple
    return (b,s,a,1 if k==3 else k+1)


def check_clock() -> dict:
    states=list(product(range(7),range(7),range(7),range(1,4)))
    outputs=[clock_gate(x) for x in states]
    assert len(states)==1029
    assert set(outputs)==set(states) and len(set(outputs))==len(states)
    assert all(sum(x[:3])==sum(y[:3]) for x,y in zip(states,outputs))
    c={(0,1,1):F(1,3),(1,0,2):F(1,3),(1,1,3):F(1,3)}

    def visit(memory):
        joint={}
        for (a,b,k),prob in memory.items():
            y=clock_gate((1,a,b,k))
            joint[y]=joint.get(y,F(0))+prob
        out_s=[sum(prob for y,prob in joint.items() if y[0]==j)
               for j in range(7)]
        out_c={}
        for y,prob in joint.items():
            key=y[1:]
            out_c[key]=out_c.get(key,F(0))+prob
        return joint,out_s,out_c

    joint,out_s,out_c=visit(c)
    assert out_c==c and out_s==[F(1,3)]*3+[F(0)]*4
    current=c
    for _ in range(100):
        _,s_now,current=visit(current)
        assert current==c and s_now==out_s
    mi=entropy(out_s)+entropy(c.values())-entropy(joint.values())
    assert abs(mi-log(3))<1e-13

    # There are three possible histories, not independent fresh thermal draws.
    histories=[]
    for initial in c:
        memory=initial
        emitted=[]
        for _ in range(30):
            y=clock_gate((1,*memory))
            emitted.append(y[0])
            memory=y[1:]
        assert memory==initial
        assert all(emitted[i]==emitted[i%3] for i in range(30))
        histories.append(emitted)
    assert len({tuple(x) for x in histories})==3
    return dict(configurations=len(states),permutation_entries=len(states),
                bijection_exact=True,energy_conservation_exact=True,
                whole_memory_stationarity_exact=True,repeated_marginal_visits=100,
                output_probabilities=[str(x) for x in out_s],
                memory_entropy=entropy(c.values()),mutual_information=mi,
                predicted_mutual_information=log(3),
                example_histories_first_nine=[x[:9] for x in histories],
                history_entropy=log(3),history_period=3)


def check_work() -> dict:
    basis=list(product(range(7),repeat=2))
    for j in range(6):
        k=j if j>=1 else 1
        mapping={x:x for x in basis}
        pairs=[((j,k),(j+1,k-1)),((j+1,k),(j,k+1))]
        assert len({x for pair in pairs for x in pair})==4
        for a,b in pairs:
            mapping[a],mapping[b]=b,a
        assert set(mapping.values())==set(basis)
        assert all(sum(x)==sum(y) for x,y in mapping.items())
        assert mapping[(j,k)]==(j+1,k-1)
        assert mapping[(j+1,k)]==(j,k+1)
    return dict(adjacent_pairs=6,configurations_per_gate=49,
                all_gates_bijective=True,energy_conservation_exact=True)


def main() -> None:
    results=dict(clock=check_clock(),work=check_work(),engine=engine())
    (ROOT/'checks').mkdir(exist_ok=True)
    (ROOT/'figures').mkdir(exist_ok=True)
    (ROOT/'checks'/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    with (ROOT/'figures'/'gibbs_curve.dat').open('w') as f:
        f.write('beta U S\n')
        for i in range(1201):
            beta=0.03+12*i/1200
            _,u,s=gibbs(beta)
            f.write(f'{beta:.12g} {u:.14g} {s:.14g}\n')
    e=results['engine']
    vals=dict(Uone=e['energy1'],Utwo=e['energy2'],Sone=e['entropy1'],
              Stwo=e['entropy2'],Ufinal=e['energy_final'],
              Sfinal=e['entropy_final'],Umid=e['midpoint_energy'])
    with (ROOT/'figures'/'example_values.tex').open('w') as f:
        f.write('% Generated by checks/model_checks.py\n')
        for key,value in vals.items():
            f.write('\\newcommand{\\Example'+key+'}{'+format(value,'.12g')+'}\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    main()
