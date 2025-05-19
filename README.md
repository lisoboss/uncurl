# Uncurl

Convert `curl` commands into clean, executable Python `requests` code — or run them directly.

> Fully supports `Copy as cURL` from `chrome` browser DevTools.

## Installation

### PIP

```bash
pip install https://github.com/lisoboss/uncurl.git
```

### uv

```bash
uv tool install git+https://github.com/lisoboss/uncurl.git
```

## Usage

### Convert curl to Python

```bash
uncurl 'https://example.com/api?param=value' -H 'Authorization: Bearer token'
```

This will output Python code that uses the `requests` library to make the same request.

### Execute curl directly

The `tuncurl` command lets you execute the curl command directly using Python's requests library:

```bash
tuncurl 'https://example.com/api?param=value' -H 'Authorization: Bearer token'
```

## Features

- Converts curl commands to clean, readable Python code
- Handles common curl options:
  - `-X`, `--request`: HTTP method
  - `-H`, `--header`: HTTP headers
  - `-d`, `--data`, `--data-binary`, `--data-raw`: POST data
  - `-b`, `--cookie`: Cookie handling
  - `-u`, `--user`: Basic authentication
  - `-x`, `--proxy`: Proxy support
  - `--proxy-user`: Proxy authentication
  - `-k`, `--insecure`: Skip SSL verification
  - `--compressed`: Accept compressed responses
  - `-i`, `--include`: Include HTTP headers in the output
  - `-s`, `--silent`: Silent mode
- Extracts and displays query parameters
- Handles URL-encoded data
- Provides proper error handling

## Examples

### From Chrome DevTools (Copy as cURL)

```bash
uncurl 'https://api.example.com/data' \
  -H 'User-Agent: Mozilla/5.0' \
  -H 'Authorization: Bearer token' \
  --compressed
```

### Basic GET request

```bash
uncurl 'https://api.example.com/users'
```

### POST request with data and headers

```bash
uncurl 'https://api.example.com/login' \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"username":"user","password":"pass"}'
```

### Request with authentication

```bash
uncurl 'https://api.example.com/protected' \
  -u 'username:password'
```

### Using a proxy

```bash
uncurl 'https://api.example.com' \
  -x 'http://proxy.example.com:8080'
```

## Requirements

- Python >= 3.12
- requests >= 2.32.3

## License

[MIT license](./LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
