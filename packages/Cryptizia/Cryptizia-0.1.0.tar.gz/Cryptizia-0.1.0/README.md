# Cryptizia

Cryptizia is a Python library for various cipher techniques including the Caesar cipher. 

## Installation

You can install the library using pip:

```bash
pip install cryptizia

```
## How to use in Code

```python

from cryptizia import CaesarCipherExample

CaesarCipherExample()
```
### Customization
You can customize the 'shift' and 'plaintext' directly in the constructor if you want different values:
```python
# Example with custom shift and plaintext
cipher = CaesarCipherExample(shift=5, plaintext="WORLD")
```