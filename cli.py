import typer
import evtx_parser
import registry_parser

# The main application
app = typer.Typer(help="DFIR Forensic Artifact Parser")

# Mount the sub-apps
app.add_typer(evtx_parser.app, name="evtx")
app.add_typer(registry_parser.app, name="reg")

if __name__ == "__main__":
    app()