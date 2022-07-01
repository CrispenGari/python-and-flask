### Python and Flask

This repository contains various flask applications examples for creating API's and Web Applications using python and flask.

<p align="center">
<img src="https://img.shields.io/static/v1?label=language&message=python&color=green"/>
<img src="https://img.shields.io/static/v1?label=language&message=javascript&color=orange"/>
<img src="https://img.shields.io/static/v1?label=language&message=typescript&color=blue"/>
<img src="https://img.shields.io/static/v1?label=language&message=htm&color=red"/>
<img src="https://img.shields.io/static/v1?label=language&message=css&color=black"/>

<img src="https://img.shields.io/static/v1?label=package&message=flask&color=blue"/>
<img src="https://img.shields.io/static/v1?label=package&message=jinja&color=yellow"/>
<img src="https://img.shields.io/static/v1?label=package&message=requests&color=green"/>
<img src="https://img.shields.io/static/v1?label=package&message=flask-rest&color=purple"/>
<img src="https://img.shields.io/static/v1?label=package&message=sql-alchamey&color=black"/>
<img src="https://img.shields.io/static/v1?label=package&message=mongodb&color=green"/>
</p>

<p align="center">
<img src="https://github.com/CrispenGari/Flask/blob/main/lnm6ybztq944ikym1s8f.jpg" alt="" width="100%">
</p>

### Creating a virtual environment

There are two ways of creating a virtual environment in python.

1. creating a virtual environment from a already exists folder.

- to create a virtual environment in the existing folder you first need to navigate to the folder that you wnt to create virtual environment by running the command:

```shell
cd myv
```

- then you run the following command to create a virtual environment

```shell
virtualenv .
```

> This just means create a virtual environment in the current directory.

2. creating a virtual environment and naming it.

- to create a virtual environment by name you run the following command:

```shell
virtualenv venv
```

### Activating virtual environment

To activate virtual environment you have to run the `activate.bat` file that will be generated in virtual environment that you have created for example:

```shell
.\venv\Scripts\activate
# or
.\venv\Scripts\activate.bat
```

> Activating the first virtual (myv) you will do it as follows:

```shell
.\Scripts\activate
# or
.\Scripts\activate.bat
```

### Deactivating virtual environment

To deactivate virtual environment you have to run the `deactivate.bat` file that will be generated in virtual environment that you have created for example:

```shell
.\venv\Scripts\deactivate
# 1.
.\venv\Scripts\deactivate.bat
```

> Activating the first virtual (myv) you will do it as follows:

```shell
.\Scripts\deactivate
# 1.
.\Scripts\deactivate.bat
```

> I reccomment to navigate to the project directory after creating a virtual environment before installing packages:

```shell
📁 root
    📁 venv
```

To install the packages after activating the virtual environment you just run the following command:

```shell
pip install <package_name>

# example

pip install numpy
```

### Getting an error?

If you are getting a command error that says:

```shell
'virtualenv' is not recognized as an internal or external command,
operable program or batch file.
```

You could try to install `virtualenv` using pip as follows:

```shell
pip install virtualenv
```

Or

```shell
python -m pip install virtualenv
```

### Installing Flask

```shell
pip install flask
```
