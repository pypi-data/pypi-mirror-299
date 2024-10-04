"""PyPackIT-Test1: A Placeholder Project Title.

Replace this text with a short abstract of PyPackIT-Test1, describing its
purpose and main features. By default, this text is displayed on the
repository's main README file, on the homepage of the project's website, on the
project's PyPI and TestPyPI pages, and on the package's main docstring. Like all
other entries in the repository's control center, this text can also contain
dynamic references to other entries, using the <code>${‎{ json-path.to.value
}}</code> syntax. By default, the first occurrence of the name of the project in
this text is styled as strong and linked to the project's website.

Copyright (C) 2024 Armin Ariamajd

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pypackit_test1 import data

__all__ = ["data", "__version_details__", "__version__"]

__version_details__: dict[str, str] = {
    "version": "0.0.1",
    "build_date": "2024.10.03",
    "committer_date": "2024.10.03",
    "author_date": "2024.10.03",
    "branch": "None",
    "distance": "0",
    "commit_hash": "cf2c32972e2e947ebe3efd9041cc04f9abd1cf1a",
}

"""Details of the currently installed version of the package,
including version number, date, branch, and commit hash."""

__version__: str = __version_details__["version"]
"""Version number of the currently installed package."""
