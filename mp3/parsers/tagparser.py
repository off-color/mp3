import struct
import mp3
from util import information, tags
import re


ENCODING = 'ISO-8859-1'


class Header:
    def __init__(self, info):
        self.name = info[0].decode(ENCODING)
        if len(info) > 2:
            self.size = struct.unpack('>I', info[1])[0]
        else:
            self.size = struct.unpack('3s', info[1])[0]
            self.size = int.from_bytes(self.size, byteorder='big', signed=True)
        if len(info) > 2:
            self.flags = info[2].decode(ENCODING)

    def __str__(self):
        return ('Name: ' + self.name + '\n'
                + 'Size: ' + str(self.size) + '\n'
                + 'Flags: ' + self.flags)


class ParseFunctions:
    funcs = {}


def tag_parser(cls):
    cls.funcs = ParseFunctions.funcs
    ParseFunctions.funcs = {}
    return cls


@tag_parser
class TagParser:
    def __init__(self, data, struct_str, header_len, info, is_v2):
        self.data = data
        self.struct_str = struct_str
        self.header_len = header_len
        self.info = info
        self.is_v2 = is_v2

    def parse_tag(self, counter):
        name = struct.unpack_from(self.struct_str[:2],
                                  self.data, counter)[0].decode(ENCODING)

        if (name in TagParser.funcs
                and TagParser.funcs[name] is not None):
            args = self.prepare_to_parse_tag(counter)
            TagParser.funcs[name](self, *args)
            counter = args[2] + args[0].size
            return counter

        # print(self.data)
        header =\
            Header(struct.unpack_from(self.struct_str, self.data, counter))
        counter += header.size + self.header_len
        return counter

    def tag(*args):
        def tag_decorator(function):
            for arg in args:
                ParseFunctions.funcs[arg] = function

            def wrapper(self, *args, **kwargs):
                return function(self, *args, **kwargs)
            return wrapper
        return tag_decorator

    @tag('MLLT', 'MLL')
    def parse_mllt(self, header, counter, begin):
        info = struct.unpack_from('2s3s3s1s1s', self.data, counter)
        self.info[header.name] =\
            tags.MPEGLocationLookuptable(*info)

    @tag('MCDI', 'WCOM', 'WCOP', 'WOAF', 'WOAR', 'WOAS', 'WORS', 'WPAY',
         'WPUB', 'MCI', 'WAF', 'WAR', 'WAS', 'WCM', 'WCP', 'WPB')
    def parse_simple_tag(self, header, counter, begin):
        result = self.data[counter:counter+header.size]
        result = result.decode(ENCODING)
        self.add_info(header.name, result)

    def prepare_to_parse_tag(self, counter):
        header =\
            Header(struct.unpack_from(self.struct_str, self.data, counter))
        counter += self.header_len
        begin = counter
        return (header, counter, begin)

    @tag('UFID', 'UFI')
    def parse_ufid_tag(self, header, counter, begin):  # many
        owner_id, counter = read_until_zero_byte(self.data, counter)
        identifier = self.data[counter:counter+header.size]
        counter += header.size - len(owner_id) + 1
        self.add_info(header.name, tags.UniqueFileId(owner_id, identifier))

    @tag('IPLS', 'TALB', 'TBPM', 'TCOM', 'TCON', 'TCOP', 'TDAT', 'TDLY',
         'TENC', 'TEXT', 'TFLT', 'TIME', 'TIT1', 'TIT2', 'TIT3', 'TKEY',
         'TLAN', 'TLEN', 'TMED', 'TOAL', 'TOFN', 'TOLY', 'TOPE', 'TORY',
         'TOWN', 'TPE1', 'TPE2', 'TPE3', 'TPE4', 'TPOS', 'TPUB', 'TRCK',
         'TRDA', 'TRSN', 'TRSO', 'TSIZ', 'TSRC', 'TSSE', 'TYER', 'TMCL',
         'TIPL', 'TDRC', 'TDOR', 'TDEN', 'TDRL', 'TDTG', 'TSOT', 'TSST',
         'TMOO', 'TPRO', 'TSOA', 'TSOP', 'TAL', 'TBP', 'TCM', 'TCO', 'TCR',
         'TDA', 'TDY', 'TEN', 'TFT', 'TIM', 'TKE', 'TLA', 'TLE', 'TMT',
         'TOA', 'TOF', 'TOL', 'TOR', 'TOT', 'TP1', 'TP2', 'TP3', 'TP4',
         'TPA', 'TPB', 'TRC', 'TRD', 'TRK', 'TSI', 'TSS', 'TT1', 'TT2',
         'TT3', 'TXT', 'TYE', 'IPL')
    def parse_text_frame(self, header, counter, begin):
        encoding_bit = self.data[counter]
        encoding = information.encoding[encoding_bit]
        self.info[header.name] = self.data[counter:counter+header.size][1:]
        self.info[header.name] =\
            self.decode_str(self.info[header.name], encoding)
        self.info[header.name] = self.info[header.name].replace('\x00', '')

    @tag('APIC', 'PIC')
    def parse_picture_frame(self, header, counter, begin):  # many
        encoding_bit, counter = read_data('B', self.data, counter)
        encoding = information.encoding[encoding_bit]

        if self.is_v2:
            mime_type, counter = read_data('3s', self.data, counter)
        else:
            mime_type, counter = read_until_zero_byte(self.data, counter)

        pic_type = information.picture_type[self.data[counter]]
        counter += 1
        description, counter = read_until_zero_byte(self.data, counter)
        data = self.data[counter:begin+header.size]
        pic = tags.PictureData(encoding,
                               self.decode_str(mime_type, encoding),
                               pic_type,
                               self.decode_str(description, encoding),
                               data)

        self.add_info(header.name, pic)

    @tag('AENC', 'CRA')
    def parse_encryption_tag(self, header, counter, begin):  # many
        owner_id, counter = read_until_zero_byte(self.data, counter)
        preview_start, preview_end, counter =\
            read_data('2s2s', self.data, counter)
        encinfo = self.data[counter:begin+header.size]
        result =\
            tags.AudioEncryption(owner_id, preview_start, preview_end, encinfo)
        self.add_info(header.name, result)

    @tag('COMM', 'COM')
    def parse_comment(self, header, counter, begin):  # many
        enc, lang, counter = read_data('B3s', self.data, counter)
        enc = information.encoding[enc]
        descr, counter = read_until_zero_byte(self.data, counter)
        text = self.decode_str(self.data[counter:begin+header.size], enc)
        comment = tags.Comment(lang, self.decode_str(descr, enc), text)
        self.add_info(header.name, comment)

    @tag('COMR')
    def parse_commercial_tag(self, header, counter, begin):  # many
        enc, counter = read_data('B', self.data, counter)
        enc = information.encoding[enc]
        price, counter = read_until_zero_byte(self.data, counter)
        date, counter = read_data('8s', self.data, counter)
        url, counter = read_until_zero_byte(self.data, counter)
        counter += 1
        name, counter = read_until_zero_byte(self.data, counter)
        descr, counter = read_until_zero_byte(self.data, counter)
        mime_type, counter = read_until_zero_byte(self.data, counter)
        logo = self.data[counter:begin+header.size]

        result =\
            tags.CommercialInfo(enc, price, date, url,
                                self.decode_str(name, enc),
                                self.decode_str(descr, enc),
                                information.logotype[mime_type], logo)
        self.add_info(header.name, result)

    @tag('PCNT', 'CNT')
    def parse_play_counter(self, header, counter, begin):
        self.info[header.name] =\
            int.from_bytes(self.data[counter:begin+header.size],
                           byteorder='big', signed=True)

    @tag('POPM', 'POP')
    def parse_popularity_meter(self, header, counter, begin):  # many
        email, counter = read_until_zero_byte(self.data, counter)
        rating, counter = read_data('1s', self.data, counter)
        play_count =\
            int.from_bytes(self.data[counter:begin+header.size],
                           byteorder='big', signed=True)
        self.add_info(header.name, tags.Popularity(email, rating, play_count))

    @tag('LINK', 'LNK')
    def parse_link(self, header, counter, begin):  # many
        frame_id, counter = read_data('3s', self.data, counter)
        url, counter = read_until_zero_byte(self.data, counter)
        data = sel.data[counter:begin+header.size]
        self.add_info(header.name, tags.LinkedInfo(frame_id, url, data))

    @tag('USER')
    def parse_user_tag(self, header, counter, begin):  # many
        enc, lang, counter = read_data('B3s', self.data, counter)
        enc = information.encoding[enc]
        data = self.decode_str(self.data[counter:begin+header.size], enc)
        self.add_info(header.name, tags.TermsOfUse(lang, data))

    @tag('OWNE')
    def parse_ownership(self, header, counter, begin):
        enc, counter = read_data('B', self.data, counter)
        enc = information.encoding[enc]
        price, counter = read_until_zero_byte(self.data, counter)
        date, counter = read_data('8s', self.data, counter)
        seller =\
            self.decode_str(self.data[counter:begin+header.size], enc)

        self.info[header.name] = tags.Ownership(price, date, seller)

    @tag('PRIV')
    def parse_private(self, header, counter, begin):
        owner, counter = read_until_zero_byte(self.data, counter)
        data = self.data[counter:begin+header.size]
        self.info[header.name] = tags.PrivateFrame(owner, data)

    @tag('GRID')
    def parse_group_id(self, header, counter, begin):  # many
        owner, counter = read_until_zero_byte(self.data, counter)
        symbol, counter = read_data('1s', self.data, counter)
        data = self.data[counter:begin+header.size]
        self.add_info(header.name, tags.GroupRegistrtion(owner, symbol, data))

    @tag('TXXX', 'WXXX', 'TXX', 'WXX')
    def parse_defined_text(self, header, counter, begin):  # many
        enc, counter = read_data('?', self.data, counter)
        enc = information.encoding[enc]
        descr, counter = read_until_zero_byte(self.data, counter)
        data = self.decode_str(self.data[counter:begin+header.size], enc)
        self.add_info(header.name, tags.DefinedText(descr, data))

    @tag('USLT', 'ULT')
    def parse_unsynch_lyrics(self, header, counter, begin):  # many
        enc, lang, counter = read_data('B3s', self.data, counter)
        enc = information.encoding[enc]
        descr, counter = read_until_zero_byte(self.data, counter)
        data = self.decode_str(self.data[counter:begin+header.size], enc)
        self.add_info(header.name, tags.UnSynchLyrics(lang, descr, data))

    @tag('SYLT', 'SLT')
    def parse_synch_lyrics(self, header, counter, begin):  # many
        enc, lang, format, con_type, counter =\
            read_data('B3s1s1s', self.data, counter)
        enc = information.encoding[enc]
        format = information.format[format]
        con_type = information.content[con_type]
        descr, counter = read_until_zero_byte(self.data, counter)
        data = self.decode_str(self.data[counter:begin+header.size], enc)

        self.add_info(header.name,
                      tags.SynchLyrics(lang, format, con_type, descr, data))

    @tag('SYTC', 'STC')
    def parse_synch_tempo_codes(self, header, counter, begin):
        format, counter = read_data('B', self.data, counter)
        format = information.format[format]
        data = self.data[counter:begin+header.size]
        self.info[header.name] = tags.SynchTempoCodes(format, data)

    @tag('POSS')
    def parse_position_synch_frame(self, header, counter, begin):
        format, pos, counter =\
            read_data('b>I', self.data[counter:begin+header.size])
        format = information.format[format]
        self.info[header.name] = tags.PosSynchFrame(format, pos)

    @tag('RVRB', 'REV')
    def parse_reverb(self, header, counter, begin):
        data =\
            struct.unpack('2s2s1s1s1s1s1s1s1s1s',
                          self.data[counter:begin+header.size])
        self.info[header.name] = tags.Reverb(*data)

    @tag('RBUF', 'BUF')
    def parse_buffer_size(self, header, counter, begin):
        if header.size >= 8:
            size, flag, offset =\
                struct.unpack('3s1s4s', self.data[counter:begin+header.size])
            self.info[header.name] =\
                tags.RecommendedBufferSize(size, flag, offset)
        else:
            size, flag =\
                struct.unpack('3s1s', self.data[counter:begin+header.size])
            self.info[header.name] =\
                tags.RecommendedBufferSize(size, flag, None)

    @tag('GEOB', 'GEO')
    def parse_encapsulated_object(self, header, counter, begin):  # many
        enc, counter = read_data('B', self.data, counter)
        enc = information.encoding[enc]
        mime, counter = read_until_zero_byte(self.data, counter)
        file_name, counter = read_until_zero_byte(self.data, counter)
        descr, counter = read_until_zero_byte(self.data, counter)
        data = self.data[counter:begin+header.size]

        self.add_info(header.name,
                      tags.EncapsulatedObject(enc, mime,
                                              self.decode_str(file_name, enc),
                                              descr, data))

    @tag('ENCR')
    def parse_encr_method_reg(self, header, counter, begin):  # many
        owner, counter = read_until_zero_byte(self.data, counter)
        symbol, counter = read_data('1s', self.data, counter)
        data = self.data[counter:begin+header.size]
        self.add_info(header.name,
                      tags.EncryptionMethodRegistration(owner, symbol, data))

    @tag('ETCO', 'ETC')
    def parse_event_time_codes(self, header, counter, begin):
        format, counter = read_data('B', self.data, counter)
        format = information.format[format]
        events = {}

        while counter < begin + header.size:
            event, stamp, counter = read_data('BI', self.data, counter)
            event = information.events[event]
            events[stamp] = event

        self.info[header.name] = tags.EventTimeCodes(format, events)

    @tag('EQUA', 'EQU')
    def parse_equalization(self, header, counter, begin):
        count, inc_and_freq = struct.unpack_from('b2s', self.data, counter)
        count /= 8
        adjustments = []

        while counter < begin + header.size:
            bits = frameparser.FrameParser.bytes_to_bits(inc_and_freq)
            inc, frequency = bit_struct.unpack('1i15i', bits)
            adjustment = self.data[counter:counter+count]
            counter += count + 3
            adjustments.append((inc, frequency, adjustment))

        self.info[header.name] = tags.Equalization(adjustments)

    @tag('RVAD', 'RVA')
    def parse_relative_volume(self, header, counter, begin):
        inc_or_decr, count, counter = read_data('1sB', self.data, counter)
        count /= 8
        format = '{0}s{0}s{0}s{0}s'.format(count)
        change_right, change_left, peak_right, peak_left, counter =\
            read_data(format, self.data, counter)
        result = [change_right, change_left, peak_right, peak_left]

        if counter < begin + header.size:
            right_back, left_back, peak_right_back, peak_left_back, counter =\
               read_data(format, self.data, counter)
            result += [right_back, left_back, peak_right_back, peak_left_back]
            if counter < begin + header.size:
                center, peak_center, counter =\
                   read_data(format[:2], self.data, counter)
                result += [center, peak_center]
                if counter < begin + header.size:
                    bass, peak_bass, counter =\
                        read_data(format[:2], self.data, counter)
                    result += [bass, peak_bass]

        if len(result) < 8:
            length = len(result)
            result += [None for _ in range(8 - length)]

        self.info[header.name] =\
            tags.RelativeVolumeAdjustment(*result)

    @tag('EQU2')
    def parse_equalization_2(self, header, counter, begin):  # many
        interpolation_method, counter = read_data('B', self.data, counter)
        interpolation_method =\
            information.interpolation_method[interpolation_method]
        id, counter = read_until_zero_byte(self.data, counter)
        frequencies = {}

        while counter < begin + header.size:
            freq, vol_adj, counter = read_data('Hh', self.data, counter)
            frequencies[freq] = vol_adj

        self.add_info(header.name,
                      tags.Equalization2(interpolation_method,
                                         id, frequencies))

    @tag('RVA2')
    def parse_relative_volume_2(self, header, counter, begin):  # many
        id, counter = read_until_zero_byte(self.data, counter)
        info = []

        while counter < begin + header.size:
            ch_type, volume, count, counter =\
                read_data('BhB', self.data, counter)
            count /= 8
            ch_type = information.channel_type[ch_type]
            peak_volume, counter =\
                read_data('{0}s'.format(count), self.data, counter)
            info.append(tags.RVA2Data(ch_type, volume, peak_volume))

        self.add_info(header.name, tags.RelativeVolumeAdjustment2(id, info))

    @tag('SEEK')
    def parse_seek(self, header, counter, begin):
        offset = struct.unpack_from('i', self.data, counter)
        self.info[header.name] = tags.Seek(offset)

    @tag('SIGN')
    def parse_sign(self, header, counter, begin):  # many
        symbol, counter = read_data('1s', self.data, counter)
        data = self.data[counter:begin+header.size]
        self.add_info(header.name, tags.Sign(symbol, data))

    @tag('ASPI')
    def parse_audio_seek_point_index(self, header, counter, begin):
        result = struct.unpack_from('IIHb', self.data, counter)
        self.info[header.name] = tags.AudioSeekPointIndex(*result)

    @tag('CRM')
    def parse_encr_meta_frame(self, header, counter, begin):
        owner, counter = read_until_zero_byte(self.data, counter)
        descr, counter = read_until_zero_byte(self.data, counter)
        data = self.data[counter:begin+header.size]
        self.info[header.name] = tags.EncryptedMeta(owner, descr, data)

    @tag('TCO')
    def parse_genre(self, header, counter, begin):
        encoding_bit, counter = read_data('B', self.data, counter)
        enc = information.encoding[encoding_bit]
        result =\
            self.data[counter:begin+header.size].decode(enc)
        result = re.findall(r'\((\d+)\)', result)[0]
        self.info[header.name] = information.genres[int(result)]

    def add_info(self, name, info):
        if name in self.info:
            if not isinstance(self.info[name], list):
                self.info[name] = [self.info[name]]
            self.info[name].append(info)
        else:
            self.info[name] = info

    def decode_str(self, string, enc):
        if enc == 'UTF-16':
            if string[0:2] == b'\xfe\xff':
                final_enc = 'UTF-16be'
            elif string[0:2] == b'\xff\xfe':
                final_enc = 'UTF-16le'
            else:
                return ''
            return string.decode(final_enc, errors='ignore')
        else:
            return string.decode(enc, errors='ignore')


def read_until_zero_byte(string, fromP=0):
    result = string[fromP:string[fromP:].find(b'\x00')+fromP]
    return (result, fromP + len(result) + 1)


def read_data(format, data, counter):
    result = struct.unpack_from(format, data, counter)
    result = list(result)
    result.append(counter + struct.calcsize(format))
    return tuple(result)
