# This file is part of Bestow.
# Copyright (C) 2024 Taylor Rodríguez.
#
# Bestow is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Bestow is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Bestow. If not, see
# <http://www.gnu.org/licenses/>.

"""Bestow: simple and secure file transfer CLI."""

__all__ = ["main", "__version__"]

import argparse
import asyncio
import errno
import importlib.metadata
import os
import socket
import sys

try:
    __version__ = importlib.metadata.version(__package__)
except (ValueError, importlib.metadata.PackageNotFoundError):
    __version__ = "0.0.0"

# Define the range of dynamic/private ports. This helps to avoid
# conflicts with reserved ports or other registered ports.
MIN_PORT = 49152
MAX_PORT = 65535
# Define the default port to use for TCP connections.
BASE_PORT = 50222


def set_port(port_input: str, /) -> int:
    """Ensure that a port conforms with the dynamic port range."""
    try:
        port = int(port_input)
    except ValueError:
        raise argparse.ArgumentTypeError("port must be an integer")

    if port < MIN_PORT or port > MAX_PORT:
        raise argparse.ArgumentTypeError(
            f"port must be between {MIN_PORT} and {MAX_PORT}"
        )

    return port


async def get_local_ip_address() -> str:
    """Determine the machine's local IP address."""
    loop = asyncio.get_event_loop()
    # BUG: For some odd reason, this function appears to seems to only
    # return the correct IP address when ran in an async event loop.
    return await loop.run_in_executor(
        None, socket.gethostbyname, socket.gethostname()
    )


async def tcp_client(host: str, port: int, message: str) -> None:
    """Send a message to the server and wait for a response."""
    try:
        reader, writer = await asyncio.open_connection(host=host, port=port)
    except OSError as e:
        # Attempt to parse errno.
        error = os.strerror(e.errno)

        if "Unknown error" in error:
            error = str(e)

        # Display error message and exit.
        sys.stderr.write(f"error: {error}\n")
        sys.exit(1)

    writer.write(message.encode(encoding="utf-8"))
    await writer.drain()

    print(f"* sent {message!r} to {host}:{port}")

    data = await reader.read(100)
    reply = data.decode(encoding="utf-8")

    print(f"* received {reply!r} from {host}:{port}")

    writer.close()
    await writer.wait_closed()


async def tcp_server(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """Receive a message from the client and echo it back."""
    data = await reader.read(100)
    message = data.decode(encoding="utf-8")

    host, port = writer.get_extra_info("peername")
    print(f"* received {message!r} from {host}:{port}")

    writer.write(data)
    await writer.drain()

    print(f"* echoed {message!r} back to {host}:{port}")

    writer.close()
    await writer.wait_closed()


async def enumerate_server_ports(
    host: str, base_port: int, max_port: int
) -> asyncio.Server:
    """Enumerate port numbers until one is not in use."""
    for port in range(base_port, max_port + 1):
        try:
            server = await asyncio.start_server(
                tcp_server, host=host, port=port
            )
        except OSError as e:
            # EADDRINUSE: Address already in use.
            if e.errno == errno.EADDRINUSE:
                print(f"* port {port} is already in use, trying next port")
            else:
                # Raise if the errno is unexpected.
                raise e
        else:
            return server

    raise RuntimeError("no available ports found")


async def start_server(host: str, port: int, message: str = "") -> None:
    server = await enumerate_server_ports(
        host=host, base_port=port, max_port=MAX_PORT
    )
    addrs = (f"{j}:{k}" for i in server.sockets for j, k in (i.getsockname(),))
    print(f"* serving on {', '.join(addrs)}")

    async with server:
        await server.serve_forever()


def handle_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Simple and secure file transfer CLI"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s version {__version__}",
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True,
        description=("Run `%(prog)s <command> --help` for more information"),
    )

    # Parse arguments for the `start` command.
    description = "Provide files to the client"
    server_parser = commands.add_parser(
        name="start", description=description, help=description.lower()
    )
    server_parser.set_defaults(
        coroutine=start_server, host=asyncio.run(get_local_ip_address())
    )
    server_parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=set_port,
        default=BASE_PORT,
        help=(
            "port number to listen for incoming connections "
            f"(default: {BASE_PORT})"
        ),
    )

    # Parse arguments for the `connect` command.
    description = "Request files from the server"
    client_parser = commands.add_parser(
        name="connect", description=description, help=description.lower()
    )
    client_parser.set_defaults(coroutine=tcp_client)
    client_parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=set_port,
        default=BASE_PORT,
        help=f"port number to connect to the server (default: {BASE_PORT})",
    )
    client_parser.add_argument(
        "host", type=str, help="the IP address of the server"
    )

    # Default argument is --help if no args are provided.
    default_args = None if sys.argv[1:] else ["--help"]
    return parser.parse_args(args=default_args)


def main() -> None:
    """Run main the script."""
    args = handle_args()
    try:
        asyncio.run(
            args.coroutine(host=args.host, port=args.port, message="hello")
        )
    except KeyboardInterrupt:
        pass
