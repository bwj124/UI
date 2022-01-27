import serial
import binascii


class LightController:
    def __init__(self, port='COM4'):
        self.feat_ch = '$'
        self.CMD_OPEN = 1
        self.CMD_CLOSE = 2
        self.CMD_SET = 3
        self.CMD_READ = 4
        self.ser = serial.Serial('COM4')

    def parse(self, code):
        lit = [int(hex(ord(c)), 16) for c in code]
        t = None
        for i in range(len(lit)):
            if i:
                t ^= lit[i]
            else:
                t = lit[i] ^ 0
        return code + hex(t).replace('0x', '')

    def encode(self, s):
        return bytes(s, "ascii")

    def send(self, cmd, ch, data=0):
        send_chs = self.parse(f'{self.feat_ch}{cmd}{ch}0{"%02x" % data}')
        self.ser.write(self.encode(send_chs))

    def close_all(self):
        for i in range(0, 10):
            self.send(contr.CMD_SET, i, 0)


if __name__ == '__main__':
    import time

    contr = LightController(port='COM4')

    contr.send(cmd=contr.CMD_CLOSE, ch=1)

    time.sleep(0.2)
    contr.send(contr.CMD_SET, 1, 0)
    time.sleep(0.2)
    contr.send(contr.CMD_SET, 2, 56)
    time.sleep(0.2)
    contr.send(contr.CMD_SET, 2, 0)
    time.sleep(0.2)
