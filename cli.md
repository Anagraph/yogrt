# `yogrt`

**Usage**:

```console
$ yogrt [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `init`: Welcome to yogrt! You can initialize template...
* `run`: Welcome to yogrt! After configuring your YAML...

## `yogrt init`

Welcome to yogrt!
You can initialize template files used for the run command with:
yogrt init --target-directory <your directory>

**Usage**:

```console
$ yogrt init [OPTIONS]
```

**Options**:

* `--target-directory TEXT`: The path where the YAML files will be initialized.
* `--help`: Show this message and exit.

## `yogrt run`

Welcome to yogrt!
After configuring your YAML profile and source file, you can download and import your sources with:
yogrt run --profile <profile.yaml> --sources <sources.yaml> --secrets <secrets.yaml>

**Usage**:

```console
$ yogrt run [OPTIONS]
```

**Options**:

* `--profile TEXT`: The path to the profile yogrt profile.
* `--sources TEXT`: The path to the sources file.
* `--secrets TEXT`: The path to the secrets file.
* `--force-download / --no-force-download`: Force download of the sources if already present.  [default: False]
* `--help`: Show this message and exit.
