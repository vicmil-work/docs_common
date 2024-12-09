import pathlib, os

def get_directory(file_path: str):
    return str(pathlib.Path(file_path).parents[0].resolve()).replace("\\", "/")


# Config
DOCS_DIRECTORY = get_directory(__file__) + "/my-docs-folder"


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


def go_to_url(url: str):
    import webbrowser
    webbrowser.open(url, new=0, autoraise=True)


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


# Usage
#if not os.path.exists("my-new-docs"):
#    mkdocs_new("my-new-docs")
os.chdir(DOCS_DIRECTORY)
go_to_url("http://127.0.0.1:8000")
build_mkdocs_documentation()
serve_mkdocs_project()
