import json
from pathlib import Path
from evtx import PyEvtxParser

def print_evtx_file(evtx_file_path: Path, output_path=None, save_file=False):
    """
    Parses an EVTX file and extracts event data and either prints it to stdout or an output_path

    Args:
        evtx_file_path: The path to the .evtx file.
        save_file: Boolean for conditional file save
        output_path: The Path to save the parsed .evtx file

    Returns:
        Prints or writes json for evtx file
    """
    parser = PyEvtxParser(str(evtx_file_path))
    if not save_file:
        for records in parser.records_json():
            print(str(records) + "\n") 
    else:
        for records in parser.records_json():
            with open(output_path, "w") as file:
                file.write(str(records) + "\n")



if __name__ == "__main__":
    # Replace with the actual path to your .evtx file
    evtx_file = Path("/home/vanshp/", "Security.evtx") 
    if evtx_file.exists():
        out = "./jeff.json"
        print_evtx_file(evtx_file)
    else:
        print(f"Error: EVTX file not found at {evtx_file}")
