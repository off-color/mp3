encoding = {0: 'ISO-8859-1',
            1: 'UTF-16',
            2: 'UTF-16BE',
            3: 'UTF-8'}

picture_type = {0:     'Other',
                1:     "32x32 pixels 'file icon' (PNG only)",
                2:     'Other file icon',
                3:     'Cover (front)',
                4:     'Cover (back)',
                5:     'Leaflet page',
                6:     'Media (e.g. lable side of CD)',
                7:     'Lead artist/lead performer/soloist',
                8:     'Artist/performer',
                9:     'Conductor',
                10:     'Band/Orchestra',
                11:     'Composer',
                12:     'Lyricist/text writer',
                13:     'Recording Location',
                14:     'During recording',
                15:     'During performance',
                16:     'Movie/video screen capture',
                17:     'A bright coloured fish',
                18:     'Illustration',
                19:     'Band/artist logotype',
                20:     'Publisher/Studio logotype'}

logotype = {0:     'Other',
            1:     'Standard CD album with other songs',
            2:     'Compressed audio on CD',
            3:     'File over the Internet',
            4:     'Stream over the Internet',
            5:     'As note sheets',
            6:     'As note sheets in a book with other sheets',
            7:     'Music on other media',
            8:     'Non-musical merchandise'}

modes = {'00': 'Stereo',
         '01': 'Joint stereo',
         '10': 'Dual channel',
         '11': 'Mono'}

bitrates = {'0000': 40,
            '0001': 32,
            '0010': 40,
            '0011': 48,
            '0100': 56,
            '0101': 64,
            '0110': 80,
            '0111': 96,
            '1000': 112,
            '1001': 128,
            '1010': 160,
            '1011': 192,
            '1100': 224,
            '1101': 256,
            '1110': 320,
            '1111': 'bad'}

frequencies = {'00': 44100,
               '01': 48000,
               '10': 32000,
               '11': 'reserv'}

format = {1: 'Absolute time, 32 bit sized, using MPEG frames as unit',
          2: 'Absolute time, 32 bit sized, using milliseconds as unit'}

content = {0:      'other',
           1:      'lyrics',
           2:      'text transcription',
           3:      'movement/part name',
           4:      'events',
           5:      'chord',
           6:      "trivia/'pop up' information"}

scale_factor_compress = {0: (0, 0),
                         1: (0, 1),
                         2: (0, 2),
                         3: (0, 3),
                         4: (3, 0),
                         5: (1, 1),
                         6: (1, 2),
                         7: (1, 3),
                         8: (2, 1),
                         9: (2, 2),
                         10: (2, 3),
                         11: (3, 1),
                         12: (3, 2),
                         13: (3, 3),
                         14: (4, 2),
                         15: (4, 3)}

