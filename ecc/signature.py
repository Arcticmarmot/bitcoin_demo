class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def der(self):
        """
        Return the DER format of signature
        """
        r_bin = self.r.to_bytes(32, byteorder='big')
        r_bin = r_bin.lstrip(b'\x00')
        if r_bin[0] & 0x80:
            r_bin = b'\x00' + r_bin
        result = bytes([2, len(r_bin)]) + r_bin

        s_bin = self.s.to_bytes(32, byteorder='big')
        s_bin = s_bin.lstrip(b'\x00')
        if s_bin[0] & 0x80:
            sbin = b'\x00' + s_bin
        result += bytes([2, len(s_bin)]) + s_bin

        return bytes([0x30, len(result)]) + result

    def __repr__(self):
        return 'Signature({:x},{:x})'.format(self.r, self.s)

