import os
import yaml
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.progress import track
from rich.console import Console

app = typer.Typer()
console = Console()


def create_structure(base_path, structure, verbose=False, force=False):
    for item in structure:
        if isinstance(item, dict):
            for key, value in item.items():
                path = os.path.join(base_path, key)
                if verbose:
                    typer.echo(f"\nProcessing: {path}")

                if isinstance(value, list):
                    if not os.path.exists(path) or force:
                        os.makedirs(path, exist_ok=True)
                        create_structure(path, value, verbose, force)
                    else:
                        typer.echo(f"\nDirectory already exists: {path}")
                        # Check for files and subdirectories within this directory
                        create_structure(path, value, verbose, force)
                else:
                    if not os.path.exists(path) or force:
                        if verbose:
                            typer.echo(f"\nCreating file: {path}")
                        with open(path, 'w') as f:
                            f.write(value)
                    else:
                        typer.echo(f"\nFile already exists: {path}")
        else:
            path = os.path.join(base_path, item)
            if not os.path.exists(path) or force:
                if verbose:
                    typer.echo(f"\nCreating file: {path}")
                with open(path, 'w') as f:
                    f.write('')
            else:
                typer.echo(f"\nFile already exists: {path}")


def create_project(config_file: str, output_dir: str = "", verbose: bool = False, force: bool = False, parent: bool = False):
    if not config_file:
        config_file = 'smith.yaml'
        if not os.path.exists(config_file):
            typer.echo(f"\nConfig file '{config_file}' not found.")
            config_file = typer.prompt("Please enter the path to the config file")
            if not os.path.exists(config_file):
                typer.echo(f"\nConfig file '{config_file}' not found. Exiting.")
                raise typer.Exit(code=1)

    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    project_name = config.get('project_name', 'MyProject')
    structure = config.get('structure', [])

    if output_dir:
        project_name = os.path.join(output_dir, project_name)

    if parent:
        if not os.path.exists(project_name) or force:
            if os.path.exists(project_name) and force:
                typer.echo(f"\nRemoving existing project directory: {project_name}")
                import shutil
                shutil.rmtree(project_name)

            os.makedirs(project_name)
    else:
        project_name = output_dir

    # Use track to show progress bar
    for item in track(structure, description="Creating structure"):
        create_structure(project_name, [item], verbose, force)

    typer.echo(f"\nProject '{project_name}' created successfully.")


def detect_structure(base_path):
    structure = []
    for root, dirs, files in os.walk(base_path):
        relative_path = os.path.relpath(root, base_path)
        if relative_path == '.':
            relative_path = ''

        # Remove hidden directories and directories starting with underscore
        dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]

        if relative_path:
            current_level = structure
            for part in relative_path.split(os.sep):
                for item in current_level:
                    if isinstance(item, dict) and part in item:
                        current_level = item[part]
                        break
                else:
                    new_dict = {part: []}
                    current_level.append(new_dict)
                    current_level = new_dict[part]

        for f in files:
            if not f.startswith('.'):
                if relative_path:
                    current_level.append(f)
                else:
                    structure.append(f)

    return structure


def convert_structure(structure):
    converted = []
    for item in structure:
        if isinstance(item, dict):
            converted.append({list(item.keys())[0]: convert_structure(list(item.values())[0])})
        else:
            converted.append(item)
    return converted

# CLI COMMANDS
@app.command()
def create(config_file: str = typer.Argument(None, help="Config file"),
           output_dir: str = typer.Option("", "--output", "-o", help="Output directory"),
           verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose mode"),
           force: bool = typer.Option(False, "--force", "-f", help="Force overwrite existing project"),
           parent: bool = typer.Option(False, "--parent", "-p", help="Create the parent folder")):
    """
    Create a new project based on the configuration file.

    This command reads the configuration file and creates the project structure in the specified output directory.
    """
    create_project(config_file, output_dir, verbose, force, parent)


