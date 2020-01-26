# Course Manager

A CLI application to manage university projects and assignments. Command line parsing uses library [click](https://github.com/pallets/click).

### Usage (Development)

Ensure you are in a virtualenv and install the package
```sh
source venv/bin/activate
pip install --editable .
```

To run the script
```sh
cm <args>
```

Alternatively, simply run the package by
```sh
python -m course_manager <args>
```

For more info about click and setuptools, check out [this page](https://click.palletsprojects.com/en/7.x/setuptools/).
