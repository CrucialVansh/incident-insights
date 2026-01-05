import typer
from Registry import Registry
from typing_extensions import Annotated
from typing import Dict
import json
import sys
import io

app = typer.Typer(help="Parse Windows Registry files incluing NTUSER.DAT")


def rec(key: Registry.RegistryKey, out: io.TextIOWrapper):

    current_key_data = {
        "path": key.path(),
        "timestamp": key.timestamp().isoformat(),
        "values": []
    }

    
    for value in key.values():
            data = value.value()
            
            item = {
                "name": value.name(),
                "type": value.value_type_str()
            }

            if isinstance(data, bytes):
                item["valueAsString"] = data.hex()
            else:
                item["value"] = data
                
            current_key_data["values"].append(item)
                
    out.write(json.dumps(current_key_data) + "\n")

    for subkey in key.subkeys():
        rec(subkey, out)




@app.command()
def print_registry_file(
    registry_file_path: Annotated[str, typer.Argument(help="Path to registry file")],
    output_path: Annotated[str, typer.Option("-o")] = None,
    csv_out: Annotated[bool, typer.Option("-c")] = False
):
    reg = Registry.Registry(registry_file_path)

    if output_path is None:
        output_path = sys.stdout
    else:
        output_path = open(output_path, 'w')
    
    rec(reg.root())


    if output_path is not sys.stdout:
        output_path.close()
    


if __name__ == "__main__":
    app()


