"""
MCP Server for Constraint Satisfaction AC-3 Backtracking Skill
"""

import json
import sys
from client import CSPSolver

def handle_call(name: str, args: dict) -> dict:
    if name == "solve_map_color":
        vars_list = args.get("variables", ["A", "B"])
        domains_map = args.get("domains", {"A": ["red", "blue"], "B": ["red", "blue"]})
        edges = args.get("edges", [["A", "B"]])
        csp = CSPSolver(vars_list, domains_map)
        for e in edges:
            csp.add_binary_constraint(e[0], e[1], lambda a, b: a != b)
        sol = csp.solve_backtracking()
        return {"solution": sol}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_call(req.get("method"), req.get("params", {}))
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
