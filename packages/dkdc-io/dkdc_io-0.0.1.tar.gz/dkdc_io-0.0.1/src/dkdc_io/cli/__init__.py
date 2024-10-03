# imports
import typer

# typer config
## default kwargs
default_kwargs = {
    "no_args_is_help": True,
    "add_completion": False,
    "context_settings": {"help_option_names": ["-h", "--help"]},
}

## main app
app = typer.Typer(help="dkdc-io", **default_kwargs)


@app.command()
@app.command("server", hidden=True)
def server():
    """
    server
    """
    from dkdc_io.server import run_server

    run_server()


# main
if __name__ == "__main__":
    typer.run(app)
