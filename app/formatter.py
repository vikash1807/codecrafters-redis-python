class ResponseFormatter:

    def error(self, data) -> bytes:
        return f"-{data}\r\n".encode()
    
    def format(self, data, simple_str=False) -> bytes:
        return self._format(data, simple_str=simple_str) + b'\r\n'
    
    def _format(self, data, simple_str=False):
        print(data)
        if data is None:
            return b'$-1'
        
        if isinstance(data, int):
           return self._format_int(data)
        
        if isinstance(data, str):
            if simple_str:
                return f"+{data}".encode()
            return self._format_string(data)
        
        if isinstance(data, list):
            return self._format_array(data)
    
    def _format_int(self, data: int)-> bytes:
        return f":{data}".encode()
    
    def _format_string(self, data: str)-> bytes:
        bdata = data.encode()
        return f"${len(bdata)}\r\n".encode() + bdata
    
    def _format_array(self, data: list)-> bytes:
        length = len(data)
        if not length:
            return b'*0'
        formatted = [self._format(element) for element in data]
        return f"*{length}\r\n".encode() + b"\r\n".join(formatted)