tags = {'AENC':    'Audio encryption',
        'APIC':    'Attached picture',
        'COMM':    'Comments',
        'COMR':    'Commercial frame',
        'ENCR':    'Encryption method registration',
        'EQUA':    'Equalization',
        'ETCO':    'Event timing codes',
        'GEOB':    'General encapsulated object',
        'GRID':    'Group identification registration',
        'IPLS':    'Involved people list',
        'LINK':    'Linked information',
        'MCDI':    'Music CD identifier',
        'MLLT':    'MPEG location lookup table',
        'OWNE':    'Ownership frame',
        'PRIV':    'Private frame',
        'PCNT':    'Play counter',
        'POPM':    'Popularimeter',
        'POSS':    'Position synchronisation frame',
        'RBUF':    'Recommended buffer size',
        'RVAD':    'Relative volume adjustment',
        'RVRB':    'Reverb',
        'SYLT':    'Synchronized lyric/text',
        'SYTC':    'Synchronized tempo codes',
        'TALB':    'Album/Movie/Show title',
        'TBPM':    'BPM (beats per minute)',
        'TCOM':    'Composer',
        'TCON':    'Content type',
        'TCOP':    'Copyright message',
        'TDAT':    'Date',
        'TDLY':    'Playlist delay',
        'TENC':    'Encoded by',
        'TEXT':    'Lyricist/Text writer',
        'TFLT':    'File type',
        'TIME':    'Time',
        'TIT1':    'Content group description',
        'TIT2':    'Title/songname/content description',
        'TIT3':    'Subtitle/Description refinement',
        'TKEY':    'Initial key',
        'TLAN':    'Language(s)',
        'TLEN':    'Length',
        'TMED':    'Media type',
        'TOAL':    'Original album/movie/show title',
        'TOFN':    'Original filename',
        'TOLY':    'Original lyricist(s)/text writer(s)',
        'TOPE':    'Original artist(s)/performer(s)',
        'TORY':    'Original release year',
        'TOWN':    'File owner/licensee',
        'TPE1':    'Lead performer(s)/Soloist(s)',
        'TPE2':    'Band/orchestra/accompaniment',
        'TPE3':    'Conductor/performer refinement',
        'TPE4':    'Interpreted, remixed, or otherwise modified by',
        'TPOS':    'Part of a set',
        'TPUB':    'Publisher',
        'TRCK':    'Track number/Position in set',
        'TRDA':    'Recording dates',
        'TRSN':    'Internet radio station name',
        'TRSO':    'Internet radio station owner',
        'TSIZ':    'Size',
        'TSRC':    'ISRC (international standard recording code)',
        'TSSE':    'Software/Hardware and settings used for encoding',
        'TYER':    'Year',
        'TXXX':    'User defined text information frame',
        'UFID':    'Unique file identifier',
        'USER':    'Terms of use',
        'USLT':    'Unsychronized lyric/text transcription',
        'WCOM':    'Commercial information',
        'WCOP':    'Copyright/Legal information',
        'WOAF':    'Official audio file webpage',
        'WOAR':    'Official artist/performer webpage',
        'WOAS':    'Official audio source webpage',
        'WORS':    'Official internet radio station homepage',
        'WPAY':    'Payment',
        'WPUB':    'Publishers official webpage',
        'WXXX':    'User defined URL link frame',
        'BUF':     'Recommended buffer size',
        'CNT':     'Play counter',
        'COM':     'Comments',
        'CRA':     'Audio encryption',
        'CRM':     'Encrypted meta frame',
        'ETC':     'Event timing codes',
        'EQU':     'Equalization',
        'GEO':     'General encapsulated object',
        'IPL':     'Involved people list',
        'LNK':     'Linked information',
        'MCI':     'Music CD Identifier',
        'MLL':     'MPEG location lookup table',
        'PIC':     'Attached picture',
        'POP':     'Popularimeter',
        'REV':     'Reverb',
        'RVA':     'Relative volume adjustment',
        'SLT':     'Synchronized lyric/text',
        'STC':     'Synced tempo codes',
        'TAL':     'Album/Movie/Show title',
        'TBP':     'BPM (Beats Per Minute)',
        'TCM':     'Composer',
        'TCO':     'Content type',
        'TCR':     'Copyright message',
        'TDA':     'Date',
        'TDY':     'Playlist delay',
        'TEN':     'Encoded by',
        'TFT':     'File type',
        'TIM':     'Time',
        'TKE':     'Initial key',
        'TLA':     'Language(s)',
        'TLE':     'Length',
        'TMT':     'Media type',
        'TOA':     'Original artist(s)/performer(s)',
        'TOF':     'Original filename',
        'TOL':     'Original Lyricist(s)/text writer(s)',
        'TOR':     'Original release year',
        'TOT':     'Original album/Movie/Show title',
        'TP1':     ('Lead artist(s)/Lead performer(s)'
                    '/Soloist(s)/Performing group'),
        'TP2':     'Band/Orchestra/Accompaniment',
        'TP3':     'Conductor/Performer refinement',
        'TP4':     'Interpreted, remixed, or otherwise modified by',
        'TPA':     'Part of a set',
        'TPB':     'Publisher',
        'TRC':     'ISRC (International Standard Recording Code)',
        'TRD':     'Recording dates',
        'TRK':     'Track number/Position in set',
        'TSI':     'Size',
        'TSS':     'Software/hardware and settings used for encoding',
        'TT1':     'Content group description',
        'TT2':     'Title/Songname/Content description',
        'TT3':     'Subtitle/Description refinement',
        'TXT':     'Lyricist/text writer',
        'TXX':     'User defined text information frame',
        'TYE':     'Year',
        'UFI':     'Unique file identifier',
        'ULT':     'Unsychronized lyric/text transcription',
        'WAF':     'Official audio file webpage',
        'WAR':     'Official artist/performer webpage',
        'WAS':     'Official audio source webpage',
        'WCM':     'Commercial information',
        'WCP':     'Copyright/Legal information',
        'WPB':     'Publishers official webpage',
        'WXX':     'User defined URL link frame'}

