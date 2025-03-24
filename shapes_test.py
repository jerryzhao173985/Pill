#!/usr/bin/python3

import sys
import interp
import pickle
import marshal
import types
import os
import pprint

print("Creating shapes and CDF parameters experiment...")

# Create a direct Python implementation instead of parsing Skill
class ShapesMockSkillModule:
    def __init__(self):
        self.procedures = {}
        self.iprocs = {}
        self.variables = {}
        self.cells = {}
        self.cdf_params = {}
        self.varstack = {}
        
    def printf(self, fmt, *args):
        """Implement printf for debug messages"""
        print(fmt % args)
        
    def sprintf(self, nil, fmt, *args):
        """Implement sprintf for string formatting"""
        return fmt % args
        
    def pcGenCell_rect_cell(self, *args, **kwargs):
        """Generate a rectangle cell with the given parameters"""
        print("Generating rectangle cell with parameters:")
        width = kwargs.get('width', 1.0)
        length = kwargs.get('length', 2.0)
        layer = kwargs.get('layer', "diff")
        print(f"- Width: {width}")
        print(f"- Length: {length}")
        print(f"- Layer: {layer}")
        
        # Create a cell object with CDF parameters
        cell = {
            "name": "rect_cell", 
            "library": "mytech",
            "cdf_params": {
                "width": {"type": "float", "value": width},
                "length": {"type": "float", "value": length},
                "layer": {"type": "string", "value": layer}
            },
            "shapes": []
        }
        
        # Store the cell
        self.cells["rect_cell"] = cell
        
        # Create the rectangle shape in the cell
        rect = self.rodCreateRect(layer, width, length)
        cell["shapes"].append(rect)
        
        return cell
        
    def pcGenCell_complex_cell(self, *args, **kwargs):
        """Generate a complex cell with multiple shapes"""
        print("Generating complex cell with parameters:")
        width1 = kwargs.get('width1', 1.0)
        length1 = kwargs.get('length1', 2.0)
        width2 = kwargs.get('width2', 0.5)
        length2 = kwargs.get('length2', 1.0)
        layer1 = kwargs.get('layer1', "diff")
        layer2 = kwargs.get('layer2', "poly")
        
        print(f"- Shape 1: Width={width1}, Length={length1}, Layer={layer1}")
        print(f"- Shape 2: Width={width2}, Length={length2}, Layer={layer2}")
        
        # Create a cell object with CDF parameters
        cell = {
            "name": "complex_cell", 
            "library": "mytech",
            "cdf_params": {
                "width1": {"type": "float", "value": width1},
                "length1": {"type": "float", "value": length1},
                "width2": {"type": "float", "value": width2},
                "length2": {"type": "float", "value": length2},
                "layer1": {"type": "string", "value": layer1},
                "layer2": {"type": "string", "value": layer2}
            },
            "shapes": []
        }
        
        # Store the cell
        self.cells["complex_cell"] = cell
        
        # Create the rectangle shapes in the cell
        rect1 = self.rodCreateRect(layer1, width1, length1)
        rect2 = self.rodCreateRect(layer2, width2, length2)
        cell["shapes"].extend([rect1, rect2])
        
        return cell
        
    def ddGetObj(self, library, cellName):
        """Get or create a cell view"""
        print(f"Getting cell: {library}/{cellName}")
        if cellName in self.cells:
            return self.cells[cellName]
        
        # Create new cell
        cell = {
            "name": cellName,
            "library": library,
            "cdf_params": {},
            "shapes": []
        }
        self.cells[cellName] = cell
        return cell
    
    def rodCreateRect(self, layer, width, length, *args):
        """Create a rectangle with the given layer and dimensions"""
        print(f"Creating rectangle: layer={layer}, width={width}, length={length}")
        rect = {
            "type": "rect",
            "layer": layer,
            "width": width,
            "length": length,
            "bbox": [[0, 0], [width, length]]  # Simplified bounding box
        }
        return rect
        
    def debug_print(self, msg):
        """Implement debug_print function from Skill"""
        print(f"DEBUG: {msg}")

# Create our mock Skill module
skill_module = ShapesMockSkillModule()

# Replace the global skill module with our mock
interp.skill = skill_module

# Define a function to print cell summaries
def print_cell_summary():
    print("\n=== Cell Summary ===")
    for name, cell in interp.skill.cells.items():
        print(f"Cell: {name}")
        print(f"- Library: {cell['library']}")
        print(f"- CDF Parameters:")
        for param, details in cell.get('cdf_params', {}).items():
            print(f"  - {param}: {details['value']} ({details['type']})")
        print(f"- Shapes: {len(cell['shapes'])}")
        for i, shape in enumerate(cell['shapes']):
            print(f"  - Shape {i+1}: {shape['type']}, layer={shape['layer']}, dimensions={shape['width']}x{shape['length']}")
        print()

# Experiment 1: Create a simple rectangle cell
print("\n=== Experiment 1: Create a simple rectangle cell ===")
rect_cell = skill_module.pcGenCell_rect_cell(width=1.5, length=2.5, layer="diff")
print("Rectangle cell created")

# Experiment 2: Create a complex cell with two shapes
print("\n=== Experiment 2: Create a complex cell with two shapes ===")
complex_cell = skill_module.pcGenCell_complex_cell(
    width1=2.0, length1=3.0, width2=1.0, length2=1.5, layer1="metal", layer2="poly"
)
print("Complex cell created")

# Experiment 3: Test varying parameters
print("\n=== Experiment 3: Create cells with varying parameters ===")
print("Creating cells with different widths and lengths")

# Store cells in a dictionary for later reference
cells = {}
for w in [0.5, 1.0, 1.5]:
    for l in [1.0, 1.5, 2.0]:
        cell_name = f"rect_cell_w{w}_l{l}"
        print(f"Creating cell with width={w}, length={l}")
        cell = skill_module.ddGetObj("mytech", cell_name)
        rect = skill_module.rodCreateRect("diff", w, l)
        cell["shapes"].append(rect)
        
        # Add CDF parameters
        cell["cdf_params"]["width"] = {"type": "float", "value": w}
        cell["cdf_params"]["length"] = {"type": "float", "value": l}
        cells[cell_name] = cell
        print(f"Cell {cell_name} created")

# Print summary of all cells
print_cell_summary()

# Experiment 4: Modify CDF parameters of existing cells
print("\n=== Experiment 4: Modify CDF parameters of existing cells ===")

# Modify rect_cell parameters
rect_cell = interp.skill.cells["rect_cell"]
rect_cell["cdf_params"]["width"]["value"] = 2.0
print(f"Modified rect_cell width to {rect_cell['cdf_params']['width']['value']}")

# Add a new shape to the complex cell with modified parameters
complex_cell = interp.skill.cells["complex_cell"]
complex_cell["cdf_params"]["width3"] = {"type": "float", "value": 0.8}
complex_cell["cdf_params"]["length3"] = {"type": "float", "value": 0.8}
complex_cell["cdf_params"]["layer3"] = {"type": "string", "value": "via"}

# Create a new rectangle based on the new parameters
new_rect = skill_module.rodCreateRect(
    complex_cell["cdf_params"]["layer3"]["value"],
    complex_cell["cdf_params"]["width3"]["value"],
    complex_cell["cdf_params"]["length3"]["value"]
)
complex_cell["shapes"].append(new_rect)
print("Added a new shape to complex_cell with new CDF parameters")

# Print final cell summary
print_cell_summary()

print("=== Experiment completed successfully! ===") 