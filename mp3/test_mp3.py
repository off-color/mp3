import unittest
from unittest.mock import patch, mock_open, call
import mp3
from util import bit_struct


ENC = 'ISO-8859-1'
ID3V23_header = b'ID3\x03\x00\x00'
ID3V22_header = b'ID3\x02\x00\x00'


def synchsafe(number):
    out, mask = (0x7F, 0x7F)
    while (mask ^ 0x7FFFFFFF):
        out = number & ~mask
        out <<= 1
        out |= number & mask
        mask = ((mask + 1) << 8) - 1
        number = out
    return out


def get_info(name, frames=False):
    info = mp3.Mp3Parser('test_data/' + name)
    if frames:
        info.get_frames_info()
    else:
        info.get_file_info()
    return info


class PicTests(unittest.TestCase):
    def test_save_pic(self):
        data = (ID3V23_header + (synchsafe(26)).to_bytes(4, byteorder='big')
                + b'APIC' + (synchsafe(14)).to_bytes(4, byteorder='big')
                + b'\x00\x00' + b'\x00PNG\x00\x01\x00picdata')
        mockOpen = mock_open(read_data=data)

        with patch('builtins.open', mockOpen, create=True):
            info = mp3.Mp3Parser('myfile')
            info.get_file_info()
            info.save_cover('mypic')

        self.assertEqual(mockOpen.call_args_list,
                         [call('myfile', 'rb'), call('mypic.PNG', 'wb')])
        mockOpen().write.assert_called_once_with(b'picdata')

    def test_save_pic_no_pic(self):
        info = get_info('notags.mp3')
        with self.assertRaises(Exception):
            info.save_cover('somefile')

    def test_save_pic_v22(self):
        data = (ID3V22_header + (synchsafe(26)).to_bytes(4, byteorder='big')
                + b'PIC' + (synchsafe(14)).to_bytes(3, byteorder='big')
                + b'\x00' + b'PNG\x00\x01\x00picdata')
        mockOpen = mock_open(read_data=data)

        with patch('builtins.open', mockOpen, create=True):
            info = mp3.Mp3Parser('myfile')
            info.get_file_info()
            info.save_cover('mypic')

        self.assertEqual(mockOpen.call_args_list,
                         [call('myfile', 'rb'), call('mypic.PNG', 'wb')])
        mockOpen().write.assert_called_once_with(b'picdata')


class BitStructTests(unittest.TestCase):
    def test_int_parse(self):
        self.assertEqual(17, bit_struct.unpack('5i', '10001')[0])

    def test_bool_parse(self):
        self.assertEqual(True, bit_struct.unpack('1b', '1')[0])

    def test_no_parse(self):
        self.assertEqual('1010', bit_struct.unpack('4n', '1010')[0])

    def test_combo(self):
        self.assertEqual([True, 0, '1'],
                         bit_struct.unpack('1b3i1n', '10001'))

    def test_divide_int(self):
        self.assertEqual((2, 2), bit_struct.unpack('4t', '1010')[0])

    def test_divide_bool(self):
        self.assertEqual((False, True), bit_struct.unpack('2r', '01')[0])

    def test_several_numbers(self):
        self.assertEqual([False, 3, '1'],
                         bit_struct.unpack('1b10i1n', '000000000111'))

    def test_more_than_ten(self):
        self.assertEqual(2792, bit_struct.unpack('12i', '101011101000')[0])


class TagsTests(unittest.TestCase):
    def test_v1_tag(self):
        info = mp3.Mp3Parser('test_data/v1tagwithnotrack.mp3')
        result = info.get_file_info()

        self.assertEqual(result.Title, 'TITLE1234567890123456789012345')
        self.assertEqual(result.Singer, 'ARTIST123456789012345678901234')
        self.assertEqual(result.Album, 'ALBUM1234567890123456789012345')
        self.assertEqual(result.Genre, 'Pop')
        self.assertEqual(result.Year, '2001')
        self.assertEqual(result.Comment, 'COMMENT123456789012345678901')
        self.assertEqual(result.Number, 0)

    def test_notag(self):
        info = get_info('notags.mp3')
        self.assertEqual({}, info.info)

    def test_v23_simple_tags(self):
        info = get_info('v23tag.mp3')
        self.assertEqual({'TIT2': 'TITLE', 'TALB': 'ALBUM', 'TPE1': 'ARTIST'},
                         info.info)

    def test_v23_url_tags(self):
        info = get_info('url_link.mp3')
        self.assertEqual([info.info['WCOM'], info.info['WOAR'],
                          info.info['WOAF'], info.info['WOAS'],
                          info.info['WORS']],
                         ['someurl' for _ in range(5)])
        self.assertEqual(info.info['WXXX'].text, 'someurl')

    def test_v22_simple_tags(self):
        info = get_info('example_mp3_file_with_id3v2_2_0.mp3')
        self.assertEqual([info.info['TT2'], info.info['TAL'],
                          info.info['TP1']],
                         [r'Blackwatch pres. Professor Okku - '
                          'Word Unspoken (DeVol Remix)',
                          'Tide:Edit:07',
                          'Blackwatch Presents Professor Okku'])


class FrameTests(unittest.TestCase):
    def test_noframes(self):
        info = get_info('no_frames.mp3', True)
        self.assertEqual([], info.frames)

    def test_frame_header(self):
        info = get_info('1_frame.mp3', True)
        self.assertEqual(1, len(info.frames))
        frame_header = info.frames[0].frame_header
        self.assertEqual(frame_header.bitRate, 128)
        self.assertEqual(frame_header.frequency, 44100)
        self.assertEqual(frame_header.mode, 'Joint stereo')

    def test_count_length(self):
        info = get_info('id3v2.4.mp3', True)
        result = info.count_length()
        self.assertAlmostEqual(result.total_seconds(), 8, delta=1)


if __name__ == '__main__':
    unittest.main()
