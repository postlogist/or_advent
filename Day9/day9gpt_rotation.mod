# Sets and Parameters
set ITEMS;                   # Set of item IDs
param width{ITEMS};          # Width of each item
param height{ITEMS};         # Height of each item

set SHEETS;                  # Fixed set of available sheets
param sheet_width{SHEETS};   # Width of each sheet
param sheet_height{SHEETS};  # Height of each sheet

set PAIRS := {ITEMS, ITEMS};  # Pairs of items to check for overlap

# Variables
var use_sheet{SHEETS} binary;     # 1 if a sheet is used, 0 otherwise
var x1{i in ITEMS, s in SHEETS} >= 0, <= sheet_width[s];  # Bottom-left x-coordinate
var y1{i in ITEMS, s in SHEETS} >= 0, <= sheet_height[s]; # Bottom-left y-coordinate
var x2{i in ITEMS, s in SHEETS} >= 0, <= sheet_width[s];  # Top-Right x-coordinate
var y2{i in ITEMS, s in SHEETS} >= 0, <= sheet_height[s]; # Top-Right y-coordinate

var placed{i in ITEMS, s in SHEETS} binary;  # 1 if an item is placed on a sheet
var rotated{i in ITEMS, s in SHEETS} binary; # 1 if an item is rotated on a sheet

/*
# Objective: Minimize the total number of sheets used
minimize TotalSheetsUsed: 
    sum{s in SHEETS} use_sheet[s];
*/

# Objective: Minimize the total number of sheets used
minimize TotalSheetsAreaUsed: 
    sum{s in SHEETS} use_sheet[s] * sheet_width[s] * sheet_height[s];

# Constraints
# Ensure each item is placed exactly once
subject to ItemPlacement{i in ITEMS}: 
    sum{s in SHEETS} placed[i, s] = 1;


# Define rotation logic for x2 and y2
subject to RotateCoordinates{i in ITEMS, s in SHEETS}:
    x2[i, s] = x1[i, s] + (1 - rotated[i, s]) * width[i] + rotated[i, s] * height[i];

subject to RotateDimensions{i in ITEMS, s in SHEETS}:
    y2[i, s] = y1[i, s] + (1 - rotated[i, s]) * height[i] + rotated[i, s] * width[i];

# Respect sheet dimensions with rotation
subject to SheetDimensionX{i in ITEMS, s in SHEETS}:
    placed[i, s] ==> 
    (x2[i, s] <= sheet_width[s] and y2[i, s] <= sheet_height[s]);

/*
subject to SheetDimensionY{i in ITEMS, s in SHEETS}:
    y2[i, s] <= sheet_height[s] * placed[i, s];
*/
# Prevent overlap of items on the same sheet using logical conditions
subject to NoOverlap{s in SHEETS, (i, j) in PAIRS: i < j}:
/*
    placed[i, s] and placed[j, s] == 1 ==>
    (
        x2[i, s] <= x1[j, s] or
        x2[j, s] <= x1[i, s] or
        y2[i, s] <= y1[j, s] or
        y2[j, s] <= y1[i, s]
    );
*/
    placed[i, s] and placed[j, s] == 1 ==>
    (
        x2[i, s] <= x1[j, s] or
        x2[j, s] <= x1[i, s] or
        y2[i, s] <= y1[j, s] or
        y2[j, s] <= y1[i, s]
    )
    and
    (
        i < j ==> x1[i, s] <= x1[j, s]  # Symmetry breaking: предмет i располагается "левее" или "ниже" предмета j
    );

# Ensure items are only placed on used sheets

subject to SheetPlacementConstraint{i in ITEMS, s in SHEETS}:
    placed[i, s] <= use_sheet[s];

/*
subject to PlaceThenUse{s in SHEETS}:
    sum {i in ITEMS} placed[i, s] <= use_sheet[s] * card(ITEMS);
*/