import pathlib
import os
import platform

def get_directory(file_path: str):
    return str(pathlib.Path(file_path).parents[0].resolve()).replace("\\", "/")


def python_virtual_environment(env_directory_path):
    # Setup a python virtual environmet
    os.makedirs(env_directory_path, exist_ok=True) # Ensure directory exists
    my_os = platform.system()
    if my_os == "Windows":
        os.system(f'python -m venv "{env_directory_path}"')
    else:
        os.system(f'python3 -m venv "{env_directory_path}"')


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


virtual_env_path = get_directory(__file__) + "/env"

python_virtual_environment(virtual_env_path)
pip_install_packages_in_virtual_environment(
    env_directory_path=virtual_env_path,
    packages=["mkdocs", "mkdocs-material", "pymdown-extensions"]
)
