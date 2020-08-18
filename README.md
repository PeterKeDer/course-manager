# Course Manager

A CLI application to manage university projects and assignments. Command line parsing uses library [click](https://github.com/pallets/click).

### Usage (Development)

📦 Ensure that `virtualenv` is installed on your system. Create a new virtual environment by running:
```sh
virtualenv env
```

Activate the environment and install the packages:
```sh
source env/bin/activate
pip3 install --editable .
```

🏃 To run the script
```sh
cm <args>
```

🏃 Alternatively, simply run the package by
```sh
python3 -m course_manager <args>
```

For more info about click and setuptools, check out [this page](https://click.palletsprojects.com/en/7.x/setuptools/).
