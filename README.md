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

### Hosting Flask App.

In this section we are going to have a look at how we can deploy a flask static site. First you need to install `frozen-flask`.

> Frozen-Flask freezes a Flask application into a set of static files. The result can be hosted without any server-side software other than a traditional web server.

```shell
pip install Frozen-Flask
```

We are going to create a `build.py` file. This is where we are going to write the code for building the app using `frozen-flask`. The script for building a static flask app is as follows:

```py
from app import app
from flask_frozen import Freezer

freezer = Freezer(app=app, with_static_files=True)
if __name__ == '__main__':
    freezer.freeze()
```

Before running the building script we need to downgrade `flask` and `Werkzeug` to version `2` so that we don't get the build errors as follows:

```shell
pip install flask==2.1.2 && pip install Werkzeug==2.3.1
```

To generate the build we will need to run the following command:

```shell
python build.py
```

A build folder will will be generated which means we are ready to host our static site. First things first we need to generate a `requirements.txt` file by running the following command:

```shell
pip freeze > requirements.txt
```

After that we are going to then commit our project to `GitHub`. Then we can host our static site on the following cloud services:

1. [Netlify](https://www.netlify.com)
2. [Cloudflare](https://www.cloudflare.com/)
3. [GitHub Pages](https://pages.github.com/)
4. [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/)

### Hosting on Netlify

First you need to create a [Netlify](https://www.netlify.com) account.

1. When authenticated you will need to select an option on the Dashboard that says **`Import From Git`**.
2. Then select `Deploy With GitHub`
3. Select the `GitHub` project that you want to deploy.
4. Specify the base directory to `/`
5. Set deploy branch to `main`
6. And you need to specify the build command to `python3 build.py`
7. Since a set of static files (HTML, CSS, JavaScript) are being deployed, only the `Publish directory` needs to be specified as the path to the set of static files: `/build`
8. Click the `deploy` button then your site will be deployed.

### Links

1. [Frozen-Flask](https://pythonhosted.org/Frozen-Flask/)
2. [static-site-flask-and-netlify](https://testdriven.io/blog/static-site-flask-and-netlify/)
