import asyncio

from app.parser import CommandParser
from app.formatter import ResponseFormatter

response_formatter = ResponseFormatter()
store = {}

class RedisServer:

    def __init__(self, reader, writer)-> None:
        self._reader = reader
        self._writer = writer

        self._commands = {
            "ping" : self._ping,
            "echo": self._echo,
            "set": self._set,
            "get": self._get
        }


    async def serve(self):
        addr = self._writer.get_extra_info("peername")
        while(True):
            data = await self._reader.read(1024)

            if not data:
                break
                
            cmd, *args = CommandParser(data).parse()
            cmd = cmd.lower()

            print(f"Recieved command {cmd} with args: {args}.")

            try:
                if cmd in self._commands:
                    self._commands[cmd.lower()](*args)
                else:
                    null_data = response_formatter.format(None)
                    self._writer.write(null_data)

            except Exception as e:
                err = response_formatter.error(f"Error on {cmd} command: {e}")
                self._writer.write(err)

            await self._writer.drain()
        
        print(f"close the connection {addr}")
        self._writer.close()
        await self._writer.wait_closed()

    def _ping(self, *args):
        self._writer.write(response_formatter.format("PONG"))

    
    def _echo(self, value):
        echo = response_formatter.format(value)
        self._writer.write(echo)
    
    def _set(self, key, value, ext_key=None, ext_value=None):

        if ext_key == 'px':
            loop = asyncio.get_running_loop()
            loop.call_later(
                int(ext_value)/1000,
                store.pop,
                key
            )
        if ext_key == 'ex':
            loop = asyncio.get_running_loop()
            loop.call_later(
                int(ext_value),
                store.pop,
                key
            )
        
        store[key] = value
        self._writer.write(response_formatter.format('OK'))

    def _get(self, key):
        value = store.get(key)
        self._writer.write(response_formatter.format(value))


        