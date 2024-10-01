To upload to pypi:

- Ensure build and twine installed
- check .pypirc file in home dir has access token
- update package name in pyproject.toml
- pythoon -m build
- twine upload dist/*