# aoc2024 by @dhennessy

Advent of Code: 2024

- **GitHub Repository**: <https://github.com/dhennessy/aoc2024/>

## Getting Started

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:dhennessy/aoc2024.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to solving Advent of Code, in style!

Tip: If you're using devcontainers, just execute `code .` and you're good to go. :)

## Project Structure

Within your project folder (aoc2024/aoc2024), you've got a python file for each day you need to solve, such as `01.py`, as well as a corresponding input file, such as `input/01.txt`. You can update the code to solve the puzzle, and put your input in the text file as per Advent of Code (feel free to skip checking it in).

You've also got the following:

- `aoc2024/aoc2024/runner.py`: The CLI; check it out for arguments, or execute the project with `-h`.
- `aoc2024/aoc2024/utils.py`: A utilities file to get you started, but feel free to flesh it out. :)

## Executing the CLI

If you're in the devcontainer:

```
python -m aoc2024
```

If you're outside of the devcontainer:

```
uv run python -m aoc2024
```

## Attribution

Repository initialized with [lskillen/cookiecutter-py-aoc](https://github.com/lskillen/cookiecutter-py-aoc), for a rockin' around the tree good time, developing Advent of Code solutions using Python+uv+ruff+mypy+pytest. Come and get your own; yes, you.
