# Add current directory to import path
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[0]))

import os
from typing import List
import subprocess, threading
import platform
import time

def path_traverse_up(path: str, count: int) -> str:
    """Traverse the provided path upwards

    Parameters
    ----------
        path (str): The path to start from, tips: use __file__ to get path of the current file
        count (int): The number of directories to go upwards

    Returns
    -------
        str: The path after the traversal, eg "/some/file/path"
    """

    parents = pathlib.Path(path).parents
    path_raw = str(parents[count].resolve())
    return path_raw.replace("\\", "/")


def get_directory(file_path: str):
    return str(pathlib.Path(file_path).parents[0].resolve()).replace("\\", "/")


def set_active_directory(path):
    os.chdir(path)


def clear_file(file_path):
     with open(file_path, "w") as log_file: # Remove any previous contents
        pass


def ensure_directory_exists(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def ensure_file_exists(file_path):
    file_directory = str(pathlib.Path(file_path).parents[0].resolve()).replace("\\", "/")
    os.makedirs(file_directory, exist_ok=True) # Ensure the parent directory exists
    if not os.path.exists(file_path):
        with open(file_path, "w") as _: # Create the file
            pass


def list_files_in_directory(dir_path):
    return os.listdir(dir_path)


def set_git_ssh_key_path(ssh_key_path): # Set the ssh key for git
    if not os.path.exists(ssh_key_path):
        print("ssh key does not exist!")
        return
    else:
        print("found valid ssh key")
        os.environ["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key_path}"


def git_fetch(dir_path, ssh_key_path = None):
    """
    Checks for new updates in the specified directory be doing a git fetch
    Returns true if any updates were available, otherwise returns false
    """

    try:
        os.chdir(dir_path) # Set active directory
        if ssh_key_path:
            if not os.path.exists(ssh_key_path): # Try and setup ssh key for git
                print("ssh key does not exist!")
                return
            else:
                print("found valid ssh key")
                os.environ["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key_path}"
      
        print("git fetch")
        # Fetch the latest changes
        subprocess.run(["git", "fetch"], check=True)

        # Compare local and remote branches
        status = subprocess.run(
            ["git", "rev-list", "--count", f"HEAD..origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        updates_ahead = int(status.stdout.strip())

        print("updates_ahead: ", updates_ahead)

        return updates_ahead > 0
    except Exception as e:
        print(e)
        print("could not fetch updates")


def git_pull(dir_path, ssh_key_path = None):
    """
    Performs git pull in a directory
    """
    print("Downloading updates...")
    os.chdir(dir_path) # Set active directory
    if ssh_key_path:
        if not os.path.exists(ssh_key_path): # Try and setup ssh key for git
            print("ssh key does not exist!")
            return
        else:
            print("found valid ssh key")
            os.environ["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key_path}"

    # Pull the latest changes
    os.system('git pull')


def git_clone(dir_path, git_repo, ssh_key_path = None):
    os.chdir(dir_path) # Set active directory
    if ssh_key_path:
        if not os.path.exists(ssh_key_path): # Try and setup ssh key for git
            print("ssh key does not exist!")
            return
        else:
            print("found valid ssh key")
            os.environ["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key_path}"

    os.system(f'git clone {git_repo}')


def python_virtual_environment(env_directory_path):
    # Setup a python virtual environmet
    os.makedirs(env_directory_path, exist_ok=True) # Ensure directory exists
    my_os = platform.system()
    if my_os == "Windows":
        os.system(f'python -m venv "{env_directory_path}"')
    else:
        os.system(f'python3 -m venv "{env_directory_path}"')


def pip_install_requirements_file_in_virtual_environment(env_directory_path, requirements_path):
    if not os.path.exists(env_directory_path):
        print(f"Invalid path: {env_directory_path}")
        raise Exception("Invalid path")
  
    if not os.path.exists(requirements_path):
        print(f"Invalid path: {requirements_path}")
        raise Exception("Invalid path")

    my_os = platform.system()
    if my_os == "Windows":
         os.system(f'powershell; &"{env_directory_path}/Scripts/pip" install -r "{requirements_path}"')
    else:
        os.system(f'"{env_directory_path}/bin/pip" install -r "{requirements_path}"')


def pip_install_packages_in_virtual_environment(env_directory_path, packages):
    if not os.path.exists(env_directory_path):
        print("Invalid path")
        raise Exception("Invalid path")
  
    my_os = platform.system()
    for package in packages:
        if my_os == "Windows":
            os.system(f'powershell; &"{env_directory_path}/Scripts/pip" install {package}')
        else:
            os.system(f'"{env_directory_path}/bin/pip" install {package}')


def process_is_running(p: subprocess.Popen):
    if not p:
        return False
  
    poll = p.poll()
    if poll is None:
        return True # The process is running
  
    return False


def terminate_process_and_all_its_children(p: subprocess.Popen):
    import psutil
    pid = p.pid
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)  # Get all descendants
        for child in children:
            child.terminate()  # Terminate each child process
        parent.terminate()  # Terminate the parent process

        # Wait for processes to exit
        gone, alive = psutil.wait_procs(children + [parent], timeout=5)
        for proc in alive:
            proc.kill()  # Force kill if still alive
    except psutil.NoSuchProcess:
        print(f"Process {pid} does not exist.")


def invoke_python_file_using_subprocess(python_env_path: str, file_path: str, logfile_path: str = None) -> subprocess.Popen:
    if not os.path.exists(python_env_path):
        print(f"invalid path: {python_env_path}")

    if not os.path.exists(file_path):
        print(f"invalid path: {file_path}")
      
    current_directory = str(pathlib.Path(file_path).parents[0].resolve()).replace("\\", "/")
    os.chdir(current_directory) # Set active directory to the current directory

    command = ""
    my_os = platform.system()
    if logfile_path:
        if my_os == "Windows":
            command = f'powershell; &"{python_env_path}/Scripts/python" -u "{file_path}" > "{logfile_path}"'
        else:
            command = f'"{python_env_path}/bin/python" -u "{file_path}" > "{logfile_path}"'
    else:
        if my_os == "Windows":
            command = f'powershell; &"{python_env_path}/Scripts/python" -u "{file_path}"'
        else:
            command = f'"{python_env_path}/bin/python" -u "{file_path}"'

    new_process = subprocess.Popen(command, shell=True)
    return new_process


def print_logs_loop(log_files: List[str]):
    """Continuously watch multiple log files"""
    if type(log_files) == type(str("")):
        log_files = [log_files]

    log_file_last_size = dict()
    for LOG_FILE in log_files:
        log_file_last_size[LOG_FILE] = 0

    while True:
        time.sleep(1)  # Polling interval (adjust as needed)
        for LOG_FILE in log_files:
            try:
                if os.path.exists(LOG_FILE):
                    current_size = os.path.getsize(LOG_FILE)
                    if current_size == 0:
                        log_file_last_size[LOG_FILE] = 0
                    if current_size > log_file_last_size[LOG_FILE]:  # Check if new data is added
                        with open(LOG_FILE, "r") as log_file:
                            log_file.seek(log_file_last_size[LOG_FILE])  # Start reading from last read position
                            new_logs = log_file.read()
                            log_file_last_size[LOG_FILE] = current_size
                            print(new_logs[:-1]) # skip the last endl character
            except Exception as e:
                print(f"Error reading logs: {e}")

# Print out the contents of the log files in real time
def create_log_file_tail_thread(log_files: List[str]):
    print("tail_log_files")
    return threading.Thread(target=print_logs_loop, daemon=True, args=(log_files,)).start();
