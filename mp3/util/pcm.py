import subprocess as sp
import numpy as np
import matplotlib.pyplot as plot


class Converter:
    def __init__(self, frequency, filename, ch_count, frames_count):
        self.frequency = frequency
        self.filename = filename
        self.ch_count = ch_count
        self.frames_count = frames_count

    def mp3_to_pcm(self):
        cmd = ['ffmpeg',
               '-i', self.filename,
               '-f', 's16le',
               '-acodec', 'pcm_s16le',
               '-ac', str(self.ch_count),
               '-ar', str(self.frequency), '-']
        try:
            pipe = sp.Popen(
                cmd, stdout=sp.PIPE, stderr=sp.DEVNULL, bufsize=10**8)

            data = pipe.stdout.read()
            array = np.frombuffer(data, dtype='int16')
        except IOError:
            print('Install ffmpeg to use this option')
            return

        return array


class WaveDrawer:
    def __init__(self, ch_count, duration, frames_count, array):
        self.ch_count = ch_count
        self.duration = duration
        self.frames_count = frames_count
        self.array = array

    def draw_wave(self):
        width = 700
        height = 300
        dpi = 72
        compression = int(self.frames_count / width / 8)
        if not compression:
            compression = 1

        plot.figure(1, figsize=(width / dpi, height / dpi), dpi=dpi)
        plot.subplots_adjust(wspace=0, hspace=0)

        for i in range(self.ch_count):
            ch = self.array[i::self.ch_count]
            ch = ch[0::compression]

            axs = plot.subplot(2, 1, i + 1)
            axs.plot(ch)

        plot.savefig('wave', dpi=dpi)
        plot.show()
