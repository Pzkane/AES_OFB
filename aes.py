from AES.aes import encrypt as aes_encrypt
import sys
import pathlib
import mimetypes

def encrypt_OFB_mode(plain_text, key, iv):
    pos = 0
    cipher_text_chunks = []
    original_IV = iv
    # Pad the data with 0x80, similar to AES padding
    if len(plain_text) % 16 != 0:
        plain_text += b"\x80"
    # Fill remaining padding with zeroes
    while len(plain_text) % 16 != 0:
        plain_text += b"0"
    # Encrypt each block of 16 bytes
    while pos + 16 <= len(plain_text):
        # Encrypt IV
        temp_after_enc_block = aes_encrypt(key,iv)
        # Get plain_text with offset
        plain_chunk = plain_text[pos:pos + 16]
        # Get cyphertext by XORing temp value from encryption block and cipher text
        cipher_text = bytes([temp_after_enc_block[i] ^ plain_chunk[i] for i in range(16)])
        cipher_text_chunks.append(cipher_text)
        pos += 16
        # Set new IV as temp value from encryption block
        iv = temp_after_enc_block
    return (original_IV, cipher_text_chunks)

# Usage:
#   python -m aes <mode> <path_to_file> <key> <iv>

# Modes:
#  E - encrypt
#  D - decrypt

# Example
#   Encrypt:
#   python -m aes E ./some_file 0123456789abcdef ffffffffeeeeeeee
#   Decrypt:
#   python -m aes D ./some_file 0123456789abcdef

STATIC_EXT_LEN = 2
STATIC_IS_BIN = 1

def is_binary(file_name):
    try:
        with open(file_name, 'tr') as check_file:  # try open file in text mode
            check_file.read()
            return False
    except:  # if fail then file is non-text (binary)
        return True


def encrypt_decrypt(mode: str, filename: str, key: bytes, globalIV: bytes):
    # Structure:
    # IV + binary_file_flag + extension_length + extension + encrypted_data
    # Note: 'extension_length' and 'extension' are in plain_text
    if mode == 'E':
        file_extension = pathlib.Path(filename).suffix
        print("File Extension:", file_extension)
        print("Is file binary?", is_binary(filename))

        combined_result = globalIV + ((1).to_bytes(STATIC_IS_BIN, 'little') if is_binary(filename) else (0).to_bytes(STATIC_IS_BIN, 'little')) + len(file_extension[1:]).to_bytes(STATIC_EXT_LEN, 'little') + str.encode(file_extension[1:])
        print(combined_result)
        r_handle = open(filename, 'rb')
        new_filename = filename + '-encrypted'
        # Write metadata
        w_handle = open(new_filename, 'wb')
        w_handle.write(combined_result)
        w_handle.close()

        # Write encrypted data
        w_handle = open(new_filename, 'ab')
        while True:
            piece = r_handle.read(1024)
            if not piece:
                break
            iv, result = encrypt_OFB_mode(piece, key, globalIV)
            # print(iv, result)
            # print("bstring:",b''.join(result))
            w_handle.write(b''.join(result))
        r_handle.close()
        w_handle.close()
        print("FILE ENCRYPTED")
    elif mode == 'D':
        r_handle = open(filename, 'rb')
        iv = r_handle.read(16)
        binary_flag = int.from_bytes(r_handle.read(STATIC_IS_BIN), 'little')
        ext_len = int.from_bytes(r_handle.read(STATIC_EXT_LEN), 'little')
        print("Extension len (decoded):", ext_len)
        ext = (r_handle.read(ext_len)).decode()
        print("Extension (decoded):", ext)
        new_filename = filename + "-decrypted." + ext
        w_handle = open(new_filename, 'wb')
        while True:
            piece = r_handle.read(1024)
            if not piece:
                break
            iv, result = encrypt_OFB_mode(piece, key, iv)
            # print(iv, result)
            result = b''.join(result)
            # For non-binary file's final chunk find the 0x80 byte position
            if binary_flag == 0:
                try:
                    pos_0x80 = result.index(b'\x80')
                    # Strip it and trailing zeroes
                    result = result[:pos_0x80]
                except ValueError:
                    pass
            w_handle.write(result)
        r_handle.close()
        w_handle.close()
        print("FILE DECRYPTED")

if __name__ == '__main__':
    encrypt_decrypt(sys.argv[1], sys.argv[2], str.encode(sys.argv[3]), str.encode(sys.argv[4]))