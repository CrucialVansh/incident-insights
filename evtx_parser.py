import json
from evtx import PyEvtxParser
import typer
from typing_extensions import Annotated
from flatten_json import flatten
import pandas as pd
import sys

app = typer.Typer(help="Parse EVTX files")


# Print as JSONL
# Print Specific ID
# Print as CSV or TSV

# takes very long -> Find fix
def output_format(parser: PyEvtxParser, delimitter: str, file=sys.stdout, id=None):
    new = pd.DataFrame()
    for records in parser.records_json():
        if id is not None and records["event_record_id"] == int(id):
            r = flatten(records)
            new = pd.concat([new, pd.DataFrame(r, index=r.keys())])
            break
        elif id is not None:
            pass
        else:
            records["data"] = json.loads(records["data"])
            r = flatten(records)
            new = pd.concat([new, pd.DataFrame(r, index=r.keys())])
    new.to_csv(file, sep=delimitter, index=False)


@app.command("show")
def print_evtx_file(
    evtx_file_path: Annotated[str, typer.Argument(help="Path to the evtx file")],
    output_path: Annotated[
        str, typer.Option("-o", help="Output path of parsed evtx")
    ] = None,
    event_id: Annotated[
        str, typer.Option("-id", help="specify event_records_id")
    ] = None,
    delimiter: Annotated[
        str,
        typer.Option("-d", help="display evtx in rows and columns by given delimter"),
    ] = None,
):
    """
    Parses an EVTX file and extracts event data and either prints it to stdout or an output path

    Args:
        evtx_file_path: The path to the .evtx file\n
        output_path: The Path to save the parsed .evtx file\n

    Returns:
        Prints or writes json for evtx file
    """

    parser = PyEvtxParser(str(evtx_file_path))
    
    if output_path is None:
        if delimiter is not None:
            output_format(parser, delimiter, id=event_id)
        else:
            for records in parser.records_json():
                records["data"] = json.loads(records["data"])
                if event_id is not None and records["event_record_id"] == int(event_id):
                    print(json.dumps(records))
                    break
                elif event_id is None:
                    print(json.dumps(records))

    else:
        if delimiter is not None and output_path is not None:
            output_format(parser, delimiter, file=output_path, event_id=event_id)
        else:
            for records in parser.records_json():
                records["data"] = json.loads(records["data"])
                with open(output_path, "w", encoding="utf-8") as file:
                    if event_id is not None and records["event_record_id"] == int(event_id):
                        file.write(json.dumps(records))
                        break
                    elif event_id is None:
                        file.write(json.dumps(records))
    





if __name__ == "__main__":
    app()
