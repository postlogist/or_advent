from ortools.sat.python import cp_model


def solve_2d_cutting(items, sheets):
    model = cp_model.CpModel()

    n_items = len(items)
    n_sheets = len(sheets)

    # Variables for item positions, rotation, and assignment
    x = {}
    y = {}
    rotated = {}
    assigned_sheet = {}

    for i in range(n_items):
        for s in range(n_sheets):
            x[(i, s)] = model.NewIntVar(0, sheets[s][0], f'x_{i}_{s}')
            y[(i, s)] = model.NewIntVar(0, sheets[s][1], f'y_{i}_{s}')
            rotated[(i, s)] = model.NewBoolVar(f'rotated_{i}_{s}')
            assigned_sheet[(i, s)] = model.NewBoolVar(f'assigned_{i}_{s}')

    # Variables for sheet usage
    used_sheet = [model.NewBoolVar(f'used_sheet_{s}') for s in range(n_sheets)]

    # Derived dimensions based on rotation
    item_width = {}
    item_height = {}
    for i in range(n_items):
        for s in range(n_sheets):
            item_width[(i, s)] = model.NewIntVar(0, max(item[0]
                                                        for item in items), f'item_width_{i}_{s}')
            item_height[(i, s)] = model.NewIntVar(0, max(item[1]
                                                         for item in items), f'item_height_{i}_{s}')
            model.Add(item_width[(i, s)] == items[i][0]
                      ).OnlyEnforceIf(rotated[(i, s)].Not())
            model.Add(item_width[(i, s)] == items[i][1]
                      ).OnlyEnforceIf(rotated[(i, s)])
            model.Add(item_height[(i, s)] == items[i][1]
                      ).OnlyEnforceIf(rotated[(i, s)].Not())
            model.Add(item_height[(i, s)] == items[i][0]
                      ).OnlyEnforceIf(rotated[(i, s)])

    # Ensure every item is placed exactly once
    for i in range(n_items):
        model.Add(sum(assigned_sheet[(i, s)] for s in range(n_sheets)) == 1)

    # Ensure items fit within assigned sheets
    for i in range(n_items):
        for s in range(n_sheets):
            model.Add(x[(i, s)] + item_width[(i, s)] <= sheets[s]
                      [0]).OnlyEnforceIf(assigned_sheet[(i, s)])
            model.Add(y[(i, s)] + item_height[(i, s)] <= sheets[s]
                      [1]).OnlyEnforceIf(assigned_sheet[(i, s)])

    # Prevent overlapping of items on the same sheet
    for s in range(n_sheets):
        for i in range(n_items):
            for j in range(i + 1, n_items):
                no_overlap = model.NewBoolVar(f'no_overlap_{i}_{j}_{s}')
                model.Add(x[(i, s)] + item_width[(i, s)] <=
                          x[(j, s)]).OnlyEnforceIf(no_overlap)
                model.Add(x[(j, s)] + item_width[(j, s)] <=
                          x[(i, s)]).OnlyEnforceIf(no_overlap.Not())
                model.Add(y[(i, s)] + item_height[(i, s)] <=
                          y[(j, s)]).OnlyEnforceIf(no_overlap)
                model.Add(y[(j, s)] + item_height[(j, s)] <=
                          y[(i, s)]).OnlyEnforceIf(no_overlap.Not())
                model.AddBoolAnd(
                    [assigned_sheet[(i, s)], assigned_sheet[(j, s)]]).OnlyEnforceIf(no_overlap)

    # Ensure an item is placed only on a used sheet
    for s in range(n_sheets):
        for i in range(n_items):
            model.Add(assigned_sheet[(i, s)] <= used_sheet[s])

    # Objective: Minimize the total number of sheets used
    model.Minimize(sum(used_sheet))

    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True  # Enable search progress log
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        for s in range(n_sheets):
            if solver.Value(used_sheet[s]):
                print(f"Sheet {s + 1}:")
                for i in range(n_items):
                    if solver.Value(assigned_sheet[(i, s)]):
                        print(f"  Item {i + 1} at ({solver.Value(x[(i, s)])}, {solver.Value(y[(i, s)])}), "
                              f"rotated: {solver.Value(rotated[(i, s)])}")
    else:
        print("No solution found.")
        print("Debug: Ensure constraints are not overly restrictive.")


# Example data
items = [
    (1, 6), (2, 8), (6, 5), (4, 9), (8, 7),
    (2, 8), (7, 5), (3, 1), (1, 4), (2, 2),
    (9, 5), (2, 1), (1, 4), (5, 6), (6, 6),
    (2, 6), (5, 4), (1, 6), (8, 8), (5, 3)
]

sheets = [
    (20, 20), (10, 30), (10, 10), (20, 30), (10, 20), (10, 40)
]

solve_2d_cutting(items, sheets)
