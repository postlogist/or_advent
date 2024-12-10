% Sets and Parameters
int: n_items;                        % Number of items
int: n_sheets;                       % Number of sheets
array[1..n_items] of int: widths;    % Width of each item
array[1..n_items] of int: heights;   % Height of each item
array[1..n_sheets] of int: sheet_widths;   % Widths of sheets
array[1..n_sheets] of int: sheet_heights;  % Heights of sheets

% Decision Variables
array[1..n_items] of var 1..n_sheets: item_sheet; % Sheet assignment for each item
array[1..n_items] of var 0..max(sheet_widths): x; % x-coordinates of items
array[1..n_items] of var 0..max(sheet_heights): y; % y-coordinates of items
array[1..n_items] of var bool: rotated;           % Rotation flag for each item
array[1..n_sheets] of var bool: used_sheets;      % Whether a sheet is used

% Derived Variables
array[1..n_items] of var 0..max(sheet_widths): w; % Effective widths of items
array[1..n_items] of var 0..max(sheet_heights): h; % Effective heights of items


% Constraints
% Rotation logic for width
constraint forall(i in 1..n_items) (
 
  w[i] = (if rotated[i] then heights[i] else widths[i]));
 

% Rotation logic for height
constraint forall(i in 1..n_items) (
  h[i] = (if rotated[i] then widths[i] else heights[i])
);







% Ensure each item is placed exactly once
constraint
  forall(i in 1..n_items) (
    item_sheet[i] >= 1 /\ item_sheet[i] <= n_sheets
  );

% Ensure all items fit within their assigned sheet
constraint
  forall(i in 1..n_items) (
    x[i] + w[i] <= sheet_widths[item_sheet[i]] /\
    y[i] + h[i] <= sheet_heights[item_sheet[i]]
  );

% No-overlap constraint on each sheet using diffn
constraint
  forall(s in 1..n_sheets) (
    let {
      set of int: items_on_sheet = {i | i in 1..n_items where item_sheet[i] == s}
    } in
      diffn(
        [x[i] | i in items_on_sheet],
        [y[i] | i in items_on_sheet],
        [w[i] | i in items_on_sheet],
        [h[i] | i in items_on_sheet]
      )
  );

% Ensure an item is placed only on a used sheet
constraint
  forall(i in 1..n_items) (
    used_sheets[item_sheet[i]] = true
  );

% Ensure at least one sheet is used if any items are placed on it
constraint
  forall(s in 1..n_sheets) (
    used_sheets[s] = exists(i in 1..n_items)(item_sheet[i] == s)
  );


% Objective: Minimize the total area of used sheets
solve minimize sum(s in 1..n_sheets)(used_sheets[s] * sheet_widths[s] * sheet_heights[s]);