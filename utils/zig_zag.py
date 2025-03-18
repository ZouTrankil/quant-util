class ZigZag(object):
    @staticmethod
    def encode(value) -> int:
        if value >= 0:
            return value << 1
        return (value << 1) ^ (~0)

    @staticmethod
    def decode(value) -> int:
        if not value & 0x1:
            return value >> 1
        return (value >> 1) ^ (~0)