genres =\
    {0:	    'Blues',
     1:	    'Classic Rock',
     2:	    'Country',
     3:	    'Dance',
     4:	    'Disco',
     5:	    'Funk',
     6:	    'Grunge',
     7:	    'Hip-Hop',
     8:	    'Jazz',
     9:	    'Metal',
     10:	'New Age',
     11:	'Oldies',
     12:	'Other',
     13:	'Pop',
     14:	'Rhythm and Blues',
     15:	'Rap',
     16:	'Reggae',
     17:	'Rock',
     18:	'Techno',
     19:	'Industrial',
     20:	'Alternative',
     21:	'Ska',
     22:	'Death Metal',
     23:	'Pranks',
     24:	'Soundtrack',
     25:	'Euro-Techno',
     26:	'Ambient',
     27:	'Trip-Hop',
     28:	'Vocal',
     29:	'Jazz & Funk',
     30:	'Fusion',
     31:	'Trance',
     32:	'Classical',
     33:	'Instrumental',
     34:	'Acid',
     35:	'House',
     36:	'Game',
     37:	'Sound Clip',
     38:	'Gospel',
     39:	'Noise',
     40:	'Alternative Rock',
     41:	'Bass',
     42:	'Soul',
     43:	'Punk',
     44:	'Space',
     45:	'Meditative',
     46:	'Instrumental Pop',
     47:	'Instrumental Rock',
     48:	'Ethnic',
     49:	'Gothic',
     50:	'Darkwave',
     51:	'Techno-Industrial',
     52:	'Electronic',
     53:	'Pop-Folk',
     54:	'Eurodance',
     55:	'Dream',
     56:	'Southern Rock',
     57:	'Comedy',
     58:	'Cult',
     59:	'Gangsta',
     60:	'Top 40',
     61:	'Christian Rap',
     62:	'Pop/Funk',
     63:	'Jungle',
     64:	'Native US',
     65:	'Cabaret',
     66:	'New Wave',
     67:	'Psychedelic',
     68:	'Rave',
     69:	'Showtunes',
     70:	'Trailer',
     71:	'Lo-Fi',
     72:	'Tribal',
     73:	'Acid Punk',
     74:	'Acid Jazz',
     75:	'Polka',
     76:	'Retro',
     77:	'Musical',
     78:	'Rock ’n’ Roll',
     79:	'Hard Rock',
     80:	'Folk',
     81:	'Folk-Rock',
     82:	'National Folk',
     83:	'Swing',
     84:	'Fast Fusion',
     85:	'Bebop',
     86:	'Latin',
     87:	'Revival',
     88:	'Celtic',
     89:	'Bluegrass',
     90:	'Avantgarde',
     91:	'Gothic Rock',
     92:	'Progressive Rock',
     93:	'Psychedelic Rock',
     94:	'Symphonic Rock',
     95:	'Slow Rock',
     96:	'Big Band',
     97:	'Chorus',
     98:	'Easy Listening',
     99:	'Acoustic',
     100:	'Humour',
     101:	'Speech',
     102:	'Chanson',
     103:	'Opera',
     104:	'Chamber Music',
     105:	'Sonata',
     106:	'Symphony',
     107:	'Booty Bass',
     108:	'Primus',
     109:	'Porn Groove',
     110:	'Satire',
     111:	'Slow Jam',
     112:	'Club',
     113:	'Tango',
     114:	'Samba',
     115:	'Folklore',
     116:	'Ballad',
     117:	'Power Ballad',
     118:	'Rhythmic Soul',
     119:	'Freestyle',
     120:	'Duet',
     121:	'Punk Rock',
     122:	'Drum Solo',
     123:	'A cappella',
     124:	'Euro-House',
     125:	'Dance Hall',
     126:	'Goa',
     127:	'Drum & Bass',
     128:	'Club-House',
     129:	'Hardcore Techno',
     130:	'Terror',
     131:	'Indie',
     132:	'BritPop',
     133:	'Negerpunk',
     134:	'Polsk Punk',
     135:	'Beat',
     136:	'Christian Gangsta Rap',
     137:	'Heavy Metal',
     138:	'Black Metal',
     139:	'Crossover',
     140:	'Contemporary Christian',
     141:	'Christian Rock',
     142:	'Merengue',
     143:	'Salsa',
     144:	'Thrash Metal',
     145:	'Anime',
     146:	'Jpop',
     147:	'Synthpop',
     148:	'Abstract',
     149:	'Art Rock',
     150:	'Baroque',
     151:	'Bhangra',
     152:	'Big Beat',
     153:	'Breakbeat',
     154:	'Chillout',
     155:	'Downtempo',
     156:	'Dub',
     157:	'EBM',
     158:	'Eclectic',
     159:	'Electro',
     160:	'Electroclash',
     161:	'Emo',
     162:	'Experimental',
     163:	'Garage',
     164:	'Global',
     165:	'IDM',
     166:	'Illbient',
     167:	'Industro-Goth',
     168:	'Jam Band',
     169:	'Krautrock',
     170:	'Leftfield',
     171:	'Lounge',
     172:	'Math Rock',
     173:	'New Romantic',
     174:	'Nu-Breakz',
     175:	'Post-Punk',
     176:	'Post-Rock',
     177:	'Psytrance',
     178:	'Shoegaze',
     179:	'Space Rock',
     180:	'Trop Rock',
     181:	'World Music',
     182:	'Neoclassical',
     183:	'Audiobook',
     184:	'Audio Theatre',
     185:	'Neue Deutsche Welle',
     186:	'Podcast',
     187:	'Indie-Rock',
     188:	'G-Funk',
     189:	'Dubstep',
     190:	'Garage Rock',
     191:	'Psybient'}

