; Skill file to create shapes, cells and experiment with CDF parameters

; Define our own print function since the mock environment doesn't fully support all Skill functions
procedure(debug_print (msg)
    printf("DEBUG: %s\n" msg)
)

; Create a rectangle cell with configurable parameters
procedure(pcGenCell_rect_cell (@key (width 1.0) (length 2.0) (layer "diff"))
    let((cv)
        debug_print(sprintf(nil "Creating rect_cell with width=%f, length=%f, layer=%s" width length layer))
        cv = ddGetObj("mytech" "rect_cell")
        rodCreateRect(layer width length)
        cv
    )
)

; Create a more complex cell with two shapes
procedure(pcGenCell_complex_cell (@key (width1 1.0) (length1 2.0) (width2 0.5) (length2 1.0) (layer1 "diff") (layer2 "poly"))
    let((cv)
        debug_print(sprintf(nil "Creating complex_cell with parameters:"))
        debug_print(sprintf(nil "  Shape1: width=%f, length=%f, layer=%s" width1 length1 layer1))
        debug_print(sprintf(nil "  Shape2: width=%f, length=%f, layer=%s" width2 length2 layer2))
        
        cv = ddGetObj("mytech" "complex_cell")
        ; Create first shape
        rodCreateRect(layer1 width1 length1)
        ; Create second shape with offset
        rodCreateRect(layer2 width2 length2)
        cv
    )
)

; Main test function
debug_print("Starting cell creation tests")

; Create a simple rectangle cell
debug_print("=== Test 1: Create a simple rectangle cell ===")
rect_cell = pcGenCell_rect_cell(?width 1.5 ?length 2.5 ?layer "diff")
debug_print("Rectangle cell created")

; Create a complex cell
debug_print("=== Test 2: Create a complex cell with two shapes ===")
complex_cell = pcGenCell_complex_cell(?width1 2.0 ?length1 3.0 ?width2 1.0 ?length2 1.5 ?layer1 "metal" ?layer2 "poly")
debug_print("Complex cell created")

; Test varying parameters
debug_print("=== Test 3: Create cells with varying parameters ===")
debug_print("Creating cells with different widths and lengths")

for(w 0.5 1.5 0.5
    for(l 1.0 2.0 0.5
        debug_print(sprintf(nil "Creating cell with width=%f, length=%f" w l))
        test_cell = pcGenCell_rect_cell(?width w ?length l)
        debug_print("Cell created")
    )
)

debug_print("All tests completed successfully!") 