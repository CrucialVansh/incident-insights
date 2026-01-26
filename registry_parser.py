import typer
from Registry import Registry
from typing_extensions import Annotated
from typing import Dict
import json
import sys
import csv
import io

app = typer.Typer(help="Parse Windows Registry files incluing NTUSER.DAT")


def reg_formater(key: Registry.RegistryKey):
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
    
    return current_key_data

def rec(key: Registry.RegistryKey, out: io.TextIOWrapper):

    current_key_data = reg_formater(key)
                
    out.write(json.dumps(current_key_data) + "\n")

    for subkey in key.subkeys():
        rec(subkey, out)


def csv_rec(key: Registry.RegistryKey, out: csv):
    current_key_data = reg_formater(key)

    if len(current_key_data["values"]) >= 1:
        for item in current_key_data["values"]:
            temp = current_key_data
            temp["values"] = item
            out.writerow(temp.values())
    else:
        out.writerow(current_key_data.values())

    for subkey in key.subkeys():
        csv_rec(subkey, out)


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
    
    if not csv_out:
        rec(reg.root(), output_path)
    else:
        write = csv.writer(output_path)
        write.writerow(["Full Path", "Timestamp", "Values"])
        csv_rec(reg.root(), write)


    if output_path is not sys.stdout:
        output_path.close()
    


if __name__ == "__main__":
    app()


