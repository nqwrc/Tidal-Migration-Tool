import subprocess
import sys


def build():
    script_path = "tidal_migrator_gui.py"  # Path to your main Python script
    output_name = "tidal_migrator_0.1.1"
    
    # Command to run PyInstaller
    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--windowed",
        "--name", output_name,
        script_path,
    ]

    # Execute the command
    subprocess.run(command, check=True)

if __name__ == "__main__":
    build()
