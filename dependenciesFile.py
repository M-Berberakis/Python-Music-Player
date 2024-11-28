import subprocess
import sys

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        print("Successfully installed/upgraded pip.")
    except subprocess.CalledProcessError:
        print("Error installing/upgrading pip.")
        sys.exit(1)

    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])
        print("Successfully installed pygame.")
    except subprocess.CalledProcessError:
        print("Error installing pygame.")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()
