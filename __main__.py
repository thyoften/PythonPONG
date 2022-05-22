# Python PONG
import PONG

if __name__ == '__main__':
    pong = PONG.Pong()
    while not pong.end():
        pong.update()
