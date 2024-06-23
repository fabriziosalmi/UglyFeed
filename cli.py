import subprocess
import os

def main():
    # Determine the path to `gui.py`
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gui_path = os.path.join(current_dir, 'gui.py')
    
    # Check if gui.py exists
    if not os.path.isfile(gui_path):
        print(f"Error: gui.py not found in {current_dir}")
        return

    # Start the Streamlit server
    command = ["streamlit", "run", gui_path, "--server.address", "0.0.0.0"]
    subprocess.run(command)

if __name__ == "__main__":
    main()
