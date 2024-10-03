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

import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__)
except (ValueError, importlib.metadata.PackageNotFoundError):
    __version__ = "0.0.0"


def main():
    print(f"Hello from {__package__}!")
    print("Version", __version__)
