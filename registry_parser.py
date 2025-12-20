import typer
from Registry import Registry
from typing_extensions import Annotated
from typing import Dict
import pdb
import json

app = typer.Typer(help="Parse Windows Registry files incluing NTUSER.DAT")


def rec(key: Registry.RegistryKey, out: Dict):
    if len(key.values()) != 0:
        for value in key.values():
            if not isinstance(value.value(), bytes) :
                out["value"] = {"name": value.name(), "type": value.value_type_str(), "value": value.value()}
            else:
                out["value"] = {"name": value.name(), "type": value.value_type_str(), "valueAsString": value.value().hex()}
                
    if len(key.subkeys()) == 0:
        return out
    for subkey in key.subkeys():
        out[subkey.name()] = {}
        rec(subkey, out[subkey.name()])


@app.command()
def print_registry_file(
    registry_file_path: Annotated[str, typer.Argument(help="Path to registry file")],
    is_json: Annotated[bool, typer.Option("-j")] = False
):
    reg = Registry.Registry(registry_file_path)
    out = {}
    rec(reg.root(), out)
    if is_json:
        print(json.dumps(out))
    else:
        print(out)


if __name__ == "__main__":
    app()
