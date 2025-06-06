import subprocess
import sys
import os

# Get the absolute paths to the scripts
base_dir = os.path.dirname(os.path.abspath(__file__))
main_py = os.path.join(base_dir, 'main.py')
main2_py = os.path.join(base_dir, 'main_2.py')

# Function to run a script in a new terminal window

def run_in_new_terminal(script_path, title):
    # For Windows PowerShell
    subprocess.Popen([
        'start', 'powershell', '-NoExit', '-Command', f'python "{script_path}"'
    ], shell=True)

if __name__ == "__main__":
    run_in_new_terminal(main_py, 'Main Script')
    run_in_new_terminal(main2_py, 'Main 2 Script')
    print("Both scripts have been started in separate terminals.")
