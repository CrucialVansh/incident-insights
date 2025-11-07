import click

@click.group()
def cli():
    pass

@cli.command()
@click.option("--source", required=True, help="Path to evidence directory")
def parse(source):
    click.echo(f"Parsing artefacts from {source}...")

if __name__ == "__main__":
    cli()
