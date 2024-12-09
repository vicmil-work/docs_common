# Using MKDocs for documentation

You can either just copy the parts that you find interesting, or download the following:

- [setup_docs.py](../static/setup_docs.py){:download="setup_docs.py"} - Install the necessary pip packages in a virtual environment in ./env
- [view_docs.py](../static/view_docs.py){:download="view_docs.py"} - Display the documentation in a browser window

### Install

```
pip install mkdocs, mkdocs-material, pymdown-extensions
```

### MKDocs new project

```python
def mkdocs_new(project_name):
    from mkdocs.utils import write_file
    # Create the project directory and docs directory
    os.makedirs(os.path.join(project_name, "docs"), exist_ok=True)

    # Write default mkdocs.yml file
    config_content = "site_name: My Docs\n"
    write_file(config_content.encode('utf-8'), os.path.join(project_name, "mkdocs.yml"))

    # Write default index.md file
    index_content = "# Welcome to MkDocs\n\nThis is your homepage!"
    write_file(index_content.encode('utf-8'), os.path.join(project_name, "docs", "index.md"))

    print(f"New MkDocs project created in: {project_name}")

mkdocs_new("my-new_project")
```

### MKDocs serve project

Makes it so you can view the project in the browser if you navigate to "http://127.0.0.1:8000"

```python
def serve_mkdocs_project(config_file="mkdocs.yml", host="127.0.0.1", port=8000):
    """
    Serve an MkDocs project locally.

    Args:
        config_file (str): Path to the mkdocs.yml configuration file.
        host (str): Host address to bind the server (default: 127.0.0.1).
        port (int): Port number to serve the site (default: 8000).
    """
    from mkdocs.commands.serve import serve
    try:
        # Start the MkDocs development server directly with the configuration file
        print(f"Serving MkDocs at http://{host}:{port}")
        serve(config_file, host=host, port=port, livereload=True, watch_theme=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
```

### Go to url

Opens the webbrowser with the provided url

```python
def go_to_url(url: str):
    import webbrowser
    webbrowser.open(url, new=0, autoraise=True)
```

### Mkdocs launch example

```python
# Setup virtual environment and install everything necessary
virtual_env_path = vicmil_pysetup.get_directory(__file__) + "/env"

vicmil_pysetup.python_virtual_environment(virtual_env_path)
vicmil_pysetup.pip_install_packages_in_virtual_environment(
    env_directory_path=virtual_env_path,
    packages=["mkdocs", "mkdocs-material", "pymdown-extensions"]
)
```

```python
# Create new docs project, and show it in the webbrowser
mkdocs_new("my-new-docs")
vicmil_pysetup.set_active_directory("my-new-docs")
go_to_url("http://127.0.0.1:8000")
serve_mkdocs_project()
```

### Build MKdocs

Builds it into html files that can be hosted as a server

```python
def build_mkdocs_documentation(config_file="mkdocs.yml", output_dir=None):
    from mkdocs.config import load_config
    from mkdocs.commands.build import build
    """
    Build MkDocs documentation into a static site.

    Args:
        config_file (str): Path to the mkdocs.yml configuration file.
        output_dir (str): Optional. Path to the output directory for the built site.
    """
    # Load the MkDocs configuration
    config = load_config(config_file)
  
    # Set a custom output directory if provided
    if output_dir:
        config['site_dir'] = os.path.abspath(output_dir)
  
    try:
        print(f"Building documentation using config: {config_file}")
        build(config)
        print(f"Documentation successfully built in: {config['site_dir']}")
    except Exception as e:
        print(f"Error while building documentation: {e}")

```

### Start a python server in the current directory

```
python -m http.server
```

### Example for building and running documentation

```python
set_active_directory(get_directory(__file__) + "/docs_common")
go_to_url("http://127.0.0.1:8000")
build_mkdocs_documentation()
set_active_directory(get_directory(__file__) + "/docs_common/site")
try:
    os.system("python3 -m http.server")
except Exception as e:
    pass

os.system("python -m http.server")
```
