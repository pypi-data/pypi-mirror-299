# nonces

A nonces generator based on a given size, a counter size, an optional seed and an optional byte order for the counter.

## Installation

```
pip install nonces
```

## Usage

```
from nonces import Nonce, Nonces

# To generate a new Nonces instance to generate nonces
# of 8 bytes, with a 4 bytes counter ->

nonces = Nonces(size=8, counter_size=4)

# Get the current nonce ->

nonce = nonces.nonce

new_nonce = bytes(nonce)

assert nonce == new_nonce

# Update the counter on default increment

nonces.update()

# Modify the counter to a given counter number

nonces.set_counter(10)

# Check counter value

nonces.counter

# Check counter bytes

nonces.counter_bytes

# Set it to the max counter number:

nonces.set_counter(nonces.max_counter)

# If you try to run nonces.update() at this point an OverFlowError
# as no more counters are available

nonces.update()

# Generate a new nonce of 16 bytes with 12 bytes from a given seed 
#and a 4 bytes counter as little endian (counter + nonce)

seed = Nonce.random(12)
# Nonce.random(12) returns a 12 bytes random nonce

nonces = Nonces(
	size=16,
	counter_size=4,
	seed=seed,
	order='little'
)

for i in range(10):
	nonces.update()

# Check seed value

nonces_seed = nonces.seed_bytes

assert seed == nonces_seed

# Change the increment value

nonces.increment = 255

for i in range(10):
	nonces.update()

# Get nonce value encoded in hex

nonce = nonces.nonce
nonce_hex = nonce.hex()

# Load a hex encoded nonce

new_nonce = Nonce.fromhex(nonce_hex)

assert nonce == new_nonce
```