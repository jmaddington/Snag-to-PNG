#!/usr/bin/env python3

import sys
import argparse
import glob
import os

def extract_png_from_snagx(snagx_file, output_png_file=None):
    # PNG file signatures
    start_signature = b'\x89PNG\r\n\x1a\n'  # Standard PNG file header
    end_signature = b'IEND\xaeB`\x82'       # Standard PNG file trailer

    try:
        with open(snagx_file, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{snagx_file}' not found.", file=sys.stderr)
        return False

    # Find the start index of the PNG data
    start_index = data.find(start_signature)
    if start_index == -1:
        print(f"Could not find PNG start signature in file '{snagx_file}'.", file=sys.stderr)
        return False

    # Find the end index of the PNG data
    end_index = data.find(end_signature, start_index)
    if end_index == -1:
        print(f"Could not find PNG end signature in file '{snagx_file}'.", file=sys.stderr)
        return False

    # Include the length of the end signature to capture the complete PNG data
    end_index += len(end_signature)

    # Extract the PNG data
    png_data = data[start_index:end_index]

    # Determine the output filename if not provided
    if not output_png_file:
        base_name = os.path.splitext(snagx_file)[0]
        output_png_file = f"{base_name}.png"

    # Save the extracted PNG data to a file
    try:
        with open(output_png_file, 'wb') as f:
            f.write(png_data)
        print(f"PNG image extracted and saved to '{output_png_file}'.")
        return True
    except IOError as e:
        print(f"Error writing to file '{output_png_file}': {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Extract PNG images from .snagx files.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'input_files', nargs='+',
        help='Path to input .snagx files (supports wildcards, e.g., "*.snagx").'
    )
    parser.add_argument(
        '-o', '--output',
        help='Path to the output PNG file (if processing a single file).'
    )
    args = parser.parse_args()

    input_files = []
    for pattern in args.input_files:
        matched_files = glob.glob(pattern)
        if not matched_files:
            print(f"No files matched the pattern '{pattern}'.", file=sys.stderr)
            continue
        input_files.extend(matched_files)

    if not input_files:
        print("No input files to process.", file=sys.stderr)
        sys.exit(1)

    if args.output and len(input_files) > 1:
        print("Error: Cannot specify a single output file when processing multiple input files.", file=sys.stderr)
        sys.exit(1)

    success_count = 0
    for input_file in input_files:
        output_file = args.output if args.output else None
        result = extract_png_from_snagx(input_file, output_file)
        if result:
            success_count += 1

    print(f"Processed {len(input_files)} file(s), successfully extracted {success_count} PNG image(s).")

if __name__ == '__main__':
    main()