import struct
from util import information
from parsers import frameparser
from collections import namedtuple
import mp3


def parse(mp3fileinfo):
    if mp3fileinfo.data[-128:-125] == b'TAG':
        title, singer, album, year, comment, zero, number, genre =\
            struct.unpack_from('30s30s30s4s28s1sbb', mp3fileinfo.data,
                               -125)
        if zero != b'\x00':
            number = b''

        genre = information.genres[genre]
        parser = frameparser.FrameParser(mp3fileinfo)
        counter = parser.search_frame_header(0)

        while counter < len(mp3fileinfo.data) - 128:
            counter = parser.parse_frame(counter)

        enc = mp3.ENCODING
        return V1Info(title.decode(enc), singer.decode(enc),
                      album.decode(enc), year.decode(enc),
                      comment.decode(enc),
                      number, genre)
    if mp3fileinfo.data[-227:-223] == b'TAG+':
        return V1ExtendedInfo(
            *struct.unpack_from('90s90s90s1s30s6s6s', mp3fileinfo.data, -223))
    return {}


V1Info = namedtuple('V1Info',
                    ['Title', 'Singer', 'Album', 'Year', 'Comment', 'Number',
                     'Genre'])

V1ExtendedInfo =\
    namedtuple('V1ExtendedInfo',
               ['Title', 'Singer', 'Album', 'Speed', 'Genre', 'StartTime',
                'FinishTime'])
