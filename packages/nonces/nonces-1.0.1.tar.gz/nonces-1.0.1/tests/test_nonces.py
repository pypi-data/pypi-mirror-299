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
import pytest
from nonces import Nonce, Nonces


SIZES = [8, 8, 12, 12, 16, 16, 24, 24, 32, 32]
C_SIZES = [2, 4, 4, 6, 6, 8, 8, 12, 12, 16]
S_SIZES = [6, 4, 8, 6, 10, 8, 16, 12, 20, 16]


assert len(SIZES) == len(C_SIZES) == len(S_SIZES)
for i in range(len(SIZES)):
    assert SIZES[i] == C_SIZES[i] + S_SIZES[i]


ALL_SIZES = list(zip(SIZES, S_SIZES, C_SIZES))
VECTORS = []
for i in range(len(SIZES)):
    VECTORS.extend(
        [
            # size, counter_size, seed, order, trailing_counter, firt_nonce
            [
                SIZES[i],
                C_SIZES[i],
                b"\xff" * S_SIZES[i],
                "big",
                True,
                b"\xff" * S_SIZES[i] + b"\x00" * (C_SIZES[i] - 1) + b"\x01"
            ],
            [
                SIZES[i],
                C_SIZES[i],
                b"\xff" * S_SIZES[i],
                "little",
                True,
                b"\xff" * S_SIZES[i] + b"\x01" + b"\x00" * (C_SIZES[i] - 1)
            ],
            [
                SIZES[i],
                C_SIZES[i],
                b"\xff" * S_SIZES[i],
                "big",
                False,
                b"\x00" * (C_SIZES[i] - 1) + b"\x01" + b"\xff" * S_SIZES[i]
            ],
            [
                SIZES[i],
                C_SIZES[i],
                b"\xff" * S_SIZES[i],
                "little",
                False,
                b"\x01" + b"\x00" * (C_SIZES[i] - 1) + b"\xff" * S_SIZES[i]
            ]
        ]
    )


class TestNonce:
    @pytest.mark.parametrize("size", SIZES)
    def test(self, size):
        nonce_bytes = b"A0" * size
        nonce = Nonce(nonce_bytes)
        assert nonce == nonce_bytes
        assert isinstance(nonce, Nonce)
        assert isinstance(nonce, bytes)


class TestNonces:
    @pytest.mark.parametrize(
        (
            "size",
            "counter_size",
            "seed",
            "order",
            "trailing_counter",
            "nonce"
        ),
        VECTORS,
    )
    def test_params(
        self,
        size: int,
        counter_size: int,
        seed: bytes,
        order: str,
        trailing_counter: bool,
        nonce: bytes,
    ):
        nonces = Nonces(size, counter_size, seed, order, trailing_counter)
        assert nonces.update() == nonce

    @pytest.mark.parametrize(
        "size, c_size", list(zip(SIZES, C_SIZES))
    )
    def test_overflow(self, size, c_size):
        nonces = Nonces(size, c_size)
        nonces.set_counter(nonces.max_counter)
        with pytest.raises(OverflowError):
            nonces.update()

    def test_bad_params(self):
        with pytest.raises(TypeError):
            Nonces("test")
        with pytest.raises(ValueError):
            Nonces(0, 0)
        with pytest.raises(TypeError):
            Nonces(8, "test")
        with pytest.raises(ValueError):
            Nonces(8, 9)
        with pytest.raises(TypeError):
            Nonces(8, 4, "test")
        with pytest.raises(TypeError):
            Nonces(8, 4, b"\x00" * 4, None)
        with pytest.raises(ValueError):
            Nonces(8, 4, b"\x00" * 4, "test")
        with pytest.raises(TypeError):
            Nonces(8, 4, b"\x00" * 4, "big", None)
        with pytest.raises(ValueError):
            Nonces(8, 4, b"\x00" * 5, "big", True)

    @pytest.mark.parametrize(
        "size, c_size", list(zip(SIZES, C_SIZES))
    )
    def test_set_counter(self, size, c_size):
        nonces = Nonces(size, c_size)
        with pytest.raises(TypeError):
            nonces.set_counter('test')
        with pytest.raises(ValueError):
            nonces.set_counter(nonces.max_counter + 1)
        nonces.set_counter(nonces.max_counter)
        with pytest.raises(AssertionError):
            nonces.set_counter(0)

    @pytest.mark.parametrize(
        "size, c_size", list(zip(SIZES, C_SIZES))
    )
    def test_increment_setter(self, size, c_size):
        nonces = Nonces(size, c_size)
        nonces.update()
        with pytest.raises(TypeError):
            nonces.increment = 'test'
        with pytest.raises(ValueError):
            nonces.increment = 0
        with pytest.raises(ValueError):
            nonces.increment = -1
        with pytest.raises(ValueError):
            nonces.increment = nonces.max_counter
        nonces.set_counter(nonces.max_counter - 2)
        nonces.increment = 2
        nonces.update()
        assert nonces.counter == nonces.max_counter
