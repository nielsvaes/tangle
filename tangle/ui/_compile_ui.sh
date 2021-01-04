#!/bin/bash

for FILE in *.ui; do
    [ -f "$FILE" ] || break
    COMPILED_NAME="${FILE%%.*}_ui.py"

    echo "Compiling >> $COMPILED_NAME"
    pyside2-uic $FILE -o $COMPILED_NAME
done
