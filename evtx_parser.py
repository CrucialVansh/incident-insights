import json
from typing import List
from evtx import PyEvtxParser
import typer
from typing_extensions import Annotated
from flatten_json import flatten
import sys
import csv
import io

app = typer.Typer(help="Parse EVTX files")


def output_format(parser: List, delimiter: str, output_path: io.TextIOWrapper):
    writer = csv.writer(output_path, delimiter=delimiter)
    header = False
    for records in parser:
        records["data"] = json.loads(records["data"])
        if not header:
            writer.writerow(flatten(records).keys())
            header = True
        writer.writerow(flatten(records).values())


def output_json(parser: List, output_path: io.TextIOWrapper):
    for records in parser:
        records["data"] = json.loads(records["data"])
        output_path.write(json.dumps(records) + "\n")


def filter_by_ID(parser: List[int], id: int) -> dict:
    out = []
    for records in parser:
        if records["event_record_id"] in id:
            out.append(records)
    return out


@app.command()
def print_evtx_file(
    evtx_file_path: Annotated[str, typer.Argument(help="Path to the evtx file")],
    output_path: Annotated[
        str, typer.Option("-o", help="Output path of parsed evtx")
    ] = None,
    event_id: Annotated[
        str,
        typer.Option(
            "-i", help="specify event_records_ids delimited by a space. E.g. 78 50 30"
        ),
    ] = None,
    delimiter: Annotated[
        str,
        typer.Option("-d", help="display evtx in rows and columns by given delimter"),
    ] = None,
):

    parser = PyEvtxParser(str(evtx_file_path))

    if output_path is None:
        output_path = sys.stdout
    else:
        output_path = open(output_path, "w")

    parser = parser.records_json()

    if event_id is not None:
        event_id = [int(item) for item in event_id.split()]
        print(type(event_id))
        parser = filter_by_ID(list(parser), event_id)
    if delimiter is not None:
        output_format(list(parser), delimiter, output_path)
    else:
        output_json(list(parser), output_path)

    if output_path is not sys.stdout:
        output_path.close()


if __name__ == "__main__":
    app()
