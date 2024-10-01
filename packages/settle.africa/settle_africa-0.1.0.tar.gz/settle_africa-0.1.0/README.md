# Settle

## Overview

This settle provides a simple interface for interacting with an API using basic authentication. It allows setting credentials either through environment variables or directly within your application, and it supports both live and test modes.

## Installation

To install the settle africa, simply use pip:

```bash
pip install settle.africa
```

## Usage

### Setting Credentials

You can set credentials using environment variables or directly in your code:

```python
from settle.africa.auth import set_credentials

set_credentials('your_username', 'your_password')
```

Alternatively, you can use a `.env` file:

### Making API Requests

To make API requests:

```python
from settle.africa.api import make_request

response = make_request('endpoint', data={'key': 'value'})
print(response)
```

### Setting the Application Mode

You can set the application mode to either `test` or `live`:

```python
from settle.africa.settings import set_mode

set_mode('test')
```

### Running Tests

To run the tests:

```bash
pytest tests/
```

## Git Versioning

We recommend using Git for version control. Here's a simple versioning guide:

- **MAJOR** version when you make incompatible API changes.
- **MINOR** version when you add functionality in a backward-compatible manner.
- **PATCH** version when you make backward-compatible bug fixes.

For example:

```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

## License

This project is licensed under the MIT License.
