import typer
from rich import print
import os

from yogrt import yogrt_run, yogrt_init

app = typer.Typer()


@app.command()
def init(target_directory: str = typer.Option(None,  help="The path where the YAML files will be initialized.")):
    """Welcome to yogrt!
    You can initialize template files used for the run command with:
    yogrt init --target-directory <your directory>"""
    print(f"Initializing new profile, sources, and secret file in {target_directory}")
    yogrt_init(profile_path=os.path.join(target_directory, "profile.yaml"),
               sources_path=os.path.join(target_directory, "sources.yaml"),
               secrets_path=os.path.join(target_directory, "secrets.yaml")),
    return


@app.command()
def run(profile: str = typer.Option(None, help="The path to the profile yogrt profile."),
        sources: str = typer.Option(None, help="The path to the sources file."),
        secrets: str = typer.Option(None, help="The path to the secrets file.")):
    """Welcome to yogrt!
    After configuring your YAML profile and source file, you can download and import your sources with:
    yogrt run --profile <profile.yaml> --sources <sources.yaml> --secrets <secrets.yaml>"""

    if profile is None:
        print('Oops, did you specify the --profile parameter?')
        return

    if secrets is None:
        print('Oops, did you specify the --secrets parameter?')
        return

    if sources is None:
        print('Oops, did you specify the --sources parameter?')
        return

    if not os.path.exists(profile):
        print('Oops, the profile file does not exist. Did you specify the right filepath?')
        return

    if not os.path.exists(sources):
        print('Oops, the sources file does not exist. Did you specify the right filepath?')
        return

    if os.path.splitext(profile)[1] not in ['.yaml', '.yml']:
        print('Oops, the profile file is not a YAML file. Did you specify the right filepath?')
        return

    if os.path.splitext(sources)[1] not in ['.yaml', '.yml']:
        print('Oops, the sources file is not a YAML file. Did you specify the right filepath?')
        return

    print("[green] Running yogrt... [/green]")
    yogrt_run(profile, sources, secrets)
    print("[green] Successfully imported data with yogrt! [/green] ")


if __name__ == '__main__':
    app()
