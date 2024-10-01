# nonces

A nonces generator based on a given size, a counter size, an optional seed and an optional byte order for the counter.

## Installation

```
pip install nonces
```

## Usage

### Basic Nonce Example:

```
from nonces import Nonce

# This will generate a random one-time 24 bytes nonce
nonce = Nonce.random(24)
```

### Basic Nonces Example:

```
from nonces import Nonces

# This will initiate an 8 bytes nonce with a 4 bytes counter
nonces = Nonces(size=8, counter_size=4)

# By default the counter is big endian with a random seed
# and the counter trailing at the end of the full nonce bytes

# Get the current nonce
nonce = nonces.nonce

print(nonce)

# Update the current counter
nonce = nonces.update()

print(nonce)
```

### Update counter:

```
# Set counter
nonce = nonces.set_counter(10)

print(nonce)

# Get the counter value
print(nonces.counter)

# Get the counter value in bytes
nonces.counter_bytes
```

### Check the OverFlowError:

```
# Check the OverFlowError exception when counter runs out
nonces.set_counter(nonces.max_counter)

nonces.update()
```

### Create nonce with counter from a specific seed:

```
# We can create a new object with the seed and change the byte order
# to little endian and a non-trailing counter (i.e, counter + nonce)

seed = b"\xff" * 4
nonces = Nonces(
   size=8,
   counter_size=4,
   seed=seed,
   order='little',
   trailing_counter=False
)
for i in range(10):
   nonces.update()

b'\x01\x00\x00\x00\xff\xff\xff\xff'
b'\x02\x00\x00\x00\xff\xff\xff\xff'
b'\x03\x00\x00\x00\xff\xff\xff\xff'
b'\x04\x00\x00\x00\xff\xff\xff\xff'
b'\x05\x00\x00\x00\xff\xff\xff\xff'
b'\x06\x00\x00\x00\xff\xff\xff\xff'
b'\x07\x00\x00\x00\xff\xff\xff\xff'
b'\x08\x00\x00\x00\xff\xff\xff\xff'
b'\t\x00\x00\x00\xff\xff\xff\xff'
b'\n\x00\x00\x00\xff\xff\xff\xff'

assert nonces.seed_bytes == seed
```

### Set the increment value:

```

nonces = Nonces(size=8, counter_size=4, seed=seed)

nonces.increment = 255

for i in range(10):
   nonces.update()

b'\xff\xff\xff\xff\x00\x00\x00\xff'
b'\xff\xff\xff\xff\x00\x00\x01\xfe'
b'\xff\xff\xff\xff\x00\x00\x02\xfd'
b'\xff\xff\xff\xff\x00\x00\x03\xfc'
b'\xff\xff\xff\xff\x00\x00\x04\xfb'
b'\xff\xff\xff\xff\x00\x00\x05\xfa'
b'\xff\xff\xff\xff\x00\x00\x06\xf9'
b'\xff\xff\xff\xff\x00\x00\x07\xf8'
b'\xff\xff\xff\xff\x00\x00\x08\xf7'
b'\xff\xff\xff\xff\x00\x00\t\xf6'
```

### Leverage bytes encoding options:

```
nonces = Nonces(size=8, counter_size=4)

nonce = nonces.nonce

nonce_hex = nonce.hex()

new_nonce = Nonce.fromhex(nonce_hex)

assert nonce == new_nonce
```