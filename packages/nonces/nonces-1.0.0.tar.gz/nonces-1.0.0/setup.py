# Copyright 2024 Gonzalo Atienza Rela
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup
from src.nonces import (
    __title__,
    __version__,
    __description__,
    __url__,
    __author__,
    __email__,
    __license__
)


setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=__url__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    packages=["nonces"],
    package_dir={"": "src"},
    python_requires='>=3.8'
)
