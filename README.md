# AES encryption with OFB mode

# GUI
## Usage:
```python -m aes_gui```


# CLI

## Usage:
```python -m aes <mode> <path_to_file> <key> <iv>```

### Modes:
E - encrypt

D - decrypt


## Example
###   Encrypt:
```python -m aes E ./some_file 0123456789abcdef ffffffffeeeeeeee```

will produce encrypted file ```some_file-encrypted```

###   Decrypt:
```python -m aes D ./some_file-encrypted 0123456789abcdef```

# GUI