@app.command()
def delete(paths: list[str]):
    """
    Delete specified paths.

    This command deletes the specified files or directories.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Deleting paths...", total=len(paths))
        for path in paths:
            if os.path.exists(path):
                if os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                    typer.echo(f"\nDeleted directory: {path}")
                else:
                    os.remove(path)
                    typer.echo(f"\nDeleted file: {path}")
            else:
                typer.echo(f"\nPath does not exist: {path}")
            progress.update(task, advance=1)
        progress.stop()
        typer.echo("\nDeletion complete")


@app.command()
def rename(src: str, dest: str):
    """
    Rename a file or directory.

    This command renames the specified source path to the destination path.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Renaming...", total=1)
        if os.path.exists(src):
            os.rename(src, dest)
            typer.echo(f"\nRenamed {src} to {dest}")
        else:
            typer.echo(f"\nSource path does not exist: {src}")
        progress.update(task, advance=1)
        progress.stop()
        typer.echo("\nRename complete")


@app.command()
def move(paths: list[str], dest: str):
    """
    Move files or directories to a specified destination.

    This command moves the specified paths to the destination directory.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Moving paths...", total=len(paths))
        for path in paths:
            if os.path.exists(path):
                dest_path = os.path.join(dest, os.path.basename(path))
                os.rename(path, dest_path)
                typer.echo(f"\nMoved {path} to {dest_path}")
            else:
                typer.echo(f"\nPath does not exist: {path}")
            progress.update(task, advance=1)
        progress.stop()
        typer.echo("\nMove complete")


@app.command()
def add(paths: list[str]):
    """
    Add new files or directories.

    This command creates the specified files or directories if they do not already exist.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Adding paths...", total=len(paths))
        for path in paths:
            if not os.path.exists(path):
                if path.endswith(os.sep) or not os.path.splitext(path)[1]:
                    # Create a directory
                    os.makedirs(path, exist_ok=True)
                    typer.echo(f"\nCreated directory: {path}")
                else:
                    # Create a file
                    with open(path, 'w') as f:
                        f.write('')
                    typer.echo(f"\nCreated file: {path}")
            else:
                typer.echo(f"\nPath already exists: {path}")
            progress.update(task, advance=1)
        progress.stop()
        typer.echo("\nAddition complete")


@app.command()
def sync(config_file: str = typer.Option("", "--config", "-c", help="Config file to write the structure to"),
         project_dir: str = typer.Option(".", "--dir", "-d", help="Project directory to detect structure from")):
    """
    Sync the project structure with a configuration file.

    This command detects the structure of the project directory and writes it to the specified configuration file.
    """
    if not config_file:
        config_file = 'smith.yaml'

    project_name = os.path.basename(os.path.abspath(project_dir))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Syncing structure...", total=1)
        structure = detect_structure(project_dir)
        converted_structure = convert_structure(structure)
        progress.update(task, advance=1)

    config = {
        'project_name': project_name,
        'structure': converted_structure
    }

    with open(config_file, 'w') as file:
        yaml.safe_dump(config, file)

    typer.echo(f"\nStructure synced with '{config_file}' successfully.")

@app.command()
def view(path: str):
    """
    View the contents of a directory or check if a file exists.

    This command lists the contents of the specified directory or checks if the specified file exists.
    """
    if os.path.isdir(path):
        if not os.listdir(path):
            typer.echo(f"\nThe directory '{path}' has no files.")
        else:
            typer.echo(f"\nContents of directory '{path}':")
            for root, dirs, files in os.walk(path):
                level = root.replace(path, '').count(os.sep)
                indent = ' ' * 4 * (level)
                typer.echo(f"\n * {indent}{os.path.basename(root)}/")
                subindent = ' ' * 4 * (level + 1)
                for file in files:
                    typer.echo(f" - {subindent}{file}")
    elif os.path.isfile(path):
        typer.echo(f"\nThe file '{path}' exists.")
    else:
        typer.echo(f"\nThe path '{path}' does not exist.")


@app.command()
def version():
    """
    Display the version of smithIt.

    This command displays the version of the smithIt tool.
    """
    typer.echo("\nsmithIt version 0.1")


if __name__ == "__main__":
    app()