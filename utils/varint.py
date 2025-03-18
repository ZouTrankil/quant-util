from io import BytesIO


class Varint:

    @staticmethod
    def encode(number):
        buf = b''
        length = 0
        while True:
            towrite = number & 0x7f
            number >>= 7
            length += 1
            if number:
                buf += bytes(((towrite | 0x80),))
            else:
                buf += bytes((towrite,))
                break
        return buf, length

    @staticmethod
    def decode(buf):
        stream = BytesIO(buf)

        shift = 0
        result = 0
        length = 0
        while True:
            i = Varint._read_one(stream)
            result |= (i & 0x7f) << shift
            shift += 7
            length += 1
            if not (i & 0x80):
                break

        return result, length

    @staticmethod
    def _read_one(stream):
        c = stream.read(1)
        if c == b'':
            raise EOFError("Unexpected EOF while reading bytes")
        return ord(c)


if __name__ == '__main__':
    varint, length = Varint.encode(299)
    print(f'{varint}:{length}')
    result, length = Varint.decode(varint)
    print(f'{result}:{length}')
