import sys
import os

def read_file(file_path):
    """Reads and prints the content of a text file."""
    try:
        with open(file_path, "r") as file:
            content = file.read()
            print("File Content:\n")
            print(content)
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    # Check if a file was passed as an argument
    if len(sys.argv) > 1:
        file_to_open = sys.argv[1]
        if os.path.exists(file_to_open):
            print(f"Opening file: {file_to_open}")
            read_file(file_to_open)
        else:
            print("Error: The file does not exist.")
    else:
        print("No file specified. Drag and drop a file onto this script or use 'Open With' to pass a file.")