import sys
import os
import time
import threading
import cv2
import pyprind


class CharFrame:
    ascii_char = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    # pixel to symbol
    def pixelToChar(self, luminance):
        return self.ascii_char[int(luminance / 256 * len(self.ascii_char))]

    # TO ASCII
    def convert(self, img, limitSize=-1, fill=False, wrap=False):
        if limitSize != -1 and (img.shape[0] > limitSize[1] or img.shape[1] > limitSize[0]):
            img = cv2.resize(img, limitSize, interpolation=cv2.INTER_AREA)
        ascii_frame = ''
        blank = ''
        if fill:
            blank += ' ' * (limitSize[0] - img.shape[1])
        if wrap:
            blank += '\n'
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                ascii_frame += self.pixelToChar(img[i, j])
            ascii_frame += blank
        return ascii_frame


class V2Char(CharFrame):
    charVideo = []
    timeInterval = 0.033

    def __init__(self, path):
        if path.endswith('txt'):
            self.load(path)
        else:
            self.genCharVideo(path)

    def genCharVideo(self, filepath):
        self.charVideo = []
        # Read video from open cv
        cap = cv2.VideoCapture(filepath)
        self.timeInterval = round(1 / cap.get(5), 3)
        nf = int(cap.get(7))
        print('Generate char video, please wait...')
        for i in pyprind.prog_bar(range(nf)):
            rawFrame = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
            frame = self.convert(rawFrame, os.get_terminal_size(), fill=True)
            self.charVideo.append(frame)
        cap.release()

    def export(self, filepath):
        if not self.charVideo:
            return
        with open(filepath, 'w') as f:
            for frame in self.charVideo:
            
                f.write(frame + '\n')

    def load(self, filepath):
        self.charVideo = []
        
        for i in open(filepath):
            self.charVideo.append(i[:-1])

    def play(self, stream=1):
        # Bug:
        if not self.charVideo:
            return
        if stream == 1 and os.isatty(sys.stdout.fileno()):
            self.streamOut = sys.stdout.write
            self.streamFlush = sys.stdout.flush
        elif stream == 2 and os.isatty(sys.stderr.fileno()):
            self.streamOut = sys.stderr.write
            self.streamFlush = sys.stderr.flush
        elif hasattr(stream, 'write'):
            self.streamOut = stream.write
            self.streamFlush = stream.flush
        breakflag = False

        def getChar():
            nonlocal breakflag
            try:
                import msvcrt
            except ImportError:
                import termios
                import tty
                fd = sys.stdin.fileno()

                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                if ch:
                    breakflag = True
            else:
                if msvcrt.getch():
                    breakflag = True

        # thread
        getchar = threading.Thread(target=getChar)
        # 
        getchar.daemon = True
        # 
        getchar.start()
        # 
        rows = len(self.charVideo[0]) // os.get_terminal_size()[0]
        for frame in self.charVideo:
            # 
            if breakflag:
                break
            self.streamOut(frame)
            self.streamFlush()
            time.sleep(self.timeInterval)
            # 
            self.streamOut('\033[{}A\r'.format(rows - 1))
        # 
        self.streamOut('\033[{}B\033[K'.format(rows - 1))
        # 
        for i in range(rows - 1):
            # 
            self.streamOut('\033[1A')
            #
            self.streamOut('\r\033[K')
        if breakflag:
            self.streamOut('User interrupt!\n')
        else:
            self.streamOut('Finished!\n')


if __name__ == '__main__':
    v2char = V2Char('vedio.mp4')
    v2char.play()
