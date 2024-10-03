# Bestow

Simple and secure file transfer CLI.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
  - [Using uv](#using-uv)
  - [Using pip](#using-pip)
  - [Using Termux](#using-termux)
- [Usage](#usage)
    - [Serving a File](#serving-a-file)
    - [Receiving a File](#receiving-a-file)
- [License](#license)

## Description

This Python program facilitates fast encrypted file transfers over a TCP
connection. I made this project because I needed peace of mind when
sending data on an untrusted network.

## Features

- Straightforward command-line interface.
- Secured with modern encryption standards.
- Capable of handling large files efficiently.
- Speed benefits due to asynchronous design.
- Supports multiple client connections concurrently.

## Installation

This project supports CPython v3.10 and later. The latest version can be
installed at <https://python.org/download/>.

### Using uv

This is the recommended installation method because it isolates the
package environment from the system.

1. Install [`uv`](https://pypi.org/project/uv) if you haven't already:

```shell
python3 -m pip install --user uv
uv tool update-shell
```

2. Install the package:

```
uv tool install git+https://codeberg.org/vitebyte/bestow.git
```

Make sure to restart the shell before using `bestow`.


### Using pip

:warning: This installation method is **not recommended**, as the
package will be installled in the global environment. This is not ideal
because it can lead to dependency conflicts or potentially break
packages needed by the system.

```
python3 -m pip install git+https://codeberg.org/vitebyte/bestow.git
```

### Using Termux

If you have issues with the [recommended](#using-uv) install method
on [Termux](https://termux.dev/), you can build
[`PyNaCl`](https://pypi.org/project/pynacl/)
using the system installation of
[`libsodium`](https://doc.libsodium.org/).
The solution is was taken from a `PyNaCl`
[GitHub issue](https://github.com/pyca/pynacl/issues/483#issuecomment-608049721).

```shell
pkg install clang python libffi openssl libsodium
SODIUM_INSTALL=system python -m pip install pynacl
python3 install git+https://codeberg.org/vitebyte/bestow.git
```

## Usage

The file transfer model involves two components: the server, who
provides the file, and the client, who receives the file. This model
ensures that the server can control who will receive the data and helps
to mitigate malicious actors.

### Serving a File

This will make it possible for a client to connect to the server's IP
address on a specific port (by default it is 4919).

```
bestow serve file.txt
```

### Receiving a File

```
bestow recv 192.168.0.1
```

### License

This project is licensed under the GNU Affero General Public License
version 3.0 or later. See the [LICENSE](./LICENSE) file for more details.
