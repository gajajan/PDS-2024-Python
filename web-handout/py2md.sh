#!/bin/bash

# Check if input and output directories are provided
if [ $# -ne 2 ]; then
  echo "Usage: $0 <input_directory> <output_directory>"
  exit 1
fi

INPUT_DIR=$1
OUTPUT_DIR=$2

# Check if input directory exists
if [ ! -d "$INPUT_DIR" ]; then
  echo "Error: Input directory '$INPUT_DIR' does not exist."
  exit 1
fi

# Create output directory if it does not exist
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
  echo "Created output directory '$OUTPUT_DIR'."
fi

# Clear the output directory
rm -rf "$OUTPUT_DIR"/*

# Traverse through each file in the input directory recursively
find "$INPUT_DIR" -type f | while read -r file; do
  # Extract the relative path of the file
  relative_path="${file#$INPUT_DIR/}"
  
  # Construct the output path, preserving subdirectory structure
  output_path="$OUTPUT_DIR/$relative_path.md"
  
  # Ensure the output subdirectory exists
  mkdir -p "$(dirname "$output_path")"
  
  # Write the content to the new file
  {
    echo "---"
    echo "layout: code"
    echo "title: $(basename "$file")"
    echo "---"
    echo ""
    echo "\`\`\`python"
    cat "$file"
    echo "\`\`\`"
  } > "$output_path"
  
  echo "Processed $file -> $output_path"
done
