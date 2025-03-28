#!/usr/bin/python3

import interp
import pickle
import marshal
import copyreg
import types
import os
library = "mytech"
layermap_file = "mytech.layermap"

print("Creating a simplified test environment...")

# Create a direct Python implementation instead of parsing Skill
class MockSkillModule:
    def __init__(self):
        self.procedures = {}
        self.iprocs = {}
        self.variables = {}
        self.cells = {}
        
    def pcGenCell_test_cell(self, *args, **kwargs):
        print("Generating test cell!")
        width = kwargs.get('width', 1.0)
        length = kwargs.get('length', 2.0)
        print(f"- Width: {width}")
        print(f"- Length: {length}")
        
        # Create a cell object
        cell = {
            "name": "test_cell", 
            "library": "mytech",
            "width": width,
            "length": length,
            "shapes": []
        }
        
        # Store the cell
        self.cells["test_cell"] = cell
        
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
            "length": length
        }
        
        # Add to the current cell if available
        if "test_cell" in self.cells:
            self.cells["test_cell"]["shapes"].append(rect)
            
        return rect

# Mock utility functions
def PushVars(*args):
    print(f"PushVars called with: {args}")
    
def PopVars(*args):
    print(f"PopVars called with: {args}")

# Replace the global skill module with our mock
interp.skill = MockSkillModule()

# Add utility functions to the global namespace
globals()["PushVars"] = PushVars
globals()["PopVars"] = PopVars

# Define entry point function that will call our function
def test_entry():
    print("\nTesting the mock Skill module")
    
    # Test getting a cell
    cell = interp.skill.ddGetObj("mytech", "test_cell")
    print(f"Got cell: {cell['name']}")
    
    # Test creating a basic shape
    rect = interp.skill.rodCreateRect("diff", 2.0, 4.0)
    print(f"Created shape: {rect}")
    
    # Test generating a cell
    result = interp.skill.pcGenCell_test_cell(width=2.5, length=3.5)
    print(f"Generated cell: {result['name']} ({result['width']}x{result['length']})")
    print(f"Cell contains {len(result['shapes'])} shapes")
    
    return result

# Execute the test
print("\n=== Running Test ===")
result = test_entry()
print("\n=== Final Cell State ===")
print(f"Cell: {result['name']}")
print(f"Dimensions: {result['width']}x{result['length']}")
print(f"Shapes: {result['shapes']}")
print("=== Test Complete ===\n")


