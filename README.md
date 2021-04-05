# Chess

A desktop application which can be used for playing chess, storing past games and viewing them move-by-move.

## Documentation

[Requirements specification](documentation/requirements_specification.md)

[Timesheet](documentation/timesheet.md)

## Installation

Start by installing [Python](https://www.python.org/) and [Poetry](https://python-poetry.org/).

Then install the dependencies using the following command:

```console
poetry install
```

Finally, start the application using the following command:

```console
poetry run invoke start
```

## Development

Run unit tests using the following command:

```console
poetry run invoke test
```

Generate a coverage report using the following command:

```console
poetry run invoke coverage-report
```

## Attributions

> Font Awesome Free 5.15.3 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0)

_SVG icons resized, recolored and converted to PNGs (saved in `src/img/pieces`)._
