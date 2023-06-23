class ASN1PartialParser:
    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def get_size(self):
        return self.offset + self.length

    def parse_tag(self, data):
        tag_size = 1
        if len(data) < 2:
            raise ValueError("few data size")
        if data[0] & 0x1F == 0x1F:
            tag_size += 1
            if len(data) < 2 or data[1]&0x80 != 0:
                raise ValueError("unexpected tag size")

        self.offset = tag_size

    def parse_length(self, data):
        if self.offset >= len(data):
            raise ValueError("few data size")
        b = data[self.offset]
        self.offset += 1
        if b&0x80 == 0:
            self.length = b
        else:
            lol = b&0x7F
            for i in range(lol):
                if self.offset >= len(data):
                    raise ValueError("truncated tag or length")
                b = data[self.offset]
                self.offset += 1
                self.length |= int(b)
    
    def parse(self, data):
        self.parse_tag(data)
        self.parse_length(data)
    