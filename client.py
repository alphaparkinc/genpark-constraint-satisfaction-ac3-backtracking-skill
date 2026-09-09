"""
Constraint Satisfaction AC-3 Backtracking Skill Client
Pure Python Standard Library implementation of Constraint Satisfaction Problems (CSP).
Applies Arc Consistency (AC-3 / Mackworth) to prune variable domains, combined with
Minimum Remaining Values (MRV) heuristic backtracking search.
"""

from typing import List, Dict, Any, Tuple, Optional, Set, Callable


class CSPSolver:
    def __init__(self, variables: List[str], domains: Dict[str, List[Any]]):
        self.variables = variables
        self.domains: Dict[str, List[Any]] = {v: list(domains[v]) for v in variables}
        self.constraints: Dict[Tuple[str, str], Callable[[Any, Any], bool]] = {}
        self.neighbors: Dict[str, Set[str]] = {v: set() for v in variables}

    def add_binary_constraint(self, var1: str, var2: str, constraint_fn: Callable[[Any, Any], bool]):
        self.constraints[(var1, var2)] = constraint_fn
        # Symmetric constraint
        self.constraints[(var2, var1)] = lambda b, a: constraint_fn(a, b)
        self.neighbors[var1].add(var2)
        self.neighbors[var2].add(var1)

    def ac3(self) -> bool:
        """Enforce Arc Consistency AC-3. Returns False if a domain becomes empty."""
        queue: List[Tuple[str, str]] = list(self.constraints.keys())

        while queue:
            xi, xj = queue.pop(0)
            if self._revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def _revise(self, xi: str, xj: str) -> bool:
        revised = False
        fn = self.constraints.get((xi, xj))
        if not fn:
            return False

        to_remove = []
        for x in self.domains[xi]:
            has_support = any(fn(x, y) for y in self.domains[xj])
            if not has_support:
                to_remove.append(x)
                revised = True

        for x in to_remove:
            self.domains[xi].remove(x)
        return revised

    def solve_backtracking(self) -> Optional[Dict[str, Any]]:
        """Solve CSP using backtracking with MRV variable ordering."""
        if not self.ac3():
            return None
        return self._backtrack({})

    def _backtrack(self, assignment: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if len(assignment) == len(self.variables):
            return assignment

        # MRV: Choose unassigned variable with smallest domain
        unassigned = [v for v in self.variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(self.domains[v]))

        for val in self.domains[var]:
            consistent = True
            for neighbor in self.neighbors[var]:
                if neighbor in assignment:
                    fn = self.constraints.get((var, neighbor))
                    if fn and not fn(val, assignment[neighbor]):
                        consistent = False
                        break

            if consistent:
                assignment[var] = val
                result = self._backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]

        return None
