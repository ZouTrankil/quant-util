import socket
import struct
from enum import IntEnum
import select
import time

from aiclient.utils.log_util import LogUtil
from aiclient.server.protocol.dldl.buffer import Buffer


class ProcessType(IntEnum):
    ADD = 0


class RequestClient:

    def __init__(self, host_ip='0.0.0.0', port=9800, dockerContainerName: str = '', print_log=False, timeout=120):
        self.host_ip = host_ip
        self.port = int(port)
        self.dockerContainerName = dockerContainerName
        self.executeCount = 0
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.timeout = timeout

        self.printLog = print_log

    def log(self, *values: object):
        if self.printLog:
            LogUtil.info(values)

    def init(self):
        try:
            self._client.connect((self.host_ip, self.port))
            self._client.setblocking(True)
        except socket.error as e:
            print(f'RequestClient尝试连接{self.host_ip}:{self.port}失败')
            raise e

    def sendCommand(self, command):
        buffer = Buffer()
        if command:
            command.write(buffer)
        self.log('sendCommand:', buffer.buffer.hex())
        ret = self._client.sendall(buffer.buffer[0:buffer.pos])
        return ret

    def clearBuffer(self):
        self.log('clearBuffer start')
        # 设置timeout后会进入非阻塞模式
        # self._client.settimeout(0.3)
        self._client.settimeout(0.15)
        try:
            # 读取缓冲区所有数据
            while self._client.recv(1024):
                pass
        except:
            pass
        finally:
            # 结束后设置timeout为None 进入阻塞模式
            self._client.settimeout(None)
        self.log('clearBuffer end')

    def send(self, buffer: Buffer):
        ret = self._client.sendall(buffer.buffer[0:buffer.pos])
        return ret

    def receiveByte(self, length: int = 1024):
        self.log('receiveByte---> start receive')
        data = self._client.recv(length)
        self.log('receiveByte---> receive:', data)
        return data

    def receiveByteTimeout(self, length: int = 1024):
        self.log('receiveByteTimeout---> start receive')
        self._client.setblocking(0)
        ready = select.select([self._client], [], [], self.timeout)
        if ready[0]:
            data = self._client.recv(length)
            self.log('receiveByteTimeout---> receive end')
            self.log('receiveByteTimeout---> receive:', data)
            return data
        print('receiveByteTimeout----> timeout')
        raise Exception(f"socket 接收数据超时:{self.timeout}秒")

    def receive(self, length: int = 1024):
        data = self._client.recv(length)
        self.log('receive:', data)
        bufferData = Buffer(bytearray(data))
        return bufferData

    def dispose(self):
        if self._client is not None:
            self._client.close()

    def is_connect(self):
        if self._client is not None:
            return getattr(self._client, '_closed') == False
        else:
            return False
