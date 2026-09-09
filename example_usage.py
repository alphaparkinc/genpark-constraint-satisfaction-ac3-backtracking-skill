"""
Demonstration of Constraint Satisfaction AC-3 Backtracking Skill
"""

from client import CSPSolver

def main():
    print("=== Solving Map Coloring CSP with AC-3 and MRV Backtracking ===")
    variables = ["WA", "NT", "SA", "Q", "NSW", "V"]
    colors = ["red", "green", "blue"]
    domains = {v: list(colors) for v in variables}

    csp = CSPSolver(variables, domains)

    # Adjacent territories cannot share color
    diff = lambda a, b: a != b
    csp.add_binary_constraint("WA", "NT", diff)
    csp.add_binary_constraint("WA", "SA", diff)
    csp.add_binary_constraint("NT", "SA", diff)
    csp.add_binary_constraint("NT", "Q", diff)
    csp.add_binary_constraint("SA", "Q", diff)
    csp.add_binary_constraint("SA", "NSW", diff)
    csp.add_binary_constraint("SA", "V", diff)
    csp.add_binary_constraint("Q", "NSW", diff)
    csp.add_binary_constraint("NSW", "V", diff)

    print("Running AC-3 Domain Pruning and Backtracking Search...")
    solution = csp.solve_backtracking()
    print("CSP Solution Found:")
    for territory, color in sorted(solution.items()):
        print(f"  {territory}: {color}")

    assert solution is not None
    # Validate no adjacent conflict
    for (v1, v2), fn in csp.constraints.items():
        assert fn(solution[v1], solution[v2])
    print("\nConstraint Satisfaction AC-3 Verification PASS!")

if __name__ == "__main__":
    main()
