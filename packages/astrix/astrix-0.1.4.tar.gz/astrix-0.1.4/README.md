# Astrix

![Astrix Logo](https://firebasestorage.googleapis.com/v0/b/nmit-hacks-f2830.appspot.com/o/AstrixDarkWiBg.png?alt=media&token=c56eb69b-8be5-410c-9c65-269043f60f00)

[![PyPI version](https://badge.fury.io/py/astrix.svg)](https://badge.fury.io/py/astrix)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Downloads](https://img.shields.io/pypi/dm/astrix)

**Astrix: Your All-in-One Python Project Analyzer**

Astrix is a comprehensive tool designed to analyze and optimize Python projects by checking dependencies, code quality metrics, documentation, and much more.

---

## Features

Astrix comes with a set of powerful commands to help you analyze, manage, and optimize your Python projects.

- **analyze**: Analyze functions in a given Python file for various metrics like cyclomatic complexity.
  
  ```bash
  astrix analyze <path>

- **callgraph**: Generate a call graph of the specified Python file to visualize function dependencies.
  
  ```bash
  astrix callgraph <file>

- **class-info**: Analyze the specified Python file and generate a class hierarchy diagram.
  
  ```bash
  astrix class-info <file>

- **maintainability**: Analyze the maintainability index and Halstead metrics for the given Python file.
  
  ```bash
  astrix maintainability <file>

- **deps**: Analyze the specified Python file and return a list of dependencies, and return various information such as dependency name, its description, its documentation link and the github url
  
  ```bash
  astrix deps <path>

- **install**: reate a virtual environment for the current project and install dependencies from a specified file (e.g., requirements.txt), if the file is not provided, it simply creates a virtual environment.
  
  ```bash
  astrix install <file>
  
- **delete**: Delete the virtual environment associated with the current project, if given path to the file specified (e.g., requirements.txt)
  
  ```bash
  astrix delete <file>

---

## Installation

You can install Astrix using:

```bash
pip install astrix
