import copy
import skin
from enigma import eListboxPythonMultiContent, gFont, getPrevAsciiCode, RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, RT_VALIGN_TOP, RT_VALIGN_CENTER, RT_VALIGN_BOTTOM, BT_SCALE
from Components.ActionMap import HelpableNumberActionMap
from Components.Input import Input
from Components.Label import Label
from Components.Language import language
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from Components.Sources.StaticText import StaticText
from Screens.ChoiceBox import ChoiceBox
from Screens.HelpMenu import HelpableScreen
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from Tools.NumericalTextInput import NumericalTextInput

class VirtualKeyBoardList(MenuList):

    def __init__(self, list, enableWrapAround = False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        font = skin.fonts.get('VirtualKeyBoard', ('Regular', 28, 45))
        self.l.setFont(0, gFont(font[0], font[1]))
        self.l.setFont(1, gFont(font[0], font[1] * 5 / 9))
        self.l.setItemHeight(font[2])


class VirtualKeyBoardEntryComponent:

    def __init__(self):
        pass


VKB_DONE_ICON = 0
VKB_ENTER_ICON = 1
VKB_OK_ICON = 2
VKB_SAVE_ICON = 3
VKB_SEARCH_ICON = 4
VKB_DONE_TEXT = 5
VKB_ENTER_TEXT = 6
VKB_OK_TEXT = 7
VKB_SAVE_TEXT = 8
VKB_SEARCH_TEXT = 9
SPACE = u'SPACEICON'

class VirtualKeyBoard(Screen, HelpableScreen):

    def __init__(self, session, title = _('Virtual KeyBoard Text:'), text = '', maxSize = False, visible_width = False, type = Input.TEXT, currPos = -1, allMarked = False, style = VKB_ENTER_ICON):
        Screen.__init__(self, session)
        HelpableScreen.__init__(self)
        self.setTitle(_('Virtual keyboard'))
        prompt = title
        greenLabel, self.green = {VKB_DONE_ICON: ('Done', u'ENTERICON'),
         VKB_ENTER_ICON: ('Enter', u'ENTERICON'),
         VKB_OK_ICON: ('OK', u'ENTERICON'),
         VKB_SAVE_ICON: ('Save', u'ENTERICON'),
         VKB_SEARCH_ICON: ('Search', u'ENTERICON'),
         VKB_DONE_TEXT: ('Done', _('Done')),
         VKB_ENTER_TEXT: ('Done', _('Enter')),
         VKB_OK_TEXT: ('OK', _('OK')),
         VKB_SAVE_TEXT: ('Save', _('Save')),
         VKB_SEARCH_TEXT: ('Search', _('Search'))}.get(style, ('Enter', u'ENTERICON'))
        self.bg = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_bg.png'))
        self.bg_l = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_bg_l.png'))
        self.bg_m = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_bg_m.png'))
        self.bg_r = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_bg_r.png'))
        self.sel_l = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_sel_l.png'))
        self.sel_m = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_sel_m.png'))
        self.sel_r = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_sel_r.png'))
        key_red_l = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_red_l.png'))
        key_red_m = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_red_m.png'))
        key_red_r = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_red_r.png'))
        key_green_l = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_green_l.png'))
        key_green_m = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_green_m.png'))
        key_green_r = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_green_r.png'))
        key_yellow_l = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_yellow_l.png'))
        key_yellow_m = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_yellow_m.png'))
        key_yellow_r = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_yellow_r.png'))
        key_blue_l = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_blue_l.png'))
        key_blue_m = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_blue_m.png'))
        key_blue_r = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_blue_r.png'))
        key_backspace = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_backspace.png'))
        key_clear = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_clear.png'))
        key_delete = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_delete.png'))
        key_enter = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_enter.png'))
        key_exit = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_exit.png'))
        key_first = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_first.png'))
        key_last = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_last.png'))
        key_left = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_left.png'))
        key_locale = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_locale.png'))
        key_right = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_right.png'))
        key_shift = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_shift.png'))
        key_shift0 = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_shift0.png'))
        key_shift1 = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_shift1.png'))
        key_shift2 = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_shift2.png'))
        key_shift3 = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_shift3.png'))
        key_space = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_space.png'))
        key_space_alt = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, 'buttons/vkey_space_alt.png'))
        self.keyHighlights = {u'EXIT': (key_red_l, key_red_m, key_red_r),
         u'EXITICON': (key_red_l, key_red_m, key_red_r),
         u'DONE': (key_green_l, key_green_m, key_green_r),
         u'ENTER': (key_green_l, key_green_m, key_green_r),
         u'ENTERICON': (key_green_l, key_green_m, key_green_r),
         u'OK': (key_green_l, key_green_m, key_green_r),
         u'SAVE': (key_green_l, key_green_m, key_green_r),
         u'SHIFT': (key_yellow_l, key_yellow_m, key_yellow_r),
         u'SHIFTICON': (key_yellow_l, key_yellow_m, key_yellow_r),
         u'CAPS': (key_blue_l, key_blue_m, key_blue_r),
         u'LOCK': (key_blue_l, key_blue_m, key_blue_r),
         u'CAPSLOCK': (key_blue_l, key_blue_m, key_blue_r),
         u'CAPSLOCKICON': (key_blue_l, key_blue_m, key_blue_r)}
        self.shiftMsgs = [_('Lower case'),
         _('Upper case'),
         _('Special 1'),
         _('Special 2')]
        self.keyImages = [{u'BACKSPACEICON': key_backspace,
          u'CAPSLOCKICON': key_shift0,
          u'CLEARICON': key_clear,
          u'DELETEICON': key_delete,
          u'ENTERICON': key_enter,
          u'EXITICON': key_exit,
          u'FIRSTICON': key_first,
          u'LASTICON': key_last,
          u'LOCALEICON': key_locale,
          u'LEFTICON': key_left,
          u'RIGHTICON': key_right,
          u'SHIFTICON': key_shift,
          u'SPACEICON': key_space,
          u'SPACEICONALT': key_space_alt},
         {u'BACKSPACEICON': key_backspace,
          u'CAPSLOCKICON': key_shift1,
          u'CLEARICON': key_clear,
          u'DELETEICON': key_delete,
          u'ENTERICON': key_enter,
          u'EXITICON': key_exit,
          u'FIRSTICON': key_first,
          u'LASTICON': key_last,
          u'LEFTICON': key_left,
          u'LOCALEICON': key_locale,
          u'RIGHTICON': key_right,
          u'SHIFTICON': key_shift,
          u'SPACEICON': key_space,
          u'SPACEICONALT': key_space_alt},
         {u'BACKSPACEICON': key_backspace,
          u'CAPSLOCKICON': key_shift2,
          u'CLEARICON': key_clear,
          u'DELETEICON': key_delete,
          u'ENTERICON': key_enter,
          u'EXITICON': key_exit,
          u'FIRSTICON': key_first,
          u'LASTICON': key_last,
          u'LEFTICON': key_left,
          u'LOCALEICON': key_locale,
          u'RIGHTICON': key_right,
          u'SHIFTICON': key_shift,
          u'SPACEICON': key_space,
          u'SPACEICONALT': key_space_alt},
         {u'BACKSPACEICON': key_backspace,
          u'CAPSLOCKICON': key_shift3,
          u'CLEARICON': key_clear,
          u'DELETEICON': key_delete,
          u'ENTERICON': key_enter,
          u'EXITICON': key_exit,
          u'FIRSTICON': key_first,
          u'LASTICON': key_last,
          u'LEFTICON': key_left,
          u'LOCALEICON': key_locale,
          u'RIGHTICON': key_right,
          u'SHIFTICON': key_shift,
          u'SPACEICON': key_space,
          u'SPACEICONALT': key_space_alt}]
        self.cmds = {u'': 'pass',
         u'ALL': "self['text'].markAll()",
         u'ALLICON': "self['text'].markAll()",
         u'BACK': "self['text'].deleteBackward()",
         u'BACKSPACE': "self['text'].deleteBackward()",
         u'BACKSPACEICON': "self['text'].deleteBackward()",
         u'BLANK': 'pass',
         u'CAPS': 'self.capsLockSelected()',
         u'CAPSLOCK': 'self.capsLockSelected()',
         u'CAPSLOCKICON': 'self.capsLockSelected()',
         u'CLEAR': "self['text'].deleteAllChars()\nself['text'].update()",
         u'CLEARICON': "self['text'].deleteAllChars()\nself['text'].update()",
         u'CLR': "self['text'].deleteAllChars()\nself['text'].update()",
         u'DEL': "self['text'].deleteForward()",
         u'DELETE': "self['text'].deleteForward()",
         u'DELETEICON': "self['text'].deleteForward()",
         u'DONE': 'self.save()',
         u'ENTER': 'self.save()',
         u'ENTERICON': 'self.save()',
         u'ESC': 'self.cancel()',
         u'EXIT': 'self.cancel()',
         u'EXITICON': 'self.cancel()',
         u'FIRST': "self['text'].home()",
         u'FIRSTICON': "self['text'].home()",
         u'LAST': "self['text'].end()",
         u'LASTICON': "self['text'].end()",
         u'LEFT': "self['text'].left()",
         u'LEFTICON': "self['text'].left()",
         u'LOC': 'self.localeMenu()',
         u'LOCALE': 'self.localeMenu()',
         u'LOCALEICON': 'self.localeMenu()',
         u'LOCK': 'self.capsLockSelected()',
         u'OK': 'self.save()',
         u'RIGHT': "self['text'].right()",
         u'RIGHTICON': "self['text'].right()",
         u'SAVE': 'self.save()',
         u'SHIFT': 'self.shiftSelected()',
         u'SHIFTICON': 'self.shiftSelected()',
         u'SPACE': "self['text'].char(' '.encode('UTF-8'))",
         u'SPACEICON': "self['text'].char(' '.encode('UTF-8'))",
         u'SPACEICONALT': "self['text'].char(' '.encode('UTF-8'))"}
        self.footer = [u'EXITICON',
         u'LEFTICON',
         u'RIGHTICON',
         SPACE,
         SPACE,
         SPACE,
         SPACE,
         SPACE,
         SPACE,
         SPACE,
         u'SHIFTICON',
         u'LOCALEICON',
         u'CLEARICON',
         u'DELETEICON']
        self.czech = [[[u';',
           u'+',
           u'\u011b',
           u'\u0161',
           u'\u010d',
           u'\u0159',
           u'\u017e',
           u'\xfd',
           u'\xe1',
           u'\xed',
           u'\xe9',
           u'=',
           u'',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'q',
           u'w',
           u'e',
           u'r',
           u't',
           u'z',
           u'u',
           u'i',
           u'o',
           u'p',
           u'\xfa',
           u'(',
           u')'],
          [u'LASTICON',
           u'a',
           u's',
           u'd',
           u'f',
           u'g',
           u'h',
           u'j',
           u'k',
           u'l',
           u'\u016f',
           u'\xa7',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'\\',
           u'y',
           u'x',
           u'c',
           u'v',
           u'b',
           u'n',
           u'm',
           u',',
           '.',
           u'-',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'.',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u'%',
           u"'",
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'Q',
           u'W',
           u'E',
           u'R',
           u'T',
           u'Z',
           u'U',
           u'I',
           u'O',
           u'P',
           u'/',
           u'(',
           u')'],
          [u'LASTICON',
           u'A',
           u'S',
           u'D',
           u'F',
           u'G',
           u'H',
           u'J',
           u'K',
           u'L',
           u'"',
           u'!',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'|',
           u'Y',
           u'X',
           u'C',
           u'V',
           u'B',
           u'N',
           u'M',
           u'?',
           u':',
           u'_',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'\xb0',
           u'~',
           u'\u011a',
           u'\u0160',
           u'\u010c',
           u'\u0158',
           u'\u017d',
           u'\xdd',
           u'\xc1',
           u'\xcd',
           u'\xc9',
           u'`',
           u"'",
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\\',
           u'|',
           u'\u20ac',
           u'\u0165',
           u'\u0164',
           u'\u0148',
           u'\u0147',
           u'\xf3',
           u'\xd3',
           u'\xda',
           u'\xf7',
           u'\xd7',
           u'\xa4'],
          [u'LASTICON',
           u'',
           u'\u0111',
           u'\xd0',
           u'[',
           u']',
           u'\u010f',
           u'\u010e',
           u'\u0142',
           u'\u0141',
           u'\u016e',
           u'\xdf',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'',
           u'',
           u'#',
           u'&',
           u'@',
           u'{',
           u'}',
           u'$',
           u'<',
           u'>',
           u'*',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.english = [[[u'`',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u'-',
           u'=',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'q',
           u'w',
           u'e',
           u'r',
           u't',
           u'y',
           u'u',
           u'i',
           u'o',
           u'p',
           u'[',
           u']',
           u'\\'],
          [u'LASTICON',
           u'a',
           u's',
           u'd',
           u'f',
           u'g',
           u'h',
           u'j',
           u'k',
           u'l',
           u';',
           u"'",
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'CAPSLOCKICON',
           u'z',
           u'x',
           u'c',
           u'v',
           u'b',
           u'n',
           u'm',
           u',',
           u'.',
           u'/',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'~',
           u'!',
           u'@',
           u'#',
           u'$',
           u'%',
           u'^',
           u'&',
           u'*',
           u'(',
           u')',
           u'_',
           u'+',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'Q',
           u'W',
           u'E',
           u'R',
           u'T',
           u'Y',
           u'U',
           u'I',
           u'O',
           u'P',
           u'{',
           u'}',
           u'|'],
          [u'LASTICON',
           u'A',
           u'S',
           u'D',
           u'F',
           u'G',
           u'H',
           u'J',
           u'K',
           u'L',
           u':',
           u'"',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'CAPSLOCKICON',
           u'Z',
           u'X',
           u'C',
           u'V',
           u'B',
           u'N',
           u'M',
           u'<',
           u'>',
           u'?',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.french = [[[u'\xb2',
           u'&',
           u'\xe9',
           u'"',
           u"'",
           u'(',
           u'-',
           u'\xe8',
           u'_',
           u'\xe7',
           u'\xe0',
           u')',
           u'=',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'a',
           u'z',
           u'e',
           u'r',
           u't',
           u'y',
           u'u',
           u'i',
           u'o',
           u'p',
           u'^',
           u'$',
           u'*'],
          [u'LASTICON',
           u'q',
           u's',
           u'd',
           u'f',
           u'g',
           u'h',
           u'j',
           u'k',
           u'l',
           u'm',
           u'\xf9',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'<',
           u'w',
           u'x',
           u'c',
           u'v',
           u'b',
           u'n',
           u',',
           u';',
           u':',
           u'!',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u'\xb0',
           u'+',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'A',
           u'Z',
           u'E',
           u'R',
           u'T',
           u'Y',
           u'U',
           u'I',
           u'O',
           u'P',
           u'\xa8',
           u'\xa3',
           u'\xb5'],
          [u'LASTICON',
           u'Q',
           u'S',
           u'D',
           u'F',
           u'G',
           u'H',
           u'J',
           u'K',
           u'L',
           u'M',
           u'%',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'>',
           u'W',
           u'X',
           u'C',
           u'V',
           u'B',
           u'N',
           u'?',
           u'.',
           u'/',
           u'\xa7',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'',
           u'',
           u'~',
           u'#',
           u'{',
           u'[',
           u'|',
           u'`',
           u'\\',
           u'^',
           u'@',
           u']',
           u'}',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'',
           u'',
           u'\u20ac',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'\xa4',
           u''],
          [u'LASTICON',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'',
           u'',
           u'\xe2',
           u'\xea',
           u'\xee',
           u'\xf4',
           u'\xfb',
           u'\xe4',
           u'\xeb',
           u'\xef',
           u'\xf6',
           u'\xfc',
           u'',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'',
           u'\xe0',
           u'\xe8',
           u'\xec',
           u'\xf2',
           u'\xf9',
           u'\xe1',
           u'\xe9',
           u'\xed',
           u'\xf3',
           u'\xfa',
           u'',
           u''],
          [u'LASTICON',
           u'',
           u'\xc2',
           u'\xca',
           u'\xce',
           u'\xd4',
           u'\xdb',
           u'\xc4',
           u'\xcb',
           u'\xcf',
           u'\xd6',
           u'\xdc',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'',
           u'\xc0',
           u'\xc8',
           u'\xcc',
           u'\xd2',
           u'\xd9',
           u'\xc1',
           u'\xc9',
           u'\xcd',
           u'\xd3',
           u'\xda',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.german = [[[u'^',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u'\xdf',
           u"'",
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'q',
           u'w',
           u'e',
           u'r',
           u't',
           u'z',
           u'u',
           u'i',
           u'o',
           u'p',
           u'\xfc',
           u'+',
           u'#'],
          [u'LASTICON',
           u'a',
           u's',
           u'd',
           u'f',
           u'g',
           u'h',
           u'j',
           u'k',
           u'l',
           u'\xf6',
           u'\xe4',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'<',
           u'y',
           u'x',
           u'c',
           u'v',
           u'b',
           u'n',
           u'm',
           u',',
           '.',
           u'-',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'\xb0',
           u'!',
           u'"',
           u'\xa7',
           u'$',
           u'%',
           u'&',
           u'/',
           u'(',
           u')',
           u'=',
           u'?',
           u'`',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'Q',
           u'W',
           u'E',
           u'R',
           u'T',
           u'Z',
           u'U',
           u'I',
           u'O',
           u'P',
           u'\xdc',
           u'*',
           u"'"],
          [u'LASTICON',
           u'A',
           u'S',
           u'D',
           u'F',
           u'G',
           u'H',
           u'J',
           u'K',
           u'L',
           u'\xd6',
           u'\xc4',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'>',
           u'Y',
           u'X',
           u'C',
           u'V',
           u'B',
           u'N',
           u'M',
           u';',
           u':',
           u'_',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'',
           u'',
           u'\xb2',
           u'\xb3',
           u'',
           u'',
           u'',
           u'{',
           u'[',
           u']',
           u'}',
           u'\\',
           u'\u1e9e',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'@',
           u'',
           u'\u20ac',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'~',
           u''],
          [u'LASTICON',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'|',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'\xb5',
           u'',
           u'',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.greek = [[[u'`',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u'-',
           u'=',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u';',
           u'\u03c2',
           u'\u03b5',
           u'\u03c1',
           u'\u03c4',
           u'\u03c5',
           u'\u03b8',
           u'\u03b9',
           u'\u03bf',
           u'\u03c0',
           u'[',
           u']',
           u'\\'],
          [u'LASTICON',
           u'\u03b1',
           u'\u03c3',
           u'\u03b4',
           u'\u03c6',
           u'\u03b3',
           u'\u03b7',
           u'\u03be',
           u'\u03ba',
           u'\u03bb',
           u'\u0384',
           u"'",
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'<',
           u'\u03b6',
           u'\u03c7',
           u'\u03c8',
           u'\u03c9',
           u'\u03b2',
           u'\u03bd',
           u'\u03bc',
           u',',
           '.',
           u'/',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'~',
           u'!',
           u'@',
           u'#',
           u'$',
           u'%',
           u'^',
           u'&',
           u'*',
           u'(',
           u')',
           u'_',
           u'+',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u':',
           u'\u0385',
           u'\u0395',
           u'\u03a1',
           u'\u03a4',
           u'\u03a5',
           u'\u0398',
           u'\u0399',
           u'\u039f',
           u'\u03a0',
           u'{',
           u'}',
           u'|'],
          [u'LASTICON',
           u'\u0391',
           u'\u03a3',
           u'\u0394',
           u'\u03a6',
           u'\u0393',
           u'\u0397',
           u'\u039e',
           u'\u039a',
           u'\u039b',
           u'\xa8',
           u'"',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'>',
           u'\u0396',
           u'\u03a7',
           u'\u03a8',
           u'\u03a9',
           u'\u0392',
           u'\u039d',
           u'\u039c',
           u'<',
           u'>',
           u'?',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'',
           u'',
           u'\xb2',
           u'\xb3',
           u'\xa3',
           u'\xa7',
           u'\xb6',
           u'',
           u'\xa4',
           u'\xa6',
           u'\xb0',
           u'\xb1',
           u'\xbd',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'',
           u'\u03ac',
           u'\u03ad',
           u'\u03ae',
           u'\u03af',
           u'\u03cc',
           u'\u03cd',
           u'\u03ce',
           u'\u03ca',
           u'\u03cb',
           u'\xab',
           u'\xbb',
           u'\xac'],
          [u'LASTICON',
           u'',
           u'\u0386',
           u'\u0388',
           u'\u0389',
           u'\u038a',
           u'\u038c',
           u'\u038e',
           u'\u038f',
           u'\u03aa',
           u'\u03ab',
           u'\u0385',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'CAPSLOCKICON',
           u'',
           u'',
           u'',
           u'\xa9',
           u'\xae',
           u'\u20ac',
           u'\xa5',
           u'',
           u'',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.latvian = [[[u'',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u'-',
           u'f',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\u016b',
           u'g',
           u'j',
           u'r',
           u'm',
           u'v',
           u'n',
           u'z',
           u'\u0113',
           u'\u010d',
           u'\u017e',
           u'h',
           u'\u0137'],
          [u'LASTICON',
           u'\u0161',
           u'u',
           u's',
           u'i',
           u'l',
           u'd',
           u'a',
           u't',
           u'e',
           u'c',
           u'\xb4',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'\u0123',
           u'\u0146',
           u'b',
           u'\u012b',
           u'k',
           u'p',
           u'o',
           u'\u0101',
           u',',
           u'.',
           u'\u013c',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'?',
           u'!',
           u'\xab',
           u'\xbb',
           u'$',
           u'%',
           u'/',
           u'&',
           u'\xd7',
           u'(',
           u')',
           u'_',
           u'F',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\u016a',
           u'G',
           u'J',
           u'R',
           u'M',
           u'V',
           u'N',
           u'Z',
           u'\u0112',
           u'\u010c',
           u'\u017d',
           u'H',
           u'\u0136'],
          [u'LASTICON',
           u'\u0160',
           u'U',
           u'S',
           u'I',
           u'L',
           u'D',
           u'A',
           u'T',
           u'E',
           u'C',
           u'\xb0',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'\u0122',
           u'\u0145',
           u'B',
           u'\u012a',
           u'K',
           u'P',
           u'O',
           u'\u0100',
           u';',
           u':',
           u'\u013b',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'',
           u'\xab',
           u'',
           u'',
           u'\u20ac',
           u'"',
           u"'",
           u'',
           u':',
           u'',
           u'',
           u'\u2013',
           u'=',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'q',
           u'\u0123',
           u'',
           u'\u0157',
           u'w',
           u'y',
           u'',
           u'',
           u'',
           u'',
           u'[',
           u']',
           u''],
          [u'LASTICON',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'\u20ac',
           u'',
           u'\xb4',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'\\',
           u'',
           u'x',
           u'',
           u'\u0137',
           u'',
           u'\xf5',
           u'',
           u'<',
           u'>',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'',
           u'',
           u'@',
           u'#',
           u'$',
           u'~',
           u'^',
           u'\xb1',
           u'',
           u'',
           u'',
           u'\u2014',
           u';',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'Q',
           u'\u0122',
           u'',
           u'\u0156',
           u'W',
           u'Y',
           u'',
           u'',
           u'',
           u'',
           u'{',
           u'}',
           u''],
          [u'LASTICON',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'\xa8',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'|',
           u'',
           u'X',
           u'',
           u'\u0136',
           u'',
           u'\xd5',
           u'',
           u'',
           u'',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.russian = [[[u'\u0451',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u'-',
           u'=',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\u0439',
           u'\u0446',
           u'\u0443',
           u'\u043a',
           u'\u0435',
           u'\u043d',
           u'\u0433',
           u'\u0448',
           u'\u0449',
           u'\u0437',
           u'\u0445',
           u'\u044a',
           u'\\'],
          [u'LASTICON',
           u'\u0444',
           u'\u044b',
           u'\u0432',
           u'\u0430',
           u'\u043f',
           u'\u0440',
           u'\u043e',
           u'\u043b',
           u'\u0434',
           u'\u0436',
           u'\u044d',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'\\',
           u'\u044f',
           u'\u0447',
           u'\u0441',
           u'\u043c',
           u'\u0438',
           u'\u0442',
           u'\u044c',
           u'\u0431',
           u'\u044e',
           u'.',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'\u0401',
           u'!',
           u'"',
           u'\u2116',
           u';',
           u'%',
           u':',
           u'?',
           u'*',
           u'(',
           u')',
           u'_',
           u'+',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\u0419',
           u'\u0426',
           u'\u0423',
           u'\u041a',
           u'\u0415',
           u'\u041d',
           u'\u0413',
           u'\u0428',
           u'\u0429',
           u'\u0417',
           u'\u0425',
           u'\u042a',
           u'/'],
          [u'LASTICON',
           u'\u0424',
           u'\u042b',
           u'\u0412',
           u'\u0410',
           u'\u041f',
           u'\u0420',
           u'\u041e',
           u'\u041b',
           u'\u0414',
           u'\u0416',
           u'\u042d',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'/',
           u'\u042f',
           u'\u0427',
           u'\u0421',
           u'\u041c',
           u'\u0418',
           u'\u0422',
           u'\u042c',
           u'\u0411',
           u'\u042e',
           u',',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'',
           u'\xa7',
           u'@',
           u'#',
           u'&',
           u'$',
           u'\u20bd',
           u'\u20ac',
           u'',
           u'',
           u'',
           u'',
           u''],
          [u'LASTICON',
           u'',
           u'<',
           u'>',
           u'[',
           u']',
           u'{',
           u'}',
           u'',
           u'',
           u'',
           u'',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.scandinavian = [[[u'\xa7',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u'+',
           u'\xb4',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'q',
           u'w',
           u'e',
           u'r',
           u't',
           u'y',
           u'u',
           u'i',
           u'o',
           u'p',
           u'\xe5',
           u'\xa8',
           u"'"],
          [u'LASTICON',
           u'a',
           u's',
           u'd',
           u'f',
           u'g',
           u'h',
           u'j',
           u'k',
           u'l',
           u'\xf6',
           u'\xe4',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'<',
           u'z',
           u'x',
           u'c',
           u'v',
           u'b',
           u'n',
           u'm',
           u',',
           '.',
           u'-',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'\xbd',
           u'!',
           u'"',
           u'#',
           u'\xa4',
           u'%',
           u'&',
           u'/',
           u'(',
           u')',
           u'=',
           u'?',
           u'`',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'Q',
           u'W',
           u'E',
           u'R',
           u'T',
           u'Y',
           u'U',
           u'I',
           u'O',
           u'P',
           u'\xc5',
           u'^',
           u'*'],
          [u'LASTICON',
           u'A',
           u'S',
           u'D',
           u'F',
           u'G',
           u'H',
           u'J',
           u'K',
           u'L',
           u'\xd6',
           u'\xc4',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'>',
           u'Z',
           u'X',
           u'C',
           u'V',
           u'B',
           u'N',
           u'M',
           u';',
           u':',
           u'_',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'',
           u'',
           u'@',
           u'\xa3',
           u'$',
           u'\u20ac',
           u'',
           u'{',
           u'[',
           u']',
           u'}',
           u'\\',
           u'',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'',
           u'',
           u'\u20ac',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'~',
           u''],
          [u'LASTICON',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'|',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'\xb5',
           u'',
           u'',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer],
         [[u'',
           u'\xe2',
           u'\xea',
           u'\xee',
           u'\xf4',
           u'\xfb',
           u'\xe4',
           u'\xeb',
           u'\xef',
           u'\xf6',
           u'\xfc',
           u'\xe3',
           u'',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\xe0',
           u'\xe8',
           u'\xec',
           u'\xf2',
           u'\xf9',
           u'\xe1',
           u'\xe9',
           u'\xed',
           u'\xf3',
           u'\xfa',
           u'\xf5',
           u'',
           u''],
          [u'LASTICON',
           u'\xc2',
           u'\xca',
           u'\xce',
           u'\xd4',
           u'\xdb',
           u'\xc4',
           u'\xcb',
           u'\xcf',
           u'\xd6',
           u'\xdc',
           u'\xc3',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'\xc0',
           u'\xc8',
           u'\xcc',
           u'\xd2',
           u'\xd9',
           u'\xc1',
           u'\xc9',
           u'\xcd',
           u'\xd3',
           u'\xda',
           u'\xd5',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.spanish = [[[u'\xba',
           u'1',
           u'2',
           u'3',
           u'4',
           u'5',
           u'6',
           u'7',
           u'8',
           u'9',
           u'0',
           u"'",
           u'\xa1',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'q',
           u'w',
           u'e',
           u'r',
           u't',
           u'y',
           u'u',
           u'i',
           u'o',
           u'p',
           u'`',
           u'+',
           u'\xe7'],
          [u'LASTICON',
           u'a',
           u's',
           u'd',
           u'f',
           u'g',
           u'h',
           u'j',
           u'k',
           u'l',
           u'\xf1',
           u'\xb4',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'<',
           u'z',
           u'x',
           u'c',
           u'v',
           u'b',
           u'n',
           u'm',
           u',',
           '.',
           u'-',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'\xaa',
           u'!',
           u'"',
           u'\xb7',
           u'$',
           u'%',
           u'&',
           u'/',
           u'(',
           u')',
           u'=',
           u'?',
           u'\xbf',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'Q',
           u'W',
           u'E',
           u'R',
           u'T',
           u'Y',
           u'U',
           u'I',
           u'O',
           u'P',
           u'^',
           u'*',
           u'\xc7'],
          [u'LASTICON',
           u'A',
           u'S',
           u'D',
           u'F',
           u'G',
           u'H',
           u'J',
           u'K',
           u'L',
           u'\xd1',
           u'\xa8',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'>',
           u'Z',
           u'X',
           u'C',
           u'V',
           u'B',
           u'N',
           u'M',
           u';',
           u':',
           u'_',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'\\',
           u'|',
           u'@',
           u'#',
           u'~',
           u'\u20ac',
           u'\xac',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'',
           u'\xe1',
           u'\xe9',
           u'\xed',
           u'\xf3',
           u'\xfa',
           u'\xfc',
           u'',
           u'',
           u'[',
           u']',
           u'',
           u''],
          [u'LASTICON',
           u'',
           u'\xc1',
           u'\xc9',
           u'\xcd',
           u'\xd3',
           u'\xda',
           u'\xdc',
           u'',
           u'',
           u'{',
           u'}',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.thai = [[[u'',
           u'',
           u'\u0e45',
           u'\u0e20',
           u'\u0e16',
           u'\u0e38',
           u'\u0e36',
           u'\u0e04',
           u'\u0e15',
           u'\u0e08',
           u'\u0e02',
           u'\u0e0a',
           u'',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\u0e46',
           u'\u0e44',
           u'\u0e33',
           u'\u0e1e',
           u'\u0e30',
           u'\u0e31',
           u'\u0e35',
           u'\u0e23',
           u'\u0e19',
           u'\u0e22',
           u'\u0e1a',
           u'\u0e25',
           u''],
          [u'LASTICON',
           u'\u0e1f',
           u'\u0e2b',
           u'\u0e01',
           u'\u0e14',
           u'\u0e40',
           u'\u0e49',
           u'\u0e48',
           u'\u0e32',
           u'\u0e2a',
           u'\u0e27',
           u'\u0e07',
           u'\u0e03',
           self.green],
          [u'CAPSLOCKICON',
           u'CAPSLOCKICON',
           u'\u0e1c',
           u'\u0e1b',
           u'\u0e41',
           u'\u0e2d',
           u'\u0e34',
           u'\u0e37',
           u'\u0e17',
           u'\u0e21',
           u'\u0e43',
           u'\u0e1d',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'',
           u'',
           u'\u0e51',
           u'\u0e52',
           u'\u0e53',
           u'\u0e54',
           u'\u0e39',
           u'\u0e55',
           u'\u0e56',
           u'\u0e57',
           u'\u0e58',
           u'\u0e59',
           u'',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\u0e50',
           u'',
           u'\u0e0e',
           u'\u0e11',
           u'\u0e18',
           u'\u0e4d',
           u'\u0e4a',
           u'\u0e13',
           u'\u0e2f',
           u'\u0e0d',
           u'\u0e10',
           u'\u0e05',
           u''],
          [u'LASTICON',
           u'\u0e24',
           u'\u0e06',
           u'\u0e0f',
           u'\u0e42',
           u'\u0e0c',
           u'\u0e47',
           u'\u0e4b',
           u'\u0e29',
           u'\u0e28',
           u'\u0e0b',
           u'',
           u'\u0e3f',
           self.green],
          [u'CAPSLOCKICON',
           u'CAPSLOCKICON',
           u'',
           u'\u0e09',
           u'\u0e2e',
           u'\u0e3a',
           u'\u0e4c',
           u'',
           u'\u0e12',
           u'\u0e2c',
           u'\u0e26',
           u'',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]]
        self.locales = {'ar_BH': [_('Arabic'), _('Bahrain'), self.arabic(self.english)],
         'ar_EG': [_('Arabic'), _('Egypt'), self.arabic(self.english)],
         'ar_JO': [_('Arabic'), _('Jordan'), self.arabic(self.english)],
         'ar_KW': [_('Arabic'), _('Kuwait'), self.arabic(self.english)],
         'ar_LB': [_('Arabic'), _('Lebanon'), self.arabic(self.english)],
         'ar_OM': [_('Arabic'), _('Oman'), self.arabic(self.english)],
         'ar_QA': [_('Arabic'), _('Qatar'), self.arabic(self.english)],
         'ar_SA': [_('Arabic'), _('Saudi Arabia'), self.arabic(self.english)],
         'ar_SY': [_('Arabic'), _('Syrian Arab Republic'), self.arabic(self.english)],
         'ar_AE': [_('Arabic'), _('United Arab Emirates'), self.arabic(self.english)],
         'ar_YE': [_('Arabic'), _('Yemen'), self.arabic(self.english)],
         'cs_CZ': [_('Czech'), _('Czechia'), self.czech],
         'nl_NL': [_('Dutch'), _('Netherlands'), self.dutch(self.english)],
         'en_AU': [_('English'), _('Australian'), self.english],
         'en_GB': [_('English'), _('United Kingdom'), self.unitedKingdom(self.english)],
         'en_US': [_('English'), _('United States'), self.english],
         'en_EN': [_('English'), _('Various'), self.english],
         'et_EE': [_('Estonian'), _('Estonia'), self.estonian(self.scandinavian)],
         'fi_FI': [_('Finnish'), _('Finland'), self.scandinavian],
         'fr_BE': [_('French'), _('Belgian'), self.belgian(self.french)],
         'fr_FR': [_('French'), _('France'), self.french],
         'fr_CH': [_('French'), _('Switzerland'), self.frenchSwiss(self.german)],
         'de_DE': [_('German'), _('Germany'), self.german],
         'de_CH': [_('German'), _('Switzerland'), self.germanSwiss(self.german)],
         'el_GR': [_('Greek (Modern)'), _('Greece'), self.greek],
         'hu_HU': [_('Hungarian'), _('Hungary'), self.hungarian(self.german)],
         'lv_01': [_('Latvian'), _('Alternative 1'), self.latvianStandard(self.english)],
         'lv_02': [_('Latvian'), _('Alternative 2'), self.latvian],
         'lv_LV': [_('Latvian'), _('Latvia'), self.latvianQWERTY(self.english)],
         'lt_LT': [_('Lithuanian'), _('Lithuania'), self.lithuanian(self.english)],
         'nb_NO': [_('Norwegian'), _('Norway'), self.norwegian(self.scandinavian)],
         'fa_IR': [_('Persian'), _('Iran, Islamic Republic'), self.persian(self.english)],
         'pl_01': [_('Polish'), _('Alternative'), self.polish(self.german)],
         'pl_PL': [_('Polish'), _('Poland'), self.polishProgrammers(self.english)],
         'ru_RU': [_('Russian'), _('Russian Federation'), self.russian],
         'sk_SK': [_('Slovak'), _('Slovakia'), self.slovak(self.german)],
         'es_ES': [_('Spanish'), _('Spain'), self.spanish],
         'sv_SE': [_('Swedish'), _('Sweden'), self.scandinavian],
         'th_TH': [_('Thai'), _('Thailand'), self.thai],
         'uk_01': [_('Ukrainian'), _('Russian'), self.ukranian(self.russian)],
         'uk_UA': [_('Ukrainian'), _('Ukraine'), self.ukranianEnhanced(self.russian)]}
        self['actions'] = HelpableNumberActionMap(self, 'VirtualKeyBoardActions', {'cancel': (self.cancel, _('Cancel any text changes and exit')),
         'save': (self.save, _('Save / Enter text and exit')),
         'shift': (self.shiftSelected, _('Select the virtual keyboard shifted character set for the next character only')),
         'capsLock': (self.capsLockSelected, _('Select the virtual keyboard shifted character set')),
         'select': (self.processSelect, _('Select the character or action under the virtual keyboard cursor')),
         'locale': (self.localeMenu, _('Select the virtual keyboard locale from a menu')),
         'up': (self.up, _('Move the virtual keyboard cursor up')),
         'left': (self.left, _('Move the virtual keyboard cursor left')),
         'right': (self.right, _('Move the virtual keyboard cursor right')),
         'down': (self.down, _('Move the virtual keyboard cursor down')),
         'first': (self.cursorFirst, _('Move the text buffer cursor to the first character')),
         'prev': (self.cursorLeft, _('Move the text buffer cursor left')),
         'next': (self.cursorRight, _('Move the text buffer cursor right')),
         'last': (self.cursorLast, _('Move the text buffer cursor to the last character')),
         'backspace': (self.backSelected, _('Delete the character to the left of text buffer cursor')),
         'delete': (self.forwardSelected, _('Delete the character under the text buffer cursor')),
         'toggleOverwrite': (self.keyToggleOW, _('Toggle new text inserts before or overwrites existing text')),
         '1': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '2': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '3': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '4': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '5': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '6': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '7': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '8': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '9': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         '0': (self.keyNumberGlobal, _('Number or SMS style data entry')),
         'gotAsciiCode': (self.keyGotAscii, _('Keyboard data entry'))}, -2, description=_('Virtual KeyBoard Functions'))
        self.lang = language.getLanguage()
        self['prompt'] = Label(prompt)
        self['text'] = Input(text=text, maxSize=maxSize, visible_width=visible_width, type=type, currPos=currPos if currPos != -1 else len(text.decode('utf-8', 'ignore')), allMarked=allMarked)
        self['list'] = VirtualKeyBoardList([])
        self['mode'] = Label(_('INS'))
        self['locale'] = Label(_('Locale') + ': ' + self.lang)
        self['language'] = Label(_('Language') + ': ' + self.lang)
        self['key_info'] = StaticText(_('INFO'))
        self['key_red'] = StaticText(_('Exit'))
        self['key_green'] = StaticText(_(greenLabel))
        self['key_yellow'] = StaticText(_('Shift'))
        self['key_blue'] = StaticText(self.shiftMsgs[1])
        self['key_help'] = StaticText(_('HELP'))
        width, height = skin.parameters.get('VirtualKeyBoard', (45, 45))
        if self.bg_l is None or self.bg_m is None or self.bg_r is None:
            self.width = width
            self.height = height
        else:
            self.width = self.bg_l.size().width() + self.bg_m.size().width() + self.bg_r.size().width()
            self.height = self.bg_m.size().height()
        self.alignment = skin.parameters.get('VirtualKeyBoardAlignment', (0, 0))
        self.padding = skin.parameters.get('VirtualKeyBoardPadding', (4, 4))
        self.shiftColors = skin.parameters.get('VirtualKeyBoardShiftColors', (16777215, 16777215, 65535, 16711935))
        self.language = None
        self.location = None
        self.keyList = []
        self.shiftLevels = 0
        self.shiftLevel = 0
        self.shiftHold = -1
        self.keyboardWidth = 0
        self.keyboardHeight = 0
        self.maxKey = 0
        self.overwrite = False
        self.selectedKey = None
        self.sms = NumericalTextInput(self.smsGotChar)
        self.smsChar = None
        self.setLocale()
        self.onExecBegin.append(self.setKeyboardModeAscii)
        self.onLayoutFinish.append(self.buildVirtualKeyBoard)

    def arabic(self, base):
        keyList = copy.deepcopy(base)
        keyList[1][0][8] = u'\u066d'
        keyList.extend([[[u'\u0630',
           u'\u0661',
           u'\u0662',
           u'\u0663',
           u'\u0664',
           u'\u0665',
           u'\u0666',
           u'\u0667',
           u'\u0668',
           u'\u0669',
           u'\u0660',
           u'-',
           u'=',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\u0636',
           u'\u0635',
           u'\u062b',
           u'\u0642',
           u'\u0641',
           u'\u063a',
           u'\u0639',
           u'\u0647',
           u'\u062e',
           u'\u062d',
           u'\u062c',
           u'\u062f',
           u'\\'],
          [u'LASTICON',
           u'\u0634',
           u'\u0633',
           u'\u064a',
           u'\u0628',
           u'\u0644',
           u'\u0627',
           u'\u062a',
           u'\u0646',
           u'\u0645',
           u'\u0643',
           u'\u0637',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'CAPSLOCKICON',
           u'\u0626',
           u'\u0621',
           u'\u0624',
           u'\u0631',
           u'\ufefb',
           u'\u0649',
           u'\u0629',
           u'\u0648',
           u'\u0632',
           u'\u0638',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer], [[u'\u0651',
           u'!',
           u'@',
           u'#',
           u'$',
           u'%',
           u'^',
           u'&',
           u'\u066d',
           u'(',
           u')',
           u'_',
           u'+',
           u'BACKSPACEICON'],
          [u'FIRSTICON',
           u'\u0636',
           u'\u0635',
           u'\u062b',
           u'\u0642',
           u'\u0641',
           u'\u063a',
           u'\u0639',
           u'\xf7',
           u'\xd7',
           u'\u061b',
           u'>',
           u'<',
           u'|'],
          [u'LASTICON',
           u'\u0634',
           u'\u0633',
           u'\u064a',
           u'\u0628',
           u'\u0644',
           u'\u0623',
           u'\u0640',
           u'\u060c',
           u'/',
           u':',
           u'"',
           self.green,
           self.green],
          [u'CAPSLOCKICON',
           u'CAPSLOCKICON',
           u'\u0626',
           u'\u0621',
           u'\u0624',
           u'\u0631',
           u'\ufef5',
           u'\u0622',
           u'\u0629',
           u',',
           u'.',
           u'\u061f',
           u'CAPSLOCKICON',
           u'CAPSLOCKICON'],
          self.footer]])
        return keyList

    def belgian(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0][6] = u'\xa7'
        keyList[0][0][8] = u'!'
        keyList[0][0][12] = u'-'
        keyList[0][1][13] = u'\xb5'
        keyList[0][3][11] = u'='
        keyList[1][0][0] = u'\xb3'
        keyList[1][0][12] = u'_'
        keyList[1][1][11] = u'\xa8'
        keyList[1][1][12] = u'*'
        keyList[1][1][13] = u'\xa3'
        keyList[1][3][11] = u'+'
        keyList[2][0] = [u'',
         u'|',
         u'@',
         u'#',
         u'{',
         u'[',
         u'^',
         u'',
         u'',
         u'{',
         u'}',
         u'',
         u'',
         u'BACKSPACEICON']
        keyList[2][1][11] = u'['
        keyList[2][1][12] = u']'
        keyList[2][1][13] = u'`'
        keyList[2][2][11] = u'\xb4'
        keyList[2][3][1] = u'\\'
        keyList[2][3][11] = u'~'
        return keyList

    def dutch(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0][0] = u'@'
        keyList[0][0][11] = u'/'
        keyList[0][0][12] = u'\xb0'
        keyList[0][1][11] = u'\xa8'
        keyList[0][1][12] = u'*'
        keyList[0][1][13] = u'<'
        keyList[0][2][10] = u'+'
        keyList[0][2][11] = u'\xb4'
        keyList[0][3] = [u'CAPSLOCKICON',
         u']',
         u'z',
         u'x',
         u'c',
         u'v',
         u'b',
         u'n',
         u'm',
         u',',
         u'.',
         u'-',
         u'CAPSLOCKICON',
         u'CAPSLOCKICON']
        keyList[1][0] = [u'\xa7',
         u'!',
         u'"',
         u'#',
         u'$',
         u'%',
         u'&',
         u'_',
         u'(',
         u')',
         u"'",
         u'?',
         u'~',
         u'BACKSPACEICON']
        keyList[1][1][11] = u'^'
        keyList[1][1][12] = u'|'
        keyList[1][1][13] = u'>'
        keyList[1][2][10] = u'\xb1'
        keyList[1][2][11] = u'`'
        keyList[1][3] = [u'CAPSLOCKICON',
         u'[',
         u'Z',
         u'X',
         u'C',
         u'V',
         u'B',
         u'N',
         u'M',
         u';',
         u':',
         u'=',
         u'CAPSLOCKICON',
         u'CAPSLOCKICON']
        keyList.append([[u'\xac',
          u'\xb9',
          u'\xb2',
          u'\xb3',
          u'\xbc',
          u'\xbd',
          u'\xbe',
          u'\xa3',
          u'{',
          u'}',
          u'',
          u'\\',
          u'\xb8',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'',
          u'',
          u'\u20ac',
          u'\xb6',
          u'',
          u'\xe1',
          u'\xe9',
          u'\xed',
          u'\xf3',
          u'\xfa',
          u'',
          u'',
          u''],
         [u'LASTICON',
          u'',
          u'\xdf',
          u'',
          u'',
          u'',
          u'\xc1',
          u'\xc9',
          u'\xcd',
          u'\xd3',
          u'\xda',
          u'',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'\xa6',
          u'\xab',
          u'\xbb',
          u'\xa2',
          u'',
          u'',
          u'',
          u'\xb5',
          u'',
          u'\xb7',
          u'',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        return keyList

    def estonian(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0][0] = u'\u02c7'
        keyList[0][1][11] = u'\xfc'
        keyList[0][1][12] = u'\xf5'
        keyList[1][0][0] = u'~'
        keyList[1][1][11] = u'\xdc'
        keyList[1][1][12] = u'\xd5'
        keyList[2][1][12] = u'\xa7'
        keyList[2][1][13] = u'\xbd'
        keyList[2][2][2] = u'\u0161'
        keyList[2][2][3] = u'\u0160'
        keyList[2][2][11] = u'^'
        keyList[2][3][2] = u'\u017e'
        keyList[2][3][3] = u'\u017d'
        keyList[2][3][8] = u''
        del keyList[3]
        return keyList

    def frenchSwiss(self, base):
        keyList = self.germanSwiss(base)
        keyList[0][0][11] = u"'"
        keyList[0][0][12] = u'^'
        keyList[0][1][11] = u'\xe8'
        keyList[0][2][10] = u'\xe9'
        keyList[0][2][11] = u'\xe0'
        keyList[1][1][11] = u'\xfc'
        keyList[1][2][10] = u'\xf6'
        keyList[1][2][11] = u'\xe4'
        return keyList

    def germanSwiss(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0][0] = u'\xa7'
        keyList[0][0][11] = u"'"
        keyList[0][0][12] = u'^'
        keyList[0][1][12] = u'\xa8'
        keyList[0][1][13] = u'$'
        keyList[1][0][1] = u'+'
        keyList[1][0][3] = u'*'
        keyList[1][0][4] = u'\xe7'
        keyList[1][0][11] = u'?'
        keyList[1][0][12] = u'`'
        keyList[1][1][11] = u'\xe8'
        keyList[1][1][12] = u'!'
        keyList[1][1][13] = u'\xa3'
        keyList[1][2][10] = u'\xe9'
        keyList[1][2][11] = u'\xe0'
        keyList[2][0] = [u'',
         u'\xa6',
         u'@',
         u'#',
         u'\xb0',
         u'\xa7',
         u'\xac',
         u'|',
         u'\xa2',
         u'',
         u'',
         u'\xb4',
         u'~',
         u'BACKSPACEICON']
        keyList[2][1][1] = u''
        keyList[2][1][9] = u'\xdc'
        keyList[2][1][10] = u'\xc8'
        keyList[2][1][11] = u'['
        keyList[2][1][12] = u']'
        keyList[2][2][6] = u'\xd6'
        keyList[2][2][7] = u'\xc9'
        keyList[2][2][8] = u'\xc4'
        keyList[2][2][9] = u'\xc0'
        keyList[2][2][10] = u'{'
        keyList[2][2][11] = u'}'
        keyList[2][3][1] = u'\\'
        keyList[2][3][8] = u''
        return keyList

    def hungarian(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0][0] = u'0'
        keyList[0][0][10] = u'\xf6'
        keyList[0][0][11] = u'\xfc'
        keyList[0][0][12] = u'\xf3'
        keyList[0][1][11] = u'\u0151'
        keyList[0][1][12] = u'\xfa'
        keyList[0][1][13] = u'\u0171'
        keyList[0][2][10] = u'\xe9'
        keyList[0][2][11] = u'\xe1'
        keyList[0][3][1] = u'\xed'
        keyList[1][0] = [u'\xa7',
         u"'",
         u'"',
         u'+',
         u'!',
         u'%',
         u'/',
         u'=',
         u'(',
         u')',
         u'\xd6',
         u'\xdc',
         u'\xd3',
         u'BACSPACEICON']
        keyList[1][1][11] = u'\u0150'
        keyList[1][1][12] = u'\xda'
        keyList[1][1][13] = u'\u0170'
        keyList[1][2][10] = u'\xc9'
        keyList[1][2][11] = u'\xc1'
        keyList[1][3][1] = u'\xcd'
        keyList[1][3][9] = u'?'
        del keyList[2]
        keyList.append([[u'',
          u'~',
          u'\u02c7',
          u'^',
          u'\u02d8',
          u'\xb0',
          u'\u02db',
          u'`',
          u'\u02d9',
          u'\xb4',
          u'\u02dd',
          u'\xa8',
          u'\xb8',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'\\',
          u'|',
          u'\xc4',
          u'',
          u'',
          u'',
          u'\u20ac',
          u'\xcd',
          u'',
          u'',
          u'\xf7',
          u'\xd7',
          u'\xa4'],
         [u'LASTICON',
          u'\xe4',
          u'\u0111',
          u'\u0110',
          u'[',
          u']',
          u'',
          u'\xed',
          u'\u0142',
          u'\u0141',
          u'$',
          u'\xdf',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'<',
          u'>',
          u'#',
          u'&',
          u'@',
          u'{',
          u'}',
          u'<',
          u';',
          u'>',
          u'*',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        return keyList

    def latvianQWERTY(self, base):
        keyList = self.latvianStandard(base)
        keyList[0][1][13] = u'\xb0'
        keyList[2][1][9] = u'\xf5'
        keyList[3][1][9] = u'\xd5'
        return keyList

    def latvianStandard(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][3][1] = u'\\'
        keyList[1][3][1] = u'|'
        keyList.append([[u'',
          u'',
          u'\xab',
          u'\xbb',
          u'\u20ac',
          u'',
          u'\u2019',
          u'',
          u'',
          u'',
          u'',
          u'\u2013',
          u'',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'',
          u'',
          u'\u0113',
          u'\u0157',
          u'',
          u'',
          u'\u016b',
          u'\u012b',
          u'\u014d',
          u'',
          u'',
          u'',
          u''],
         [u'LASTICON',
          u'\u0101',
          u'\u0161',
          u'',
          u'',
          u'\u0123',
          u'',
          u'',
          u'\u0137',
          u'\u013c',
          u'',
          u'\xb4',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'',
          u'\u017e',
          u'',
          u'\u010d',
          u'',
          u'',
          u'\u0146',
          u'',
          u'',
          u'',
          u'',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        keyList.append([[u'',
          u'',
          u'',
          u'',
          u'\xa7',
          u'\xb0',
          u'',
          u'\xb1',
          u'\xd7',
          u'',
          u'',
          u'\u2014',
          u'',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'',
          u'',
          u'\u0112',
          u'\u0156',
          u'',
          u'',
          u'\u016a',
          u'\u012a',
          u'\u014c',
          u'',
          u'',
          u'',
          u''],
         [u'LASTICON',
          u'\u0100',
          u'\u0160',
          u'',
          u'',
          u'\u0122',
          u'',
          u'',
          u'\u0136',
          u'\u013b',
          u'',
          u'\xa8',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'',
          u'\u017d',
          u'',
          u'\u010c',
          u'',
          u'',
          u'\u0145',
          u'',
          u'',
          u'',
          u'',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        return keyList

    def lithuanian(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0] = [u'`',
         u'\u0105',
         u'\u010d',
         u'\u0119',
         u'\u0117',
         u'\u012f',
         u'\u0161',
         u'\u0173',
         u'\u016b',
         u'9',
         u'0',
         u'-',
         u'\u017e',
         u'BACKSPACEICON']
        keyList[0][3][1] = u'\\'
        keyList[1][0] = [u'~',
         u'\u0104',
         u'\u010c',
         u'\u0118',
         u'\u0116',
         u'\u012e',
         u'\u0160',
         u'\u0172',
         u'\u016a',
         u'(',
         u')',
         u'_',
         u'\u017d',
         u'BACKSPACEICON']
        keyList[1][3][1] = u'|'
        keyList.append([[u'',
          u'1',
          u'2',
          u'3',
          u'4',
          u'5',
          u'6',
          u'7',
          u'8',
          u'9',
          u'0',
          u'',
          u'=',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'!',
          u'@',
          u'#',
          u'$',
          u'%',
          u'^',
          u'&',
          u'*',
          u'',
          u'',
          u'',
          u'+',
          u''],
         [u'LASTICON',
          u'',
          u'',
          u'\u20ac',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        return keyList

    def norwegian(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0][0] = u'|'
        keyList[0][0][12] = u'\\'
        keyList[0][2][10] = u'\xf8'
        keyList[0][2][11] = u'\xe6'
        keyList[1][0][0] = u'\xa7'
        keyList[1][2][10] = u'\xd8'
        keyList[1][2][11] = u'\xc6'
        keyList[2][0][11] = u''
        keyList[2][0][12] = u'\xb4'
        keyList[2][3][1] = u''
        return keyList

    def persian(self, base):
        keyList = copy.deepcopy(base)
        keyList.append([[u'\xf7',
          u'\u06f1',
          u'\u06f2',
          u'\u06f3',
          u'\u06f4',
          u'\u06f5',
          u'\u06f6',
          u'\u06f7',
          u'\u06f8',
          u'\u06f9',
          u'\u06f0',
          u'-',
          u'=',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'\u0636',
          u'\u0635',
          u'\u062b',
          u'\u0642',
          u'\u0641',
          u'\u063a',
          u'\u0639',
          u'\u0647',
          u'\u062e',
          u'\u062d',
          u'\u062c',
          u'\u0686',
          u'\u067e'],
         [u'LASTICON',
          u'\u0634',
          u'\u0633',
          u'\u06cc',
          u'\u0628',
          u'\u0644',
          u'\u0627',
          u'\u062a',
          u'\u0646',
          u'\u0645',
          u'\u06a9',
          u'\u06af',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'\u0649',
          u'\u0638',
          u'\u0637',
          u'\u0632',
          u'\u0631',
          u'\u0630',
          u'\u062f',
          u'\u0626',
          u'\u0648',
          u'.',
          u'/',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        keyList.append([[u'\xd7',
          u'!',
          u'@',
          u'#',
          u'$',
          u'%',
          u'^',
          u'&',
          u'*',
          u')',
          u'(',
          u'_',
          u'+',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'\u064b',
          u'\u064c',
          u'\u064d',
          u'\u0631',
          u'\u060c',
          u'\u061b',
          u',',
          u']',
          u'[',
          u'\\',
          u'}',
          u'{',
          u'|'],
         [u'LASTICON',
          u'\u064e',
          u'\u064f',
          u'\u0650',
          u'\u0651',
          u'\u06c0',
          u'\u0622',
          u'\u0640',
          u'\xab',
          u'\xbb',
          u':',
          u'"',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'|',
          u'\u0629',
          u'\u064a',
          u'\u0698',
          u'\u0624',
          u'\u0625',
          u'\u0623',
          u'\u0621',
          u'<',
          u'>',
          u'\u061f',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        return keyList

    def polish(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0][0] = u'\u02db'
        keyList[0][0][11] = u'+'
        keyList[0][1][11] = u'\u017c'
        keyList[0][1][12] = u'\u015b'
        keyList[0][1][13] = u'\xf3'
        keyList[0][2][10] = u'\u0142'
        keyList[0][2][11] = u'\u0105'
        keyList[1][0][0] = u'\xb7'
        keyList[1][0][3] = u'#'
        keyList[1][0][4] = u'\xa4'
        keyList[1][0][12] = u'*'
        keyList[1][1][11] = u'\u0144'
        keyList[1][1][12] = u'\u0107'
        keyList[1][1][13] = u'\u017a'
        keyList[1][2][10] = u'\u0141'
        keyList[1][2][11] = u'\u0119'
        del keyList[2]
        keyList.append([[u'',
          u'~',
          u'\u02c7',
          u'^',
          u'\u02d8',
          u'\xb0',
          u'\u02db',
          u'`',
          u'\xb7',
          u'\xb4',
          u'\u02dd',
          u'\xa8',
          u'\xb8',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'\\',
          u'\xa6',
          u'',
          u'\u017b',
          u'\u015a',
          u'\xd3',
          u'\u20ac',
          u'\u0143',
          u'\u0106',
          u'\u0179',
          u'\xf7',
          u'\xd7',
          u''],
         [u'LASTICON',
          u'',
          u'\u0111',
          u'\u0110',
          u'',
          u'',
          u'',
          u'',
          u'\u0104',
          u'\u0118',
          u'$',
          u'\xdf',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'',
          u'',
          u'',
          u'',
          u'@',
          u'{',
          u'}',
          u'\xa7',
          u'<',
          u'>',
          u'',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        return keyList

    def polishProgrammers(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][3][1] = u'\\'
        keyList[1][3][1] = u'|'
        keyList.append([[u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'',
          u'',
          u'\u0119',
          u'\u0118',
          u'',
          u'',
          u'\u20ac',
          u'',
          u'\xf3',
          u'\xd3',
          u'',
          u'',
          u''],
         [u'LASTICON',
          u'\u0105',
          u'\u0104',
          u'\u015b',
          u'\u015a',
          u'',
          u'',
          u'',
          u'',
          u'\u0142',
          u'\u0141',
          u'',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'\u017c',
          u'\u017b',
          u'\u017a',
          u'\u0179',
          u'\u0107',
          u'\u0106',
          u'\u0144',
          u'\u0143',
          u'',
          u'',
          u'',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        return keyList

    def slovak(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][0] = [u';',
         u'+',
         u'\u013e',
         u'\u0161',
         u'\u010d',
         u'\u0165',
         u'\u017e',
         u'\xfd',
         u'\xe1',
         u'\xed',
         u'\xe9',
         u'=',
         u'\xb4',
         u'BACKSPACEICON']
        keyList[0][1][11] = u'\xfa'
        keyList[0][1][12] = u'\xe4'
        keyList[0][1][13] = u'\u0148'
        keyList[0][2][10] = u'\xf4'
        keyList[0][2][11] = u'\xa7'
        keyList[0][3][1] = u'&'
        keyList[1][0] = [u'\xb0',
         u'1',
         u'2',
         u'3',
         u'4',
         u'5',
         u'6',
         u'7',
         u'8',
         u'9',
         u'0',
         u'%',
         u'\u02c7',
         u'BACKSPACEICON']
        keyList[1][1][11] = u'/'
        keyList[1][1][12] = u'('
        keyList[1][1][13] = u')'
        keyList[1][2][10] = u'"'
        keyList[1][2][11] = u'!'
        keyList[1][3][1] = u'*'
        keyList[1][3][9] = u'?'
        del keyList[2]
        keyList.append([[u'',
          u'~',
          u'\u02c7',
          u'^',
          u'\u02d8',
          u'\xb0',
          u'\u02db',
          u'`',
          u'\u02d9',
          u'\xb4',
          u'\u02dd',
          u'\xa8',
          u'\xb8',
          u'BACKSPACEICON'],
         [u'FIRSTICON',
          u'\\',
          u'|',
          u'\u20ac',
          u'',
          u'',
          u'',
          u'',
          u'',
          u'',
          u"'",
          u'\xf7',
          u'\xd7',
          u'\xa4'],
         [u'LASTICON',
          u'',
          u'\u0111',
          u'\u0110',
          u'[',
          u']',
          u'',
          u'',
          u'\u0142',
          u'\u0141',
          u'$',
          u'\xdf',
          self.green,
          self.green],
         [u'CAPSLOCKICON',
          u'<',
          u'>',
          u'#',
          u'&',
          u'@',
          u'{',
          u'}',
          u'',
          u'<',
          u'>',
          u'*',
          u'CAPSLOCKICON',
          u'CAPSLOCKICON'],
         self.footer])
        return keyList

    def ukranian(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][1][12] = u'\u0457'
        keyList[0][1][13] = u'\\'
        keyList[0][2][11] = u'\u0454'
        keyList[0][2][2] = u'\u0456'
        keyList[0][3][1] = u'\u0491'
        keyList[1][1][12] = u'\u0407'
        keyList[1][1][13] = u'/'
        keyList[1][2][11] = u'\u0404'
        keyList[1][2][2] = u'\u0406'
        keyList[1][3][1] = u'\u0490'
        return keyList

    def ukranianEnhanced(self, base):
        keyList = self.ukranian(base)
        keyList[0][0][0] = u"'"
        keyList[1][0][0] = u'\u20b4'
        return keyList

    def unitedKingdom(self, base):
        keyList = copy.deepcopy(base)
        keyList[0][1][13] = u'#'
        keyList[0][3] = [u'CAPSLOCKICON',
         u'\\',
         u'z',
         u'x',
         u'c',
         u'v',
         u'b',
         u'n',
         u'm',
         u',',
         u'.',
         u'/',
         u'CAPSLOCKICON',
         u'CAPSLOCKICON']
        keyList[0][4] = copy.copy(self.footer)
        keyList[0][4][10] = u'\xa6'
        keyList[1][0][0] = u'\xac'
        keyList[1][0][2] = u'"'
        keyList[1][0][3] = u'\xa3'
        keyList[1][1][13] = u'~'
        keyList[1][2][11] = u'@'
        keyList[1][3] = [u'CAPSLOCKICON',
         u'|',
         u'Z',
         u'X',
         u'C',
         u'V',
         u'B',
         u'N',
         u'M',
         u'<',
         u'>',
         u'?',
         u'CAPSLOCKICON',
         u'CAPSLOCKICON']
        keyList[1][4] = copy.copy(self.footer)
        keyList[1][4][10] = u'\u20ac'
        return keyList

    def smsGotChar(self):
        if self.smsChar and self.selectAsciiKey(self.smsChar):
            self.processSelect()

    def setLocale(self):
        self.language, self.location, self.keyList = self.locales.get(self.lang, [None, None, None])
        if self.language is None or self.location is None or self.keyList is None:
            self.lang = 'en_EN'
            self.language = _('English')
            self.location = _('Various')
            self.keyList = self.english
        self.shiftLevel = 0
        self['locale'].setText(_('Locale') + ': ' + self.lang + '  (' + self.language + ' - ' + self.location + ')')

    def buildVirtualKeyBoard(self):
        self.shiftLevels = len(self.keyList)
        if self.shiftLevel >= self.shiftLevels:
            self.shiftLevel = 0
        self.keyboardWidth = len(self.keyList[self.shiftLevel][0])
        self.keyboardHeight = len(self.keyList[self.shiftLevel])
        self.maxKey = self.keyboardWidth * (self.keyboardHeight - 1) + len(self.keyList[self.shiftLevel][-1]) - 1
        self.index = 0
        self.list = []
        for keys in self.keyList[self.shiftLevel]:
            self.list.append(self.virtualKeyBoardEntryComponent(keys))

        self.previousSelectedKey = None
        if self.selectedKey is None:
            self.selectedKey = self.keyboardWidth
        self.markSelectedKey()

    def virtualKeyBoardEntryComponent(self, keys):
        res = [keys]
        text = []
        offset = 14 - self.keyboardWidth
        x = self.width * offset / 2
        if offset % 2:
            x += self.width / 2
        xHighlight = x
        prevKey = None
        for key in keys:
            if key != prevKey:
                xData = x + self.padding[0]
                start, width = self.findStartAndWidth(self.index)
                if self.bg_l is None or self.bg_m is None or self.bg_r is None:
                    x += self.width * width
                else:
                    w = self.bg_l.size().width()
                    res.append(MultiContentEntryPixmapAlphaBlend(pos=(x, 0), size=(w, self.height), png=self.bg_l))
                    x += w
                    w = self.bg_m.size().width() + self.width * (width - 1)
                    res.append(MultiContentEntryPixmapAlphaBlend(pos=(x, 0), size=(w, self.height), png=self.bg_m, flags=BT_SCALE))
                    x += w
                    w = self.bg_r.size().width()
                    res.append(MultiContentEntryPixmapAlphaBlend(pos=(x, 0), size=(w, self.height), png=self.bg_r))
                    x += w
                highlight = self.keyHighlights.get(key.upper(), (None, None, None))
                if highlight[0] is None or highlight[1] is None or highlight[2] is None:
                    xHighlight += self.width * width
                else:
                    w = highlight[0].size().width()
                    res.append(MultiContentEntryPixmapAlphaBlend(pos=(xHighlight, 0), size=(w, self.height), png=highlight[0]))
                    xHighlight += w
                    w = highlight[1].size().width() + self.width * (width - 1)
                    res.append(MultiContentEntryPixmapAlphaBlend(pos=(xHighlight, 0), size=(w, self.height), png=highlight[1], flags=BT_SCALE))
                    xHighlight += w
                    w = highlight[2].size().width()
                    res.append(MultiContentEntryPixmapAlphaBlend(pos=(xHighlight, 0), size=(w, self.height), png=highlight[2]))
                    xHighlight += w
                if self.alignment[0] == 1:
                    alignH = RT_HALIGN_LEFT
                elif self.alignment[0] == 2:
                    alignH = RT_HALIGN_CENTER
                elif self.alignment[0] == 3:
                    alignH = RT_HALIGN_RIGHT
                elif start == 0 and width > 1:
                    alignH = RT_HALIGN_LEFT
                elif start + width == self.keyboardWidth and width > 1:
                    alignH = RT_HALIGN_RIGHT
                else:
                    alignH = RT_HALIGN_CENTER
                if self.alignment[1] == 1:
                    alignV = RT_VALIGN_TOP
                elif self.alignment[1] == 3:
                    alignV = RT_VALIGN_BOTTOM
                else:
                    alignV = RT_VALIGN_CENTER
                w = width * self.width - self.padding[0] * 2
                h = self.height - self.padding[1] * 2
                image = self.keyImages[self.shiftLevel].get(key, None)
                if image:
                    left = xData
                    wImage = image.size().width()
                    if alignH == RT_HALIGN_CENTER:
                        left += (w - wImage) / 2
                    elif alignH == RT_HALIGN_RIGHT:
                        left += w - wImage
                    top = self.padding[1]
                    hImage = image.size().height()
                    if alignV == RT_VALIGN_CENTER:
                        top += (h - hImage) / 2
                    elif alignV == RT_VALIGN_BOTTOM:
                        top += h - hImage
                    res.append(MultiContentEntryPixmapAlphaBlend(pos=(left, top), size=(wImage, hImage), png=image))
                elif len(key) > 1:
                    text.append(MultiContentEntryText(pos=(xData, self.padding[1]), size=(w, h), font=1, flags=alignH | alignV, text=key.encode('utf-8'), color=self.shiftColors[self.shiftLevel]))
                else:
                    text.append(MultiContentEntryText(pos=(xData, self.padding[1]), size=(w, h), font=0, flags=alignH | alignV, text=key.encode('utf-8'), color=self.shiftColors[self.shiftLevel]))
            prevKey = key
            self.index += 1

        return res + text

    def markSelectedKey(self):
        if self.sel_l is None or self.sel_m is None or self.sel_r is None:
            return
        if self.previousSelectedKey is not None:
            del self.list[self.previousSelectedKey / self.keyboardWidth][-3:]
        if self.selectedKey > self.maxKey:
            self.selectedKey = self.maxKey
        start, width = self.findStartAndWidth(self.selectedKey)
        x = start * self.width
        w = self.sel_l.size().width()
        self.list[self.selectedKey / self.keyboardWidth].append(MultiContentEntryPixmapAlphaBlend(pos=(x, 0), size=(w, self.height), png=self.sel_l))
        x += w
        w = self.sel_m.size().width() + self.width * (width - 1)
        self.list[self.selectedKey / self.keyboardWidth].append(MultiContentEntryPixmapAlphaBlend(pos=(x, 0), size=(w, self.height), png=self.sel_m, flags=BT_SCALE))
        x += w
        w = self.sel_r.size().width()
        self.list[self.selectedKey / self.keyboardWidth].append(MultiContentEntryPixmapAlphaBlend(pos=(x, 0), size=(w, self.height), png=self.sel_r))
        self.previousSelectedKey = self.selectedKey
        self['list'].setList(self.list)

    def findStartAndWidth(self, key):
        if key > self.maxKey:
            key = self.maxKey
        row = key / self.keyboardWidth
        key = key % self.keyboardWidth
        start = key
        while start:
            if self.keyList[self.shiftLevel][row][start - 1] != self.keyList[self.shiftLevel][row][key]:
                break
            start -= 1

        max = len(self.keyList[self.shiftLevel][row])
        width = 1
        while width <= max:
            if start + width >= max or self.keyList[self.shiftLevel][row][start + width] != self.keyList[self.shiftLevel][row][key]:
                break
            width += 1

        return (start, width)

    def processSelect(self):
        self.smsChar = None
        text = self.keyList[self.shiftLevel][self.selectedKey / self.keyboardWidth][self.selectedKey % self.keyboardWidth].encode('UTF-8')
        cmd = self.cmds.get(text.upper(), None)
        if cmd is None:
            self['text'].char(text.encode('UTF-8'))
        else:
            exec cmd
        if text not in (u'SHIFT', u'SHIFTICON') and self.shiftHold != -1:
            self.shiftRestore()

    def cancel(self):
        self.close(None)

    def save(self):
        self.close(self['text'].getText())

    def localeMenu(self):
        languages = []
        for locale, data in self.locales.iteritems():
            languages.append((data[0] + '  -  ' + data[1] + '  (' + locale + ')', locale))

        languages = sorted(languages)
        index = 0
        default = 0
        for item in languages:
            if item[1] == self.lang:
                default = index
                break
            index += 1

        self.session.openWithCallback(self.localeMenuCallback, ChoiceBox, _('Available locales are:'), list=languages, selection=default, keys=[])

    def localeMenuCallback(self, choice):
        if choice:
            self.lang = choice[1]
            self.setLocale()
            self.buildVirtualKeyBoard()

    def shiftSelected(self):
        if self.shiftHold == -1:
            self.shiftHold = self.shiftLevel
        self.capsLockSelected()

    def capsLockSelected(self):
        self.shiftLevel = (self.shiftLevel + 1) % self.shiftLevels
        self.shiftCommon()

    def shiftCommon(self):
        self.smsChar = None
        nextLevel = (self.shiftLevel + 1) % self.shiftLevels
        self['key_blue'].setText(self.shiftMsgs[nextLevel])
        self.buildVirtualKeyBoard()

    def shiftRestore(self):
        self.shiftLevel = self.shiftHold
        self.shiftHold = -1
        self.shiftCommon()

    def keyToggleOW(self):
        self['text'].toggleOverwrite()
        self.overwrite = not self.overwrite
        if self.overwrite:
            self['mode'].setText(_('OVR'))
        else:
            self['mode'].setText(_('INS'))

    def backSelected(self):
        self['text'].deleteBackward()

    def forwardSelected(self):
        self['text'].deleteForward()

    def cursorFirst(self):
        self['text'].home()

    def cursorLeft(self):
        self['text'].left()

    def cursorRight(self):
        self['text'].right()

    def cursorLast(self):
        self['text'].end()

    def up(self):
        self.smsChar = None
        self.selectedKey -= self.keyboardWidth
        if self.selectedKey < 0:
            self.selectedKey = self.maxKey / self.keyboardWidth * self.keyboardWidth + self.selectedKey % self.keyboardWidth
            if self.selectedKey > self.maxKey:
                self.selectedKey -= self.keyboardWidth
        self.markSelectedKey()

    def left(self):
        self.smsChar = None
        start, width = self.findStartAndWidth(self.selectedKey)
        if width > 1:
            width = self.selectedKey % self.keyboardWidth - start + 1
        self.selectedKey = self.selectedKey / self.keyboardWidth * self.keyboardWidth + (self.selectedKey + self.keyboardWidth - width) % self.keyboardWidth
        if self.selectedKey > self.maxKey:
            self.selectedKey = self.maxKey
        self.markSelectedKey()

    def right(self):
        self.smsChar = None
        start, width = self.findStartAndWidth(self.selectedKey)
        if width > 1:
            width = start + width - self.selectedKey % self.keyboardWidth
        self.selectedKey = self.selectedKey / self.keyboardWidth * self.keyboardWidth + (self.selectedKey + width) % self.keyboardWidth
        if self.selectedKey > self.maxKey:
            self.selectedKey = self.selectedKey / self.keyboardWidth * self.keyboardWidth
        self.markSelectedKey()

    def down(self):
        self.smsChar = None
        self.selectedKey += self.keyboardWidth
        if self.selectedKey > self.maxKey:
            self.selectedKey %= self.keyboardWidth
        self.markSelectedKey()

    def keyNumberGlobal(self, number):
        self.smsChar = self.sms.getKey(number)
        self.selectAsciiKey(self.smsChar)

    def keyGotAscii(self):
        self.smsChar = None
        if self.selectAsciiKey(str(unichr(getPrevAsciiCode()).encode('utf-8'))):
            self.processSelect()

    def selectAsciiKey(self, char):
        if char == u' ':
            char = SPACE
        self.shiftLevel = -1
        for keyList in self.keyList:
            self.shiftLevel = (self.shiftLevel + 1) % self.shiftLevels
            self.buildVirtualKeyBoard()
            selkey = 0
            for keys in keyList:
                for key in keys:
                    if key == char:
                        self.selectedKey = selkey
                        self.markSelectedKey()
                        return True
                    selkey += 1

        return False
