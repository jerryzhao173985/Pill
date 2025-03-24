#!/usr/bin/python3

import sys
import interp
import pickle
import marshal
import types
import os
library = "mytech"
layermap_file = "mytech.layermap"

print("Creating specialized mock environment for shapes experiment...")

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
            "library": library,
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
            "library": library,
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

# Register our procedures in the mock Skill module
def register_procedures(skill_module):
    # Add all methods as procedures for Skill interpreter to use
    for name in dir(skill_module):
        if not name.startswith('_'):  # Skip internal methods
            attr = getattr(skill_module, name)
            if callable(attr):
                skill_module.procedures[name] = attr

# Replace the global skill module with our mock
interp.skill = ShapesMockSkillModule()
register_procedures(interp.skill)

# Run the script if a file is provided
if len(sys.argv) > 1:
    script_file = sys.argv[1]
    print(f"\n=== Running script {script_file} ===")
    
    try:
        # Load and run the Skill script
        result = interp.load(script_file)
        print(f"Script execution result: {result}")
    except Exception as e:
        print(f"Error running script: {e}")
        import traceback
        traceback.print_exc()
    
    # Print a summary of all cells
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
    
    print("=== Script execution complete ===")
else:
    print("No script file specified. Usage: python shapes_mock.py <script_file>") 