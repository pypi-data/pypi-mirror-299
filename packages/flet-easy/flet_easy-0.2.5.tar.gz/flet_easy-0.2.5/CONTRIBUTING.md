# Contributing to Flet-Easy

First off, thanks for taking the time to contribute! Contributions include but are not restricted to:

* Reporting bugs
* Contributing to code
* Writing tests
* Writing documentation

The following is a set of guidelines for contributing.

## 1. Install uv

For more information [here](https://github.com/astral-sh/uv).

```bash
pip install uv
```

## 2. Clone repository

```bash
git clone https://github.com/Jviduz/flet-easy.git
```

## 3. Maintain dependencies to initialize the project

Install all dependencies and create a runtime environment for python automatically.

```bash
uv sync --all-extras
```

## 4. Code formatting and check

If you make some changes in the src/ and you want to preview the result of the code if it is optimal, just do it:

> [!NOTE]
> It is recommended to install the following extensions to get errors immediately in the code.
>
> * [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
> * [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)

* **Format code**

```bash
uv run ruff run format
```

* **Check code**

```bash
uv run ruff run check
```

## 5. Preview the documentation

If you make some changes to the docs/ and you want to preview the build result, simply do:

```bash
uv run mkdocs serve
```

## 6. Create a Pull Request

Once you have reviewed step 4 you can make the pull request with a detailed description of the new integrations or changes made to the code, with images or videos demonstrating what the code does if possible.
