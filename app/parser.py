class CommandParser:
    def __init__(self, raw: bytes) -> None:
        self.raw = raw
        self.type_handlers = {
            ord('+'): self.parse_line,
            ord('-'): self.parse_line,
            ord(':'): self.parse_integers,
            ord('$'): self.parse_bulk_string,
            ord('*'): self.parse_array
        }

    def parse(self):
        handler = self.type_handlers.get(self.raw[0])

        if not handler:
            return None
        return handler()
    
    def parse_integers(self):
        try:
            idx = self.raw.index(b"\r\n")
            value = int(self.raw[1:idx].decode())

            self.raw = self.raw[idx+2:]
            return value
        except ValueError:
            return None

        
    def parse_line(self):
        try:
            idx = self.raw.index(b'\r\n')
            str_byte = self.raw[1:idx]

            self.raw = self.raw[idx+2:]
            return str_byte.decode('utf-8')
        except ValueError:
            return None
    

    def parse_array(self):
        try:
            idx = self.raw.index(b'\r\n')
            num_elements = int(self.raw[1:idx].decode())

            self.raw = self.raw[idx+2:]
            elements = []
            for _ in range(num_elements):
                if not self.raw:
                    return None
                handler = self.type_handlers.get(self.raw[0])
                if not handler:
                    return None
                element = handler()
                elements.append(element)
            return elements
        except ValueError:
            return None

    def parse_bulk_string(self):
        # b"$3\r\nfoo\r\n"
        try:
            idx = self.raw.index(b'\r\n')
            string_length = int(self.raw[1:idx].decode())
            string_start = idx + 2
            string_end = string_start + string_length

            result =  self.raw[string_start:string_end].decode()
            self.raw = self.raw[string_end+2:]
            return result
        except ValueError:
            return None