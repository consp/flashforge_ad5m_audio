#!/bin/bash
cp pyproject.toml.template pyproject.toml
sed -i 's/PROJECT_NAME/ff-ad5m-audio/g' pyproject.toml
python3 -m build
cp pyproject.toml.template pyproject.toml
sed -i 's/PROJECT_NAME/ff-adm5-audio/g' pyproject.toml
python3 -m build
python3 -m twine upload --repository pypi dist/*
