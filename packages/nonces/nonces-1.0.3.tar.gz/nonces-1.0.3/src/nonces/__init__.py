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
from .nonces import Nonce, Nonces


__all__ = [
    Nonce,
    Nonces,
    "__title__",
    "__description__",
    "__url__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]

__title__ = "nonces"
__description__ = "Nonces generator for cryptographic purposes"
__url__ = "https://github.com/gonatienza/nonces/"
__version__ = "1.0.3"
__author__ = "Gonzalo Atienza Rela"
__email__ = "gonatienza@gmail.com"
__license__ = "Apache License 2.0"
__copyright__ = f"Copyright 2024 {__author__}"
