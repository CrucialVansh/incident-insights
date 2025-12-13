import typer
from Registry import Registry
from typing_extensions import Annotated

app = typer.Typer(help="Parse Windows Registry files incluing NTUSER.DAT")


def rec(key, depth=0):
    print("\t" * depth + key.path())

    for subkey in key.subkeys():
        rec(subkey, depth + 1)

@app.command()
def print_registry_file(registry_file_path: Annotated[str, typer.Argument(help="Path to registry file")]):
    reg = Registry.Registry(registry_file_path)
    rec(reg.root())


if __name__ == "__main__":
    app()