from collections import namedtuple


class PictureData:
    def __init__(self, encoding, mimeType, pictureType, description, data):
        self.encoding = encoding
        self.mimeType = mimeType
        self.pictureType = str(pictureType)
        self.description = description
        self.data = data

    def __str__(self):
        return '\nMimeType: {0}\nPictureType: {1}\nDescription: {2}'.format(
            self.mimeType, self.pictureType, self.description)


UniqueFileId = namedtuple('UniqueFileId', ['ownerId', 'identifier'])

MPEGLocationLookuptable = namedtuple('MPEGLocationLookuptable',
                                     ['framesBetweenRef', 'bytesBetweenRef',
                                      'msBetweenRef', 'bitsForByteDeviation',
                                      'bitsForMsDeviation'])


class AudioEncryption:
    def __init__(self, ownerId, previewStart, previewEnd, encinfo):
        self.ownerId = ownerId
        self.previewStart = previewStart  # in frames
        self.previewEnd = previewEnd
        self.encinfo = encinfo

    def __str__(self):
        return '\nOwnerId: {0}\nPreviewStart: {1}\n PreviewEnd: {2}'.format(
            self.ownerId, self.previewStart, self.previewEnd)


class Comment:
    def __init__(self, lang, descr, text):
        self.language = lang
        self.description = descr
        self.text = text

    def __str__(self):
        return self.text


class CommercialInfo:
    def __init__(self, enc, price, valid, url, sn, descr, picMime, logo):
        self.price = price
        self.valid = valid
        self.url = url
        self.name = sn
        self.descr = descr
        self.mime = picMime
        self.logo = logo

    def __str__(self):
        return ('\nPrice: {0}\nValidUntil: {1}\nURL: {2}\n'
                'SellerName: {3}\nDescription: {4}\nPictureType: {5}'.format(
                   self.price, self.valid, self.url, self.name, self.descr,
                   self.mime))


Popularity = namedtuple('PopularityMeter', ['Email', 'Rating', 'Counter'])

LinkedInfo = namedtuple('LinkedInfo', ['FrameID', 'URL', 'ID_and_data'])

TermsOfUse = namedtuple('TermsOfUse', ['Language', 'Terms'])

Ownership = namedtuple('Ownership', ['Price', 'Date_of_purch', 'Seller'])


class PrivateFrame:
    def __init__(self, ownerId, data):
        self.ownerId = ownerId
        self.data = data

    def __str__(self):
        return '\nOwnerId: {0}'.format(self.ownerId)


class GroupRegistration:
    def __init__(self, ownerId, symbol, data):
        self.ownerId = ownerId
        self.symbol = symbol
        self.data = data

    def __str__(self):
        return '\nOwnerId: {0}\nGroupSymbol: {1}'.format(
            self.ownerId, self.symbol)


class DefinedText:
    def __init__(self, descr, text):
        self.descr = descr
        self.text = text

    def __str__(self):
        return self.text


UnSynchLyrics =\
    namedtuple('UnsynchLyrics', ['Language', 'Description', 'Text'])

SynchLyrics =\
    namedtuple('SynchLyrics',
               ['Language', 'TimeFormat', 'Content_type', 'Description',
                'Text'])


class SynchTempoCodes:
    def __init__(self, timeFormat, tempoData):
        self.timeFormat = timeFormat
        self.tempoData = tempoData


PosSynchFrame = namedtuple('PosSynchFrame', ['TimeFormat', 'Position'])

Reverb =\
    namedtuple('Reverb',
               ['Reverb_left', 'Reverb_right', 'Reverb_bounces_left',
                'Reverb_bounces_right', 'Reverb_feedback_left_to_left',
                'Reverb_feedback_left_to_right',
                'Reverb_feedback_right_to_right',
                'Reverb_feedback_right_to_left', 'Premix_left_to_right',
                'Premix_right_to_left'])

RecommendedBufferSize =\
    namedtuple('RecommendedBufferSize', ['Buffer_size', 'Embedded_into_flag',
                                         'Offset_to_next_flag'])


class EncapsulatedObject:
    def __init__(self, enc, mime, fileName, descr, object):
        self.mime = mime
        self.fileName = fileName
        self.descr = descr
        self.object = object

    def __str__(self):
        return '\nMimeType: {0}\nFileName: {1}\nDescription: {2}'.format(
            self.mime, self.fileName, self.descr)


class EncryptionMethodRegistration:
    def __init__(self, ownerId, methodSymbol, data):
        self.ownerId = ownerId
        self.symbol = methodSymbol
        self.data = data

    def __str__(self):
        return '\nOwnerId: {0}\nSymbol: {1}'.format(
            self.ownerId, self.symbol)


Equalization =\
    namedtuple('Equalization', ['Adjustments'])

Seek = namedtuple('Seek', ['Minimum_offset_to_next_tag'])


class Sign:
    def __init__(self, symb, data):
        self.symbol = symb
        self.data = data

    def __str__(self):
        return '\nGroupSymbol: {0}'.format(self.symbol)


class EncryptedMeta:
    def __init__(self, ownerId, descr, data):
        self.ownerId = ownerId
        self.descr = descr
        self.data = data

    def __str__(self):
        return '\nOwnerId: {0}\nDescription: {1}'.format(
            self.ownerId, self.descr)


AudioSeekPointIndex =\
    namedtuple('AudioSeekPointIndex',
               ['indexed_data_start', 'indexed_data_length',
                'number_of_index_points', 'bits_per_index_point'])

Equalization2 =\
    namedtuple('Equalization2', ['interpolation_method', 'identification',
                                 'frequencies'])
EventTimeCodes =\
    namedtuple('EventTimeCodes', ['TimeFormat', 'Events'])


class RelativeVolumeAdjustment:
    def __init__(self, inc_decr, Relative_volume_change_right,
                 Relative_volume_change_left, Peak_volume_right,
                 Peak_volume_left, Relative_volume_change_right_back=None,
                 Relative_volume_change_left_back=None,
                 Peak_volume_right_back=None,
                 Peak_volume_left_back=None,
                 Relative_volume_change_center=None,
                 Peak_volume_center=None, Relative_volume_change_bass=None,
                 Peak_volume_bass=None):
        self.inc_decr = inc_decr
        self.Relative_volume_change_right = Relative_volume_change_right
        self.Relative_volume_change_left = Relative_volume_change_left
        self.Peak_volume_right = Peak_volume_right
        self.Peak_volume_left = Peak_volume_left
        self.Relative_volume_change_right_back =\
            Relative_volume_change_right_back
        self.Relative_volume_change_left_back =\
            Relative_volume_change_left_back
        self.Peak_volume_right_back = Peak_volume_right_back
        self.Peak_volume_left_back = Peak_volume_left_back
        self.Relative_volume_change_center = Relative_volume_change_center
        self.Peak_volume_center = Peak_volume_center
        self.Relative_volume_change_bass = Relative_volume_change_bass
        self.Peak_volume_bass = Peak_volume_bass


RelativeVolumeAdjustment2 =\
    namedtuple('RelativeVolumeAdjustment2', ['Identification', 'RVA2Data'])

RVA2Data = namedtuple('RVA2Data', ['channel_type', 'volume_adjustment',
                                   'peak_volume'])
