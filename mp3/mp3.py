#!/usr/bin/env python3

import struct
import argparse
import os
import sys
import datetime

try:
    from util import information, tags, bit_struct, player, pcm
    from parsers import tagparser, v1parser, frameparser
except Exception as e:
    sys.exit(str(e))


ENCODING = 'ISO-8859-1'


class Mp3Parser:
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            self.data = f.read()
            self.info = {}
            self.frames = []

        self.is_v2 = False
        self.is_v1 = False
        self.struct_str = '4s4s2s'
        self.header_len = 10
        self.counter = 0
        self.filename = filename

    def get_file_info(self):
        info = struct.unpack_from('3s2s1s4s', self.data)
        # print(info)

        if info[0] != b'ID3':
            self.is_v1 = True
            self.info = v1parser.parse(self)
            return v1parser.parse(self)

        if info[1][0] == 2:
            self.is_v2 = True
            self.struct_str = '3s3s'
            self.header_len = 6

        length = self.parse_synchsafe_integer(info[3])
        # print(length)
        self.counter = 10

        while self.counter < length:
            parser = tagparser.TagParser(self.data, self.struct_str,
                                         self.header_len, self.info,
                                         self.is_v2)
            self.counter = parser.parse_tag(self.counter)
        return self.info

    def get_frames_info(self):
        parser = frameparser.FrameParser(self)
        self.counter = parser.search_frame_header(self.counter)
        while self.counter < len(self.data):
            self.counter = parser.parse_frame(self.counter)

    def get_pcm_data(self):
        if not self.frames:
            return

        conv = pcm.Converter(
            self.frames[0].frame_header.frequency, self.filename,
            self.frames[0].ch_count, len(self.frames))
        array = conv.mp3_to_pcm()
        return array

    def draw_wave(self):
        if not self.frames:
            return

        drawer = pcm.WaveDrawer(
            self.frames[0].ch_count, self.count_length_sec(),
            len(self.frames), self.get_pcm_data())
        drawer.draw_wave()

    def print_file_info(self):
        if not (self.info or self.frames):
            self.get_file_info()

        if self.is_v1 and self.info:
            print(self.info)
        else:
            for item in self.info:
                self.print_tag(item)

    def print_frames_info(self):
        # print(self.frames[0])
        print(len(self.frames))
        print('Length: ' + str(self.count_length()))

    def print_tag(self, item):
        if isinstance(self.info[item], list):
            for i in self.info[item]:
                print('{}: {}'.format(information.tags[item], i))
        else:
            print('{}: {}'.format(information.tags[item], self.info[item]))

    def count_length(self):
        seconds =\
            len(self.frames) * 1152 / self.frames[0].frame_header.frequency
        return datetime.timedelta(seconds=seconds)

    def count_length_sec(self):
        return len(self.frames) * 1152 / self.frames[0].frame_header.frequency

    @staticmethod
    def parse_synchsafe_integer(number):
        return ((number[3] & 0x7f) | (number[2] & 0x7f) << 7
                | (number[1] & 0x7f) << 14 | (number[0] & 0x7f) << 21)

    def save_cover(self, filename):
        if self.is_v2:
            tag_name = 'PIC'
        else:
            tag_name = 'APIC'

        if tag_name not in self.info:
            raise Exception('File does not have cover')

        ext = self.info[tag_name].mimeType.split('/')[-1]
        if ext != '':
            ext = '.' + ext
        with open(filename + ext, 'wb') as f:
            f.write(self.info[tag_name].data)


def get_parser():
    parser = argparse.ArgumentParser(
        description='mp3 info')
    parser.add_argument('-t', '--tags', action='store_true', dest='tags',
                        help='id3 info')
    parser.add_argument('-f', '--frames', action='store_true', dest='frames',
                        help='frames info')
    parser.add_argument('-p', '--play', action='store_true', dest='play',
                        help='play mp3')
    parser.add_argument('-s', '--savecover', dest='filename', nargs='?',
                        help='save cover in file')
    parser.add_argument('-w', '--wave', action='store_true', dest='wave',
                        help='разбор аудиоданных')
    parser.add_argument('fn', metavar='FILE',
                        help='name of an archive')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    fileParser = Mp3Parser(args.fn)

    if not (args.tags or args.frames or args.play
       or args.filename or args.wave):
        parser.error('No action requested')

    if args.tags or args.filename:
        fileParser.get_file_info()
        fileParser.print_file_info()

    if args.frames:
        fileParser.get_frames_info()
        fileParser.print_frames_info()

    if args.wave:
        if not args.frames:
            fileParser.get_frames_info()
        fileParser.draw_wave()

    if args.play:
        pl = player.Player(args.fn)
        pl.play()

    if args.filename:
        fileParser.save_cover(args.filename)


if __name__ == '__main__':
    main()
