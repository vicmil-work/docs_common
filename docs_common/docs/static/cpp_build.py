from typing import List
import platform
import pathlib
import os

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


class BuildSetup:
    def __init__(self, cpp_file_paths: List[str], output_dir: str = path_traverse_up(__file__, 0) + "/bin", deps_dir: str = path_traverse_up(__file__, 0) + "/deps", browser = False):
        # When building c++ projects, this is in general the order the flags should be
        self.n1_compiler_path = get_default_compiler_path(browser = browser)
        self.n2_cpp_files = '"' + '" "'.join(cpp_file_paths) + '"'
        self.n3_optimization_level = ""
        self.n4_macros = ""
        self.n5_additional_compiler_settings = ""
        self.n6_include_paths = ""
        self.n7_library_paths = ""
        self.n8_library_files = ""
        self.n9_output_file = output_dir + "/" + get_default_output_file(browser=browser)

        # If the target platform is the browser
        self.browser_flag = browser

        # Where to find dependencies
        self.deps_dir = deps_dir

    def include_opengl(self): # Opengl is a cross platform graphics library that also works in the browser(with the right setup)
        add_opengl_flags(self, self.browser_flag)

    def enable_debug(self):
        self.n4_macros += " -D USE_DEBUG"

    def include_asio(self): # Asio is a cross platform networking library to work with sockets etc.
        add_asio_flags(self, browser=self.browser_flag)

    def generate_build_command(self):
        arguments = [
            self.n1_compiler_path, 
            self.n2_cpp_files,
            self.n3_optimization_level,
            self.n4_macros,
            self.n5_additional_compiler_settings,
            self.n6_include_paths,
            self.n7_library_paths,
            self.n8_library_files,
            "-o " + '"' + self.n9_output_file + '"',
        ]

        # Reomve arguments with length 0
        arguments = filter(lambda arg: len(arg) > 0, arguments)

        return " ".join(arguments)


    def build_and_run(self):
        build_command = self.generate_build_command()

        # Remove the output file if it exists already
        if os.path.exists(self.n9_output_file):
            os.remove(self.n9_output_file)

        # Run the build command
        print(build_command)
        run_command(build_command)

        invoke_file(self.n9_output_file)


def get_default_output_file(browser = False):
    platform_name = platform.system()

    if not browser:
        if platform_name == "Windows": # Windows
            return "run.exe"

        elif platform_name == "Linux": # Linux
            return "run.out"

        else:
            raise NotImplementedError()
        
    else:
        return "run.html"


def run_command(command: str) -> None:
    """Run a command in the terminal"""
    platform_name = platform.system()
    if platform_name == "Windows": # Windows
        if command[0] != '"':
            os.system(f'powershell; {command}')
        else:
            os.system(f'powershell; &{command}')
    else:
        os.system(command)


def invoke_file(file_path: str):
    if not os.path.exists(file_path=file_path):
        print(file_path + " does not exist")

    file_extension = file_path.split(".")[-1]

    if file_extension == "html":
        # Create a local python server and open the file in the browser
        launch_html_page(file_path)

    elif file_extension == "exe" or file_extension == "out":
        # Navigate to where the file is located and invoke the file
        file_directory = path_traverse_up(file_path, 0)
        os.chdir(file_directory) # Change active directory
        run_command('"' + file_path + '"')


def launch_html_page(html_file_path: str):
    import webbrowser
    """ Start the webbrowser if not already open and launch the html page

    Parameters
    ----------
        html_file_path (str): The path to the html file that should be shown in the browser

    Returns
    -------
        None
    """
    os.chdir(path_traverse_up(html_file_path, count=0))
    if not (os.path.exists(html_file_path)):
        print("html file does not exist!")
        return
    
    file_name: str = html_file_path.replace("\\", "/").rsplit("/", maxsplit=1)[-1]
    webbrowser.open("http://localhost:8000/" + file_name, new=0, autoraise=True)

    try:
        run_command("python3 -m http.server")
    except Exception as e:
        pass

    run_command("python -m http.server")


