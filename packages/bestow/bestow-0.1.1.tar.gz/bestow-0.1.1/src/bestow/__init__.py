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

__all__ = ["main", "__version__"]

import argparse
import asyncio
import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__)
except (ValueError, importlib.metadata.PackageNotFoundError):
    __version__ = "0.0.0"


def format_address(address: tuple[str, int]) -> str:
    host, port = address
    return f"{host}:{port}"


async def tcp_client(message: str) -> None:
    reader, writer = await asyncio.open_connection(host="127.0.0.1", port=8888)

    writer.write(message.encode(encoding="utf-8"))
    await writer.drain()

    print(f"* sent {message!r}")

    data = await reader.read(100)
    reply = data.decode(encoding="utf-8")

    print(f"* received {reply!r}")

    writer.close()
    await writer.wait_closed()


async def tcp_server(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    data = await reader.read(100)
    message = data.decode(encoding="utf-8")
    address = writer.get_extra_info("peername")

    print(f"* received {message!r} from {format_address(address)}")

    writer.write(data)
    await writer.drain()

    print(f"* echoed {message!r} back")

    writer.close()
    await writer.wait_closed()


async def start_server() -> None:
    server = await asyncio.start_server(tcp_server, host="127.0.01", port=8888)
    addrs = ", ".join(
        format_address(sock.getsockname()) for sock in server.sockets
    )
    print(f"* serving on {addrs}")

    async with server:
        await server.serve_forever()


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", dest="server", action="store_true")
    parser.add_argument("-c", "--client", dest="client", action="store_true")
    return parser.parse_args()


def main() -> None:
    print("*", __package__, "version", __version__)

    args = handle_args()

    if args.server:
        asyncio.run(start_server())
    elif args.client:
        asyncio.run(tcp_client("hello"))
