import click
import os

from yogrt import yogrt_run, yogrt_init


@click.command()
@click.option("--init", is_flag=True, show_default=True, default=False,
              help="Initialize a new profile and sources file.")
@click.option('--profile', default=None, help='The path to the profile yogrt profile.')
@click.option('--sources', default=None, help='The path to the sources file.')
@click.option('--secrets', default=None, help='The path to the secrets file.')
def main(init, profile, sources, secrets):
    """Welcome to yogrt!
    After configuring your YAML profile and source file, you can download and import your sources with:
    yogrt run --profile profile.yaml --sources sources.yaml --secrets secrets.yaml"""

    if init:
        click.echo("Initializing new profile and sources file.")
        yogrt_init()
        return

    if profile is None:
        click.echo('Oops, did you specify the --profile parameter?')
        return

    if secrets is None:
        click.echo('Oops, did you specify the --secrets parameter?')
        return

    if sources is None:
        click.echo('Oops, did you specify the --sources parameter?')
        return

    if not os.path.exists(profile):
        click.echo('Oops, the profile file does not exist. Did you specify the right filepath?')
        return

    if not os.path.exists(sources):
        click.echo('Oops, the sources file does not exist. Did you specify the right filepath?')
        return

    if os.path.splitext(profile)[1] not in ['.yaml', '.yml']:
        click.echo('Oops, the profile file is not a YAML file. Did you specify the right filepath?')
        return

    if os.path.splitext(sources)[1] not in ['.yaml', '.yml']:
        click.echo('Oops, the sources file is not a YAML file. Did you specify the right filepath?')
        return

    click.echo("Running yogrt...")
    yogrt_run(profile, sources, secrets)
    click.echo("Done.")


if __name__ == '__main__':
    main()
