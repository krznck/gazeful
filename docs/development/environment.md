# Environment Setup

The following page outlines how to set up Gazeful.

- Python 3.10 is required.
- Dependencies are listed in [requirements.txt](https://github.com/krznck/gazeful/blob/main/requirements.txt).
- Using a virtual environment is recommended.

## 1. Clone the Repository

The code can be found at our [GitHub repository](https://github.com/krznck/gazeful).

```bash
git clone git@github.com:krznck/gazeful.git
cd gazeful
```

### 2. Create a Virtual Environment

All platforms:

```bash
python -m venv .venv
```

## 3. Activate the Virtual Environment
<!-- markdownlint-disable MD046 -->

=== "Linux / macOS (BASH or Zsh)"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows (PowerShell)"

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

    > If PowerShell blocks activation, you may need to run:
    >
    > ```powershell
    > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    > ```

=== "Windows (Command Prompt)"

    ```cmd
    .venv\Scripts\activate.bat
    ```

<!-- markdownlint-enable MD046 -->
## 4. Install Dependencies

All platforms:

```bash
pip install --requirement requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

For installation instructions, refer to
[Getting Started](../getting_started.md).

## Development Tools

The following are a list of tools meant to be used when contributing to Gazeful.

- [ruff](https://github.com/astral-sh/ruff/):
  A Python linter and code formatter.
  In Gazeful, it is used for style formatting and docstring linting.
  The repository provides a
  [configuration file](https://github.com/krznck/gazeful/blob/main/ruff.toml)
  for ruff.

- [isort](https://pypi.org/project/isort/):
  A utility to sort Python imports alphabetically.

- [markdownlint](https://github.com/DavidAnson/markdownlint):
  A style checker and lint tool for Markdown files.

- [pyright](https://github.com/microsoft/pyright):
  A static type checker for Python.
