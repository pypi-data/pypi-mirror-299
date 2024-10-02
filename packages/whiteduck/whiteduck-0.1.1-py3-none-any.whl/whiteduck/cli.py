import click
import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Path to the directory containing templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-o",
    "--output",
    default=".",
    type=click.Path(),
    help="Output path for the new project (defaults to current directory)",
)
@click.option(
    "-t",
    "--template",
    default="default",
    required=True,
    help="Name of the template to use",
)
def create(output, template):
    """Create a new project scaffold."""
    try:
        create_project(output, template)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


@cli.command()
def list_templates():
    """List available templates."""
    templates = get_available_templates()
    if templates:
        click.echo("Available templates:")
        for tmpl in templates:
            click.echo(f"- {tmpl}")
    else:
        click.echo("No templates found.")


@cli.command()
@click.argument("template")
def template_info(template):
    """Display information about a template."""
    readme_path = os.path.join(TEMPLATES_DIR, template, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            click.echo(f.read())
    else:
        click.echo(f"No README.md found for template '{template}'")


def get_available_templates():
    if os.path.exists(TEMPLATES_DIR):
        return [
            name
            for name in os.listdir(TEMPLATES_DIR)
            if os.path.isdir(os.path.join(TEMPLATES_DIR, name))
        ]
    return []


def create_project(output_path, template_name):
    logging.info(f"Creating project at {output_path} using template '{template_name}'")

    template_path = os.path.join(TEMPLATES_DIR, template_name)

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template '{template_name}' not found.")

    shutil.copytree(template_path, output_path, dirs_exist_ok=True)
    logging.info("Project scaffold created successfully.")


if __name__ == "__main__":
    cli()
