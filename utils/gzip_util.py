import base64
import gzip


def gzip_str_encode(string_: str) -> str:
    byte_array = gzip.compress(string_.encode())
    return base64.b64encode(byte_array).decode()


def gzip_str_decode(content: str) -> str:
    res = base64.b64decode(content)
    return gzip.decompress(res).decode()