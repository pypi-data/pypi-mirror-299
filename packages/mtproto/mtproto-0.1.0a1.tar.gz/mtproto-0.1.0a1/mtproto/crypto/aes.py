from functools import partial
from hashlib import sha256

try:
    import tgcrypto
except ImportError:  # pragma: no cover
    tgcrypto = None
try:
    import pyaes
except ImportError:  # pragma: no cover
    pyaes = None


if tgcrypto is None and pyaes is None:  # pragma: no cover
    raise ImportError("Expected at least one or (tgcrypto, pyaes) to be installed.")


if tgcrypto is not None:
    _ctr256_encrypt = tgcrypto.ctr256_encrypt
    _ctr256_decrypt = tgcrypto.ctr256_decrypt
    _ige256_encrypt = tgcrypto.ige256_encrypt
    _ige256_decrypt = tgcrypto.ige256_decrypt
elif pyaes is not None:
    def ctr(data: bytes, key: bytes, iv: bytearray, state: bytearray) -> bytes:
        cipher = pyaes.AES(key)

        out = bytearray(data)
        chunk = cipher.encrypt(iv)

        for i in range(0, len(data), 16):
            for j in range(0, min(len(data) - i, 16)):
                out[i + j] ^= chunk[state[0]]

                state[0] += 1

                if state[0] >= 16:
                    state[0] = 0

                if state[0] == 0:
                    for k in range(15, -1, -1):
                        try:
                            iv[k] += 1
                            break
                        except ValueError:
                            iv[k] = 0

                    chunk = cipher.encrypt(iv)

        return out


    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )


    def ige(data: bytes, key: bytes, iv: bytes, encrypt: bool) -> bytes:
        cipher = pyaes.AES(key)

        iv_1 = iv[:16]
        iv_2 = iv[16:]

        data = [data[i: i + 16] for i in range(0, len(data), 16)]

        if encrypt:
            for i, chunk in enumerate(data):
                iv_1 = data[i] = xor(cipher.encrypt(xor(chunk, iv_1)), iv_2)
                iv_2 = chunk
        else:
            for i, chunk in enumerate(data):
                iv_2 = data[i] = xor(cipher.decrypt(xor(chunk, iv_2)), iv_1)
                iv_1 = chunk

        return b"".join(data)


    _ctr256_encrypt = ctr
    _ctr256_decrypt = ctr
    _ige256_encrypt = partial(ige, encrypt=True)
    _ige256_decrypt = partial(ige, encrypt=False)


def ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray) -> bytes:
    return _ctr256_encrypt(data, key, iv, state)


def ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray) -> bytes:
    return _ctr256_decrypt(data, key, iv, state)


def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return _ige256_encrypt(data, key, iv)


def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return _ige256_decrypt(data, key, iv)


def kdf(auth_key: bytes, msg_key: bytes, from_client: bool) -> tuple:
    # taken from pyrogram, mtproto.py
    x = 0 if from_client else 8

    sha256_a = sha256(msg_key + auth_key[x:x + 36]).digest()
    sha256_b = sha256(auth_key[x + 40:x + 76] + msg_key).digest()  # 76 = 40 + 36

    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]

    return aes_key, aes_iv


CtrTuple = tuple[bytes, bytes, bytearray]
