# This script contains the command to compile the .ui file into Python code.
# Run this script from the root directory of the project whenever you make changes to the UI in Qt Designer.

import os
import subprocess

# --- Configuration ---
# Path to the .ui file from Qt Designer
UI_FILE = os.path.join("gui", "gui_interface.ui")
# Path to the output Python file for the UI
PY_UI_FILE = os.path.join("gui", "gui_interface.py")

# --- Commands ---
# Command to convert .ui to .py
UI_COMMAND = f"pyuic6 -x {UI_FILE} -o {PY_UI_FILE}"

def run_command(command, description):
    """Runs a command and prints its status."""
    print(f"--- {description} ---")
    print(f"Executing: {command}")
    try:
        # Using subprocess.run for better error handling
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("Success!")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(e.stderr)
    except FileNotFoundError:
        print(f"Error: The command '{command.split()[0]}' was not found.")
        print("Please ensure it is installed and in your system's PATH.")
    print("-" * (len(description) + 8))
    print()


if __name__ == "__main__":
    print("Starting UI compilation...\n")
    run_command(UI_COMMAND, "Converting .ui to .py")
    print("\nCompilation process finished.")
