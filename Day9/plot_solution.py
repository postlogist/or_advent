import re
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def read_solution_file(file_path):
    sheets = {}
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(
                r"Item (\d+) \(item size (\d+)x(\d+)\) placed on sheet (\d+) \(sheet size (\d+)x(\d+)\), at \((\d+), (\d+)\), rotated: (\d+)",
                line
            )
            if match:
                item_id = int(match.group(1))
                item_width = int(match.group(2))
                item_height = int(match.group(3))
                sheet_id = int(match.group(4))
                sheet_width = int(match.group(5))
                sheet_height = int(match.group(6))
                x = int(match.group(7))
                y = int(match.group(8))
                rotated = int(match.group(9))

                if sheet_id not in sheets:
                    sheets[sheet_id] = {
                        "width": sheet_width,
                        "height": sheet_height,
                        "items": []
                    }

                sheets[sheet_id]["items"].append({
                    "id": item_id,
                    "width": item_width if rotated == 0 else item_height,
                    "height": item_height if rotated == 0 else item_width,
                    "x": x,
                    "y": y,
                    "rotated": rotated
                })
    return sheets


def plot_sheets(sheets, output_file="solution_diagram.png"):
    fig, axes = plt.subplots(len(sheets), 1, figsize=(10, 5 * len(sheets)))
    if len(sheets) == 1:
        axes = [axes]  # Ensure axes is iterable for a single sheet

    for ax, (sheet_id, sheet) in zip(axes, sheets.items()):
        ax.set_xlim(0, sheet["width"])
        ax.set_ylim(0, sheet["height"])
        ax.set_aspect('equal')
        ax.set_title(f"Sheet {sheet_id} ({sheet['width']}x{sheet['height']})")
        ax.set_xlabel("Width")
        ax.set_ylabel("Height")

        # Add sheet rectangle
        ax.add_patch(
            patches.Rectangle(
                (0, 0), sheet["width"], sheet["height"],
                edgecolor="black", fill=False, linewidth=2
            )
        )

        # Add items
        for item in sheet["items"]:
            # Red for rotated items
            color = "red" if item["rotated"] == 1 else "blue"
            ax.add_patch(
                patches.Rectangle(
                    (item["x"], item["y"]),
                    item["width"], item["height"],
                    edgecolor="black", facecolor=color, alpha=0.6
                )
            )
            ax.text(
                item["x"] + item["width"] / 2, item["y"] + item["height"] / 2,
                f"{item['id']}", ha="center", va="center", fontsize=10, color="white"
            )

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)  # Save the diagram to a PNG file
    plt.show()


os.chdir('Day9')

# Path to the solution file
file_path = "solution.txt"

# Read and process the solution file
sheets_data = read_solution_file(file_path)

# Plot the sheets and item placements, and save as PNG
plot_sheets(sheets_data, output_file="solution_diagram.png")
