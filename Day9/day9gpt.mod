# Sets and Parameters
set ITEMS;                   # Set of item IDs
param width{ITEMS};          # Width of each item
param height{ITEMS};         # Height of each item

set SHEETS;                  # Fixed set of available sheets
param sheet_width{SHEETS};   # Width of each sheet
param sheet_height{SHEETS};  # Height of each sheet

set PAIRS := {ITEMS, ITEMS};  # Pairs of items to check for overlap

# Variables
var use_sheet{SHEETS} binary;     # 1 if a sheet type is used, 0 otherwise
var x1{i in ITEMS, s in SHEETS} >= 0, <= sheet_width[s];  # Bottom-left x-coordinate
var y1{i in ITEMS, s in SHEETS} >= 0, <= sheet_height[s]; # Bottom-left y-coordinate
var placed{i in ITEMS, s in SHEETS} binary;  # 1 if an item is placed on a sheet

# Objective: Minimize the total number of sheets used
minimize TotalSheetsUsed: 
    sum{s in SHEETS} use_sheet[s];

# Constraints
# Ensure each item is placed exactly once
subject to ItemPlacement{i in ITEMS}: 
    sum{s in SHEETS} placed[i, s] = 1;

# Respect sheet dimensions
subject to SheetDimensionX{i in ITEMS, s in SHEETS}:
    x1[i, s]  <= (sheet_width[s] - width[i]) * placed[i, s];

subject to SheetDimensionY{i in ITEMS, s in SHEETS}:
    y1[i, s] <= (sheet_height[s] - height[i]) * placed[i, s];

# Prevent overlap of items on the same sheet using logical conditions
subject to NoOverlap{s in SHEETS, (i, j) in PAIRS: i < j}:
    (placed[i, s] or placed[j, s])  ==>
    (x1[i, s] + width[i] <= x1[j, s] or
     x1[j, s] + width[j] <= x1[i, s] or
     y1[i, s] + height[i] <= y1[j, s] or
     y1[j, s] + height[j] <= y1[i, s]);

/*# Link sheet usage to item placement
subject to LinkSheetUsage{s in SHEETS}: 
    use_sheet[s] >= max{i in ITEMS} placed[i, s];
*/
# Ensure items are only placed on used sheets
subject to SheetPlacementConstraint{i in ITEMS, s in SHEETS}:
    placed[i, s] <= use_sheet[s];