scalefac_compress =\
    {0: (0, 0),
     1: (0, 1),
     2: (0, 2),
     3: (0, 3),
     4: (3, 0),
     5: (1, 1),
     6: (1, 2),
     7: (1, 3),
     8: (2, 1),
     9: (2, 2),
     10: (2, 3),
     11: (3, 1),
     12: (3, 2),
     13: (3, 3),
     14: (4, 2),
     15: (4, 3)}

block_type =\
    {'00': 'forbidden',
     '01': 'start',
     '10': '3 short windows',
     '11': 'end'}

interpolation_method = {0:  'Band', 1:  'Linear'}

events =\
    {0:     'padding (has no meaning)',
     1:     'end of initial silence',
     2:     'intro start',
     3:     'mainpart start',
     4:     'outro start',
     5:     'outro end',
     6:     'verse start',
     7:     'refrain start',
     8:     'interlude start',
     9:     'theme start',
     10:     'variation start',
     11:     'key change',
     12:     'time change',
     13:     'momentary unwanted noise (Snap, Crackle & Pop)',
     14:     'sustained noise',
     15:     'sustained noise end',
     16:     'intro end',
     17:     'mainpart end',
     18:     'verse end',
     19:     'refrain end',
     20:     'theme end',
     224:    'not predefined sync 0-F',
     225:    'not predefined sync 0-F',
     226:    'not predefined sync 0-F',
     227:    'not predefined sync 0-F',
     228:    'not predefined sync 0-F',
     229:    'not predefined sync 0-F',
     230:    'not predefined sync 0-F',
     231:    'not predefined sync 0-F',
     232:    'not predefined sync 0-F',
     233:    'not predefined sync 0-F',
     234:    'not predefined sync 0-F',
     235:    'not predefined sync 0-F',
     236:    'not predefined sync 0-F',
     237:    'not predefined sync 0-F',
     238:    'not predefined sync 0-F',
     239:    'not predefined sync 0-F',
     253:    'audio end (start of silence)',
     254:    'audio file ends',
     255:    'one more byte of events follows'}

channel_type =\
    {0:  'Other',
     1:  'Master volume',
     2:  'Front right',
     3:  'Front left',
     4:  'Back right',
     5:  'Back left',
     6:  'Front centre',
     7:  'Back centre',
     8:  'Subwoofer'}

scale_band_indicies = {
        44100: {
            'L': [0, 4, 8, 12, 16, 20, 24, 30, 36, 44, 52, 62, 74, 90, 110,
                  134, 162, 196, 238, 288, 342, 418, 576],
            'S': [0, 4, 8, 12, 16, 22, 30, 40, 52, 66, 84, 106, 136, 192],
        },
        48000: {
            'L': [0, 4, 8, 12, 16, 20, 24, 30, 36, 42, 50, 60, 72, 88, 106,
                  128, 156, 190, 230, 276, 330, 384, 576],
            'S': [0, 4, 8, 12, 16, 22, 28, 38, 50, 64, 80, 100, 126, 192],
        },
        32000: {
            'L': [0, 4, 8, 12, 16, 20, 24, 30, 36, 44, 54, 66, 82, 102, 126,
                  156, 194, 240, 296, 364, 448, 550, 576],
            'S': [0, 4, 8, 12, 16, 22, 30, 42, 58, 78, 104, 138, 180, 192],
        },
    }
