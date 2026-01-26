import json
from typing import List, Generator, Optional
from evtx import PyEvtxParser
import typer
from typing_extensions import Annotated
from flatten_json import flatten
import sys
import csv
import io
from dateutil import parser as date_parser
from datetime import timezone

app = typer.Typer(help="Parse EVTX files")


def output_format(parser: List, delimiter: str, output_path: io.TextIOWrapper):
    writer = csv.writer(output_path, delimiter=delimiter)
    for records in parser:
        records["data"] = json.loads(records["data"])
        writer.writerow(flatten(records).values())


def output_json(parser: List, output_path: io.TextIOWrapper):
    for records in parser:
        records["data"] = json.loads(records["data"])
        output_path.write(json.dumps(records) + "\n")


def filter_by_ID(parser: List, id: List[int]):
    for records in parser:
        if records["event_record_id"] in id:
            yield records



def filter_by_time(parser: Generator, start_time: Optional[str], end_time: Optional[str]):
    start_dt = None
    if start_time:
        start_dt = date_parser.parse(start_time)
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=timezone.utc)

    end_dt = None
    if end_time:
        end_dt = date_parser.parse(end_time)
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=timezone.utc)

    for records in parser:
        record_dt = date_parser.parse(records["timestamp"])
        if start_dt and record_dt < start_dt:
            continue
        
        if end_dt and record_dt > end_dt:
            continue
        yield records

@app.command("parse")
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
    after: Annotated[str, typer.Option("--after", help="Start time (e.g. 2021-01-01)")] = None,
    before: Annotated[str, typer.Option("--before", help="End time (e.g. 2021-01-30)")] = None,
):

    parser = PyEvtxParser(str(evtx_file_path))

    if output_path is None:
        output_path = sys.stdout
    else:
        output_path = open(output_path, "w")

    parser = parser.records_json()


    if event_id is not None:
        event_id = [int(item) for item in event_id.split()]
        parser = filter_by_ID(parser, event_id)
    if after is not None or before is not None:
        parser = filter_by_time(parser, after, before)
    if delimiter is not None:
        output_format(parser, delimiter, output_path)
    else:
        output_json(parser, output_path)

    if output_path is not sys.stdout:
        output_path.close()


if __name__ == "__main__":
    app()
