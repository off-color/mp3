import mp3
from util import information, bit_struct
from collections import namedtuple
from bitstring import Bits


class FrameParser:
    def __init__(self, mp3parser):
        self.mp3 = mp3parser

    def search_frame_header(self, counter):
        while counter < len(self.mp3.data):
            if (self.mp3.data[counter] == 255
                    and counter < len(self.mp3.data) - 1
                    and self.mp3.data[counter+1] == 251):
                return counter
            counter += 1
        return counter

    def parse_frame(self, counter):
        frame_header_data, counter = self.parse_frame_header(counter)

        frame = Mp3Frame(FrameHeader(*frame_header_data), b'')
        frame_length = int(144 * (frame.frame_header.bitRate
                           / (frame.frame_header.frequency / 1000))
                           + frame.frame_header.isPad) - 4
        frame.data = self.mp3.data[counter:counter+frame_length]

        if frame.frame_header.mode == 'Mono':
            self.parse_side_info_single(frame)
        else:
            self.parse_side_info_double(frame)

        self.mp3.frames.append(frame)
        counter += frame_length
        return counter

    def parse_frame_header(self, counter):
        bits = FrameParser.bytes_to_bits(self.mp3.data[counter:counter+4])
        result = bit_struct.unpack('1b4n2n1i1n2n2n1b1b2n', bits[15:])
        counter += 4

        result[1] = information.bitrates[result[1]]
        result[2] = information.frequencies[result[2]]
        result[5] = information.modes[result[5]]
        result = tuple(result)
        return (result, counter)

    @staticmethod
    def hex_symbol_to_binary(symbol):
        return bin(int(symbol, 16))[2:].zfill(4)

    @staticmethod
    def bytes_to_bits(bytestr):
        return Bits(bytes=bytestr, length=8*len(bytestr)).bin
        # return ''.join([bin(symb)[2:].zfill(8) for symb in bytestr])

    def parse_side_info_single(self, frame):
        frame.ch_count = 1
        self.parse_side_info_1(frame)
        if frame.main_data_begin > 0:
            pass
        else:
            frame.main_data = frame.data[17:]

    def parse_side_info_double(self, frame):
        frame.ch_count = 2
        self.parse_side_info_2(frame)
        if frame.main_data_begin > 0:
            pass
        else:
            frame.main_data = frame.data[32:]

    def parse_side_info_1(self, frame):
        data = FrameParser.bytes_to_bits(frame.data[:17])
        begin, _, scfsi = bit_struct.unpack('9i5n4i', data[:18])
        frame.main_data_begin = begin
        frame.scfsi = scfsi

        frame.granule1_info[0] = self.parse_for_granule_1(data[18:77])
        frame.granule2_info[0] = self.parse_for_granule_1(data[77:136])

    def parse_for_granule_1(self, data):
        par2_3_length, big_values, global_gain, scalefac_compress, wsf =\
            bit_struct.unpack('12i9i8i4i1b', data[:34])
        scalefac_compress = information.scalefac_compress[scalefac_compress]

        if wsf:
            region0_count = None
            region1_count = None
            block_type, mixed_block_flag, table_select, subblock_gain =\
                bit_struct.unpack('2n1b10n9n', data[34:56])
            preflag, scalefac_scale, c1table_select =\
                bit_struct.unpack('1i1b1i', data[56:])
            block_type = information.block_type[block_type]
        else:
            block_type = None
            mixed_block_flag = None
            subblock_gain = None
            table_select, region0_count, region1_count =\
                bit_struct.unpack('15n4i3i', data[34:56])
            preflag, scalefac_scale, c1table_select =\
                bit_struct.unpack('1i1b1b', data[56:])

        return GranuleInfo(par2_3_length, big_values, global_gain,
                           scalefac_compress, wsf, block_type,
                           mixed_block_flag, table_select,
                           subblock_gain, region0_count, region1_count,
                           preflag, scalefac_compress, c1table_select, None)

    def parse_side_info_2(self, frame):
        data = FrameParser.bytes_to_bits(frame.data[:32])
        begin, _, scfsi = bit_struct.unpack('9i3n8t', data[:20])
        frame.main_data_begin = begin
        frame.scfsi = scfsi

        frame.granule1_info[0], frame.granule1_info[1] =\
            self.parse_for_granule_2(data[20:138])
        frame.granule2_info[0], frame.granule2_info[1] =\
            self.parse_for_granule_2(data[138:256])

    def parse_for_granule_2(self, data):
        return [self.parse_for_granule_1(data[:59]),
                self.parse_for_granule_1(data[59:])]


class Mp3Frame:
    def __init__(self, frame_header, data):
        self.frame_header = frame_header
        if frame_header.errorProtection == 0:
            self.data = data[2:]
        else:
            self.data = data
        self.main_data_begin = None
        self.scfsi = None
        self.ch_count = 0
        self.granule1_info = [None, None]
        self.granule2_info = [None, None]
        self.granules = [self.granule1_info, self.granule2_info]
        self.main_data = None
        self.part2_length = []

    def __str__(self):
        return str(self.frame_header)


FrameHeader = namedtuple(
    'FrameHeader',
    ['errorProtection', 'bitRate', 'frequency', 'isPad', 'privBit',
     'mode', 'modeExtensions', 'isCopy', 'isOriginal', 'emphasis'])


class GranuleInfo:
    def __init__(self, par2_3_length, big_values, global_gain,
                 scalefac_compress, wsf, block_type,
                 mixed_block_flag, table_select, subblock_gain,
                 region0_count, region1_count, preflag,
                 scalefac_scale, c1table_select, huffman_data):
        self.par2_3_length = par2_3_length
        self.big_values = big_values
        self.global_gain = global_gain
        self.scalefac_compress = scalefac_compress
        self.wsf = wsf
        self.block_type = block_type
        self.mixed_block_flag = mixed_block_flag
        self.table_select = table_select
        self.subblock_gain = subblock_gain
        self.region0_count = region0_count
        self.region1_count = region1_count
        self.preflag = preflag
        self.scalefac_scale = scalefac_scale
        self.c1table_select = c1table_select
        self.huffman_data = huffman_data
        self.par2_start = 0
        self.par2_length = 0
