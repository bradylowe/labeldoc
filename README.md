# labeldoc
A simple, extendible PyQt5 app for annotating documents.

Inspiration taken from [labelme](https://github.com/labelmeai/labelme.git) repo.
===========================================================

## Quick Start

### Installation

   **Creating a virtual environment**
   ```
   python3 -m pip install virtualenv
   python3 -m virtualenv .venv
   source .venv/bin/activate
   ```

   **Installing the app**
   ```
   pip install -r requirements.txt
   pip install -e .
   ```

   **Installing the app from another directory**
   ```
   pip install -r /path/to/labeldoc/requirements.txt
   pip install -e /path/to/labeldoc
   ```

### Running the app

Launch the app by running:

```
labeldoc
```

or, to open a file on launch:

```
labeldoc /path/to/file.pdf
```
