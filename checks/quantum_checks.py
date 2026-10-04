#!/usr/bin/env python3
"""Exact finite checks for the reference flag and stationary quantum example.

Python 3.10+; standard library only. Matrix entries of the Hadamard block
are represented in Q(sqrt(2)). State entries and partial traces use Fraction.
This checks the displayed finite gates, not the universal conversion theorem.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from typing import TypeAlias
import json

Root = Path(__file__).resolve().parents[1]
Surd: TypeAlias = tuple[F, F]  # a + b sqrt(2)
ZERO: Surd = (F(0), F(0))
ONE: Surd = (F(1), F(0))
HALF_ROOT: Surd = (F(0), F(1, 2))


def add(a: Surd, b: Surd) -> Surd:
    return a[0] + b[0], a[1] + b[1]


def mul(a: Surd, b: Surd) -> Surd:
    return a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def index(a: int, b: int) -> int:
    return 7 * a + b


def cells(k: int) -> tuple[int, int]:
    return divmod(k, 7)


def flag_map(b: int, a1: int, a2: int) -> tuple[int, int, int]:
    if b not in (0, 1) or not (0 <= a1 < 7 and 0 <= a2 < 7):
        raise ValueError("Configuration outside the 98-state apparatus")
    return (b, a1, a2) if b == 0 else (b, a2, a1)


def check_flag() -> dict[str, object]:
    basis = list(product(range(2), range(7), range(7)))
    images = [flag_map(*v) for v in basis]
    assert len(set(images)) == len(basis) == 98
    for v, w in zip(basis, images):
        assert v[1] + v[2] == w[1] + w[2]
        assert flag_map(*w) == v
    examples = [F(0), F(1), F(1, 2), F(1, 3), F(1, 1000)]
    for t in examples:
        joint: dict[tuple[int, int, int], F] = defaultdict(F)
        joint[flag_map(0, 2, 3)] += 1 - t
        joint[flag_map(1, 2, 3)] += t
        control: dict[int, F] = defaultdict(F)
        output: dict[tuple[int, int], F] = defaultdict(F)
        for (b, a1, a2), prob in joint.items():
            control[b] += prob
            output[a1, a2] += prob
        assert control[0] == 1 - t and control[1] == t
        assert output[2, 3] == 1 - t and output[3, 2] == t
        tv_from_x = (abs(output[2, 3] - 1) + output[3, 2]) / 2
        assert tv_from_x == t
    return {
        "configurations": 98,
        "bijection": True,
        "energy_preserved_exactly": True,
        "involution": True,
        "tested_t": [str(t) for t in examples],
        "whole_control_marginal_returned_exactly": True,
        "distance_from_sharp_flag": "t (linear identity, both endpoints checked)",
    }


def check_quantum() -> dict[str, object]:
    x, y = index(2, 3), index(3, 2)
    # Each dictionary is a column of a 49-by-49 real matrix over Q(sqrt(2)).
    cols: list[dict[int, Surd]] = [{j: ONE} for j in range(49)]
    cols[x] = {x: HALF_ROOT, y: HALF_ROOT}
    cols[y] = {x: HALF_ROOT, y: (F(0), F(-1, 2))}
    for i, j in product(range(49), repeat=2):
        value = ZERO
        for k in cols[i].keys() & cols[j].keys():
            value = add(value, mul(cols[i][k], cols[j][k]))
        assert value == (ONE if i == j else ZERO)
    for j, col in enumerate(cols):
        for i, value in col.items():
            assert value != ZERO
            assert sum(cells(i)) == sum(cells(j))
    # H |2,3><2,3| H^* has four rational entries, all 1/2.
    psi: dict[tuple[int, int], F] = {}
    for i, j in product(cols[x], repeat=2):
        a, b = mul(cols[x][i], cols[x][j])
        assert b == 0
        psi[i, j] = a
    assert psi == {(i, j): F(1, 2) for i, j in product((x, y), repeat=2)}
    # The controlled relative phase is diagonal with signs +/-1 on all 98 states.
    sign = {(b, f): (-1 if b == 1 and f == y else 1)
            for b, f in product(range(2), range(49))}
    assert len(sign) == 98 and all(v * v == 1 for v in sign.values())
    # Classical uniform control has no coherence between its two branches.
    joint: dict[tuple[int, int, int, int], F] = {}
    for b in range(2):
        for (i, j), a in psi.items():
            joint[b, i, b, j] = a * sign[b, i] * sign[b, j] / 2
    system: dict[tuple[int, int], F] = defaultdict(F)
    control: dict[tuple[int, int], F] = defaultdict(F)
    for (b, i, c, j), a in joint.items():
        if b == c:
            system[i, j] += a
        if i == j:
            control[b, c] += a
    system = {k: v for k, v in system.items() if v}
    control = {k: v for k, v in control.items() if v}
    assert system == {(x, x): F(1, 2), (y, y): F(1, 2)}
    assert control == {(0, 0): F(1, 2), (1, 1): F(1, 2)}
    # Partial transpose on cell 2; test the normalized |2,2>-|3,3> vector.
    pt: dict[tuple[int, int], F] = defaultdict(F)
    for (i, j), a in psi.items():
        ai, bi = cells(i)
        aj, bj = cells(j)
        pt[index(ai, bj), index(aj, bi)] += a
    v = {index(2, 2): F(1), index(3, 3): F(-1)}
    numerator = sum(v[i] * pt.get((i, j), F(0)) * v[j]
                    for i, j in product(v, repeat=2))
    expectation = numerator / sum(a * a for a in v.values())
    assert expectation == F(-1, 2)
    return {
        "Hadamard_dimension": 49,
        "Hadamard_orthogonality_entries_checked": 49 * 49,
        "arithmetic": "exact Q(sqrt(2)) for gate; rational density matrices",
        "Hadamard_unitary": True,
        "Hadamard_energy_preserving": True,
        "controlled_phase_dimension": 98,
        "controlled_phase_unitary_and_energy_preserving": True,
        "output_is_equal_energy_flag_mixture": True,
        "control_marginal_returned_exactly": True,
        "entanglement_partial_transpose_expectation": str(expectation),
    }


def main() -> None:
    result = {"flag": check_flag(), "stationary_quantum_example": check_quantum()}
    out = Root / "checks" / "quantum_results.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
