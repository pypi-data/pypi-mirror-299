import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("-o", "--output", required=True, help="Output path for the new project")
def create(output):
    """Create a new project scaffold."""
    click.echo(f"Creating project at {output}")
    # Implement your scaffolding logic here


if __name__ == "__main__":
    cli()