# Get the defualt compiler path within vicmil lib
def get_default_compiler_path(deps_dir: str, browser = False):
    platform_name = platform.system()

    if not browser:
        if platform_name == "Windows": # Windows
            return '"' + deps_dir + "/mingw64/bin/g++" + '"'
        else:
            return "g++"

    else:
        if platform_name == "Windows": # Windows
            return '"' + deps_dir + "/emsdk/upstream/emscripten/em++.bat" + '"'
        else:
            return '"' + deps_dir + "/emsdk/upstream/emscripten/em++" + '"'


def add_opengl_flags(build_setup: BuildSetup, browser = False):
    if not browser:
        platform_name = platform.system()

        if platform_name == "Windows": # Windows
            dependencies_directory = build_setup.deps_dir

            # SDL
            build_setup.n6_include_paths += ' -I"' + dependencies_directory + "/sdl_mingw/SDL2-2.30.7/x86_64-w64-mingw32/include/SDL2" + '"'
            build_setup.n6_include_paths += ' -I"' + dependencies_directory + "/sdl_mingw/SDL2-2.30.7/x86_64-w64-mingw32/include" + '"'
            build_setup.n7_library_paths += ' -L"' + dependencies_directory + "/sdl_mingw/SDL2-2.30.7/x86_64-w64-mingw32/lib" + '"'

            # SDL_image
            build_setup.n6_include_paths += ' -I"' + dependencies_directory + "/sdl_mingw/SDL2_image-2.8.2/x86_64-w64-mingw32/include" + '"'
            build_setup.n7_library_paths += ' -L"' + dependencies_directory + "/sdl_mingw/SDL2_image-2.8.2/x86_64-w64-mingw32/lib" + '"'

            # Glew
            build_setup.n6_include_paths += ' -I"' + dependencies_directory + "/glew-2.2.0/include" + '"'
            build_setup.n7_library_paths += ' -L"' + dependencies_directory + "/glew-2.2.0/lib/Release/x64" + '"'

            build_setup.n8_library_files += ' -l' + "mingw32"
            build_setup.n8_library_files += ' -l' + "glew32"
            build_setup.n8_library_files += ' -l' + "opengl32"
            build_setup.n8_library_files += ' -l' + "SDL2main"
            build_setup.n8_library_files += ' -l' + "SDL2"
            build_setup.n8_library_files += ' -l' + "SDL2_image"

        elif platform_name == "Linux": # Linux
            build_setup.n6_include_paths += ' -I' + "/usr/include"

            build_setup.n8_library_files += ' -l' + "SDL2"
            build_setup.n8_library_files += ' -l' + "SDL2_image"
            build_setup.n8_library_files += ' -l' + "GL"  #(Used for OpenGL on desktops)
            build_setup.n8_library_files += ' -l' + "SDL2_image"

        else:
            raise NotImplementedError()

    else:
        build_setup.n5_additional_compiler_settings += " -s USE_SDL=2"
        build_setup.n5_additional_compiler_settings += " -s USE_SDL_IMAGE=2"
        build_setup.n5_additional_compiler_settings += " -s EXTRA_EXPORTED_RUNTIME_METHODS=ccall,cwrap"
        # build_setup.n5_additional_compiler_settings += """ -s SDL2_IMAGE_FORMATS='["png"]'"""
        build_setup.n5_additional_compiler_settings += " -s FULL_ES3=1"


# Asio is used for sockets and network programming
def add_asio_flags(build_setup: BuildSetup, browser = False):
    if browser:
        raise Exception("Asio is not supported for the browser, consider using websockets bindings to javascript(TODO)")

    build_setup.n6_include_paths += ' -I"' + build_setup.deps_dir + "/asio/include" + '"'

    platform_name = platform.system()
    if platform_name == "Windows": # Windows
        build_setup.n8_library_files += " -lws2_32" # Needed to make it compile with mingw compiler

    else:
        print("asio include not implemented for ", platform_name)