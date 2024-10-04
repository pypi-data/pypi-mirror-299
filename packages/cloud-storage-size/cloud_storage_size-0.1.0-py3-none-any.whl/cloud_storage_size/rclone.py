"""
https://github.com/Johannes11833/rclone_python/blob/master/rclone_python/rclone.py
"""
import os
import platform
import subprocess
import zipfile
import urllib.request

from functools import wraps
from shutil import which, move, rmtree


def ensure_path_includes_local_bin():
    """
    Ensure that ~/.local/bin is in the PATH environment variable.
    If it's not, add it and update the .bashrc or .bash_profile file.
    """
    home = os.path.expanduser("~")
    local_bin = os.path.join(home, ".local", "bin")

    # Check if ~/.local/bin exists
    if not os.path.exists(local_bin):
        os.makedirs(local_bin, exist_ok=True)

    # Check if ~/.local/bin is in PATH
    if local_bin not in os.environ["PATH"].split(os.pathsep):
        # Add to PATH for the current session
        os.environ["PATH"] = f"{local_bin}:{os.environ['PATH']}"


def __install_rclone():
    """
    Install rclone on the system, location: ~/.local/bin
    This function works for Unix-like systems (Linux/macOS).
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system not in ['linux', 'darwin']:
        raise NotImplementedError(f"Automatic installation not supported for {system}")

    # Determine the appropriate rclone download URL
    if system == 'linux':
        os_name = 'linux'
    else:  # darwin (macOS)
        os_name = 'osx'

    if 'arm' in machine or 'aarch64' in machine:
        arch = 'arm64'
    else:
        arch = 'amd64'

    url = f"https://downloads.rclone.org/rclone-current-{os_name}-{arch}.zip"

    # Create ~/.local/bin if it doesn't exist
    install_dir = os.path.expanduser("~/.local/bin")
    os.makedirs(install_dir, exist_ok=True)

    # Download rclone
    print("Downloading rclone...")
    filename, _ = urllib.request.urlretrieve(url)

    # Extract the zip file
    print("Extracting rclone...")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(install_dir)

    # Move the rclone binary to ~/.local/bin
    extracted_dir = os.path.join(install_dir, f"rclone-*-{os_name}-{arch}")
    extracted_dirs = [d for d in os.listdir(install_dir) if d.startswith("rclone-")]
    if extracted_dirs:
        extracted_dir = os.path.join(install_dir, extracted_dirs[0])
        move(os.path.join(extracted_dir, "rclone"), os.path.join(install_dir, "rclone"))

        # Clean up
        rmtree(extracted_dir)

    # Clean up
    os.remove(filename)

    # Make rclone executable
    os.chmod(os.path.join(install_dir, "rclone"), 0o755)

    # Ensure ~/.local/bin is in PATH
    ensure_path_includes_local_bin()

    print(f"rclone has been installed to {install_dir}")
    print("~/.local/bin has been added to your PATH if it wasn't already there.")
    print("Please restart your terminal or run 'source ~/.bashrc' for the changes to take effect.")


def is_installed() -> bool:
    """
    :return: True if rclone is correctly installed on the system.
    """
    return which("rclone") is not None


def __check_installed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_installed():
            __install_rclone()
        return func(*args, **kwargs)

    return wrapper


@__check_installed
def ls(remote: str, flags: str = "") -> str:
    """
    List the contents of a remote.
    :param remote: The remote to list.
    :param flags: Additional flags to pass to the rclone command.
    :return: The output of the rclone command.
    """
    command = f"rclone ls {remote} {flags}"
    return subprocess.run(command, shell=True, check=True, capture_output=True, text=True).stdout
