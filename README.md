# Uplink

A narrow REST server that lets the judy container act on the host



[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/karshosphere/template-python)

## Setup

### Requirements

* Add system requirements here

### Build

```bash
$ make build
```

### Run

```bash
$ uv run main
```



## Testing

### Run all tests

```bash
$ make test
```

### Formatting

```bash
$ make format           # format in place
$ make format-dry-run   # list files that need formatting
```



## Documentation

* [Project Structure](docs/project_structure.md): repository layout and module responsibilities




## Release

`make release` builds a wheel and an sdist into `dist/`. They install on any platform with Python 3.13.



## Copier Update

The project uses [Copier](https://copier.readthedocs.io/en/stable/) to manage its template. When the template is updated, the project can be easily brought up to date by running the following command from the project root:

```bash
$ copier update --defaults --answers-file .copier-py-answers.yml
```
When the `--defaults` option is used, copier update skips all previously answered questions and prompts only for newly introduced ones.

