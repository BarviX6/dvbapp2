from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Screens.HelpMenu import HelpableScreen
from Screens.ChoiceBox import ChoiceBox
from Tools.BoundFunction import boundFunction
from Tools.Directories import pathExists, createDir, removeDir
from Components.config import config
import os
from Tools.NumericalTextInput import NumericalTextInput
from Components.ActionMap import NumberActionMap, HelpableActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Button import Button
from Components.FileList import FileList
from Components.MenuList import MenuList
from enigma import eTimer
defaultInhibitDirs = ['/bin',
 '/boot',
 '/dev',
 '/etc',
 '/lib',
 '/proc',
 '/sbin',
 '/sys',
 '/usr',
 '/var']

class LocationBox(Screen, NumericalTextInput, HelpableScreen):
    skin = '<screen name="LocationBox" position="100,75" size="540,460" >\n\t\t\t<widget name="text" position="0,2" size="540,22" font="Regular;22" />\n\t\t\t<widget name="target" position="0,23" size="540,22" valign="center" font="Regular;22" />\n\t\t\t<widget name="filelist" position="0,55" zPosition="1" size="540,210" scrollbarMode="showOnDemand" selectionDisabled="1" />\n\t\t\t<widget name="textbook" position="0,272" size="540,22" font="Regular;22" />\n\t\t\t<widget name="booklist" position="5,302" zPosition="2" size="535,100" scrollbarMode="showOnDemand" />\n\t\t\t<widget name="red" position="0,415" zPosition="1" size="135,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,415" zPosition="2" size="135,40" halign="center" valign="center" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="green" position="135,415" zPosition="1" size="135,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />\n\t\t\t<widget name="key_green" position="135,415" zPosition="2" size="135,40" halign="center" valign="center" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="yellow" position="270,415" zPosition="1" size="135,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />\n\t\t\t<widget name="key_yellow" position="270,415" zPosition="2" size="135,40" halign="center" valign="center" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="blue" position="405,415" zPosition="1" size="135,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />\n\t\t\t<widget name="key_blue" position="405,415" zPosition="2" size="135,40" halign="center" valign="center" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-1,-1" />\n\t\t</screen>'

    def __init__(self, session, text = '', filename = '', currDir = None, bookmarks = None, userMode = False, windowTitle = 'Select location', minFree = None, autoAdd = False, editDir = False, inhibitDirs = [], inhibitMounts = []):
        if not inhibitDirs:
            inhibitDirs = []
        if not inhibitMounts:
            inhibitMounts = []
        Screen.__init__(self, session)
        NumericalTextInput.__init__(self, handleTimeout=False)
        HelpableScreen.__init__(self)
        self.setUseableChars(u'1234567890abcdefghijklmnopqrstuvwxyz')
        self.qs_timer = eTimer()
        self.qs_timer.callback.append(self.timeout)
        self.qs_timer_type = 0
        self.curr_pos = -1
        self.quickselect = ''
        self['text'] = Label(text)
        self['textbook'] = Label(_('Bookmarks'))
        self.text = text
        self.filename = filename
        self.minFree = minFree
        self.realBookmarks = bookmarks
        self.bookmarks = bookmarks and bookmarks.value[:] or []
        self.userMode = userMode
        self.autoAdd = autoAdd
        self.editDir = editDir
        self.inhibitDirs = inhibitDirs
        self['filelist'] = FileList(currDir, showDirectories=True, showFiles=False, inhibitMounts=inhibitMounts, inhibitDirs=inhibitDirs)
        self['booklist'] = MenuList(self.bookmarks)
        self['key_green'] = Button(_('OK'))
        self['key_yellow'] = Button(_('Rename'))
        self['key_blue'] = Button(_('Remove bookmark'))
        self['key_red'] = Button(_('Cancel'))
        self['green'] = Pixmap()
        self['yellow'] = Pixmap()
        self['blue'] = Pixmap()
        self['red'] = Pixmap()
        self['target'] = Label()
        self['targetfreespace'] = Label()
        if self.userMode:
            self.usermodeOn()

        class LocationBoxActionMap(HelpableActionMap):

            def __init__(self, parent, context, actions = None, prio = 0):
                if not actions:
                    actions = {}
                HelpableActionMap.__init__(self, parent, context, actions, prio)
                self.box = parent

            def action(self, contexts, action):
                self.box.timeout(force=True)
                return HelpableActionMap.action(self, contexts, action)

        self['WizardActions'] = LocationBoxActionMap(self, 'WizardActions', {'ok': (self.ok, _('select')),
         'back': (self.cancel, _('Cancel'))}, -2)
        self['DirectionActions'] = LocationBoxActionMap(self, 'DirectionActions', {'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down}, -2)
        self['ColorActions'] = LocationBoxActionMap(self, 'ColorActions', {'red': self.cancel,
         'green': self.select,
         'yellow': self.changeName,
         'blue': self.addRemoveBookmark}, -2)
        self['EPGSelectActions'] = LocationBoxActionMap(self, 'EPGSelectActions', {'prevService': (self.switchToBookList, _('switch to bookmarks')),
         'nextService': (self.switchToFileList, _('switch to filelist'))}, -2)
        self['MenuActions'] = LocationBoxActionMap(self, 'MenuActions', {'menu': (self.showMenu, _('menu'))}, -2)
        self['NumberActions'] = NumberActionMap(['NumberActions'], {'1': self.keyNumberGlobal,
         '2': self.keyNumberGlobal,
         '3': self.keyNumberGlobal,
         '4': self.keyNumberGlobal,
         '5': self.keyNumberGlobal,
         '6': self.keyNumberGlobal,
         '7': self.keyNumberGlobal,
         '8': self.keyNumberGlobal,
         '9': self.keyNumberGlobal,
         '0': self.keyNumberGlobal})
        self.onShown.extend((boundFunction(self.setTitle, _('Select Location')), self.updateTarget, self.showHideRename))
        self.onLayoutFinish.append(self.switchToFileListOnStart)
        self.onClose.append(self.disableTimer)

    def switchToFileListOnStart(self):
        self.switchToFileList()

    def disableTimer(self):
        self.qs_timer.callback.remove(self.timeout)

    def showHideRename(self):
        if self.filename == '':
            self['key_yellow'].hide()

    def switchToFileList(self):
        if not self.userMode:
            self.currList = 'filelist'
            self['filelist'].selectionEnabled(1)
            self['booklist'].selectionEnabled(0)
            self['key_blue'].text = _('Add bookmark')
            self.updateTarget()

    def switchToBookList(self):
        self.currList = 'booklist'
        self['filelist'].selectionEnabled(0)
        self['booklist'].selectionEnabled(1)
        self['key_blue'].text = _('Remove bookmark')
        self.updateTarget()

    def addRemoveBookmark(self):
        if self.currList == 'filelist':
            folder = self['filelist'].getSelection()[0]
            if folder is not None and folder not in self.bookmarks:
                self.bookmarks.append(folder)
                self.bookmarks.sort()
                self['booklist'].setList(self.bookmarks)
        elif not self.userMode:
            name = self['booklist'].getCurrent()
            self.session.openWithCallback(boundFunction(self.removeBookmark, name), MessageBox, _('Do you really want to remove your bookmark of %s?') % name)

    def removeBookmark(self, name, ret):
        if not ret:
            return
        if name in self.bookmarks:
            self.bookmarks.remove(name)
            self['booklist'].setList(self.bookmarks)

    def createDir(self):
        if self['filelist'].current_directory is not None:
            self.session.openWithCallback(self.createDirCallback, InputBox, title=_('Please enter name of the new directory'), text='')

    def createDirCallback(self, res):
        if res:
            path = os.path.join(self['filelist'].current_directory, res)
            if not pathExists(path):
                if not createDir(path):
                    self.session.open(MessageBox, _('Creating directory %s failed.') % path, type=MessageBox.TYPE_ERROR, timeout=5)
                self['filelist'].refresh()
            else:
                self.session.open(MessageBox, _('The path %s already exists.') % path, type=MessageBox.TYPE_ERROR, timeout=5)

    def removeDir(self):
        sel = self['filelist'].getSelection()
        if sel and pathExists(sel[0]):
            self.session.openWithCallback(boundFunction(self.removeDirCallback, sel[0]), MessageBox, _('Do you really want to remove directory %s from the disk?') % sel[0], type=MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _('Invalid directory selected: %s') % sel[0], type=MessageBox.TYPE_ERROR, timeout=5)

    def removeDirCallback(self, name, res):
        if res:
            if not removeDir(name):
                self.session.open(MessageBox, _('Removing directory %s failed. (Maybe not empty.)') % name, type=MessageBox.TYPE_ERROR, timeout=5)
            else:
                self['filelist'].refresh()
                self.removeBookmark(name, True)
                val = self.realBookmarks and self.realBookmarks.value
                if val and name in val:
                    val.remove(name)
                    self.realBookmarks.value = val
                    self.realBookmarks.save()

    def up(self):
        self[self.currList].up()
        self.updateTarget()

    def down(self):
        self[self.currList].down()
        self.updateTarget()

    def left(self):
        self[self.currList].pageUp()
        self.updateTarget()

    def right(self):
        self[self.currList].pageDown()
        self.updateTarget()

    def ok(self):
        if self.currList == 'filelist':
            if self['filelist'].canDescent():
                self['filelist'].descent()
                self.updateTarget()
        else:
            self.select()

    def cancel(self):
        self.close(None)

    def getPreferredFolder(self):
        if self.currList == 'filelist':
            return self['filelist'].getSelection()[0]
        else:
            return self['booklist'].getCurrent()

    def selectConfirmed(self, ret):
        if ret:
            ret = ''.join((self.getPreferredFolder(), self.filename))
            if self.realBookmarks:
                if self.autoAdd and ret not in self.bookmarks:
                    self.bookmarks.append(self.getPreferredFolder())
                    self.bookmarks.sort()
                if self.bookmarks != self.realBookmarks.value:
                    self.realBookmarks.value = self.bookmarks
                    self.realBookmarks.save()
            self.close(ret)

    def select(self):
        currentFolder = self.getPreferredFolder()
        if currentFolder is not None:
            if self.minFree is not None:
                try:
                    s = os.statvfs(currentFolder)
                    if s.f_bavail * s.f_bsize / 1000000 > self.minFree:
                        return self.selectConfirmed(True)
                except OSError:
                    pass

                self.session.openWithCallback(self.selectConfirmed, MessageBox, _('There might not be enough space on the selected partition..\nDo you really want to continue?'), type=MessageBox.TYPE_YESNO)
            else:
                self.selectConfirmed(True)

    def changeName(self):
        if self.filename != '':
            self.session.openWithCallback(self.nameChanged, InputBox, title=_('Please enter a new filename'), text=self.filename)

    def nameChanged(self, res):
        if res is not None:
            if len(res):
                self.filename = res
                self.updateTarget()
            else:
                self.session.open(MessageBox, _('An empty filename is illegal.'), type=MessageBox.TYPE_ERROR, timeout=5)

    def updateTarget(self):
        currFolder = self.getPreferredFolder()
        if currFolder is not None:
            free = ''
            try:
                stat = os.statvfs(currFolder)
                free = ('%0.f GB ' + _('free')) % (float(stat.f_bavail) * stat.f_bsize / 1024 / 1024 / 1024)
            except:
                pass

            self['targetfreespace'].setText(free)
            self['target'].setText(''.join((currFolder, self.filename)))
        else:
            self['target'].setText(_('Invalid location'))

    def showMenu(self):
        if not self.userMode and self.realBookmarks:
            if self.currList == 'filelist':
                menu = [(_('switch to bookmarks'), self.switchToBookList), (_('add bookmark'), self.addRemoveBookmark)]
                if self.editDir:
                    menu.extend(((_('create directory'), self.createDir), (_('remove directory'), self.removeDir)))
            else:
                menu = ((_('switch to filelist'), self.switchToFileList), (_('remove bookmark'), self.addRemoveBookmark))
            self.session.openWithCallback(self.menuCallback, ChoiceBox, title='', list=menu)

    def menuCallback(self, choice):
        if choice:
            choice[1]()

    def usermodeOn(self):
        self.switchToBookList()
        self['filelist'].hide()
        self['key_blue'].hide()

    def keyNumberGlobal(self, number):
        self.qs_timer.stop()
        if number != self.lastKey:
            self.nextKey()
            self.selectByStart()
            self.curr_pos += 1
        char = self.getKey(number)
        self.quickselect = self.quickselect[:self.curr_pos] + unicode(char)
        self.qs_timer_type = 0
        self.qs_timer.start(1000, 1)

    def selectByStart(self):
        if not self.quickselect:
            return
        if self['filelist'].getCurrentDirectory():
            files = self['filelist'].getFileList()
            idx = 0
            lookfor = self['filelist'].getCurrentDirectory() + self.quickselect
            for file in files:
                if file[0][0] and file[0][0].lower().startswith(lookfor):
                    self['filelist'].instance.moveSelectionTo(idx)
                    break
                idx += 1

    def timeout(self, force = False):
        if not force and self.qs_timer_type == 0:
            self.selectByStart()
            self.lastKey = -1
            self.qs_timer_type = 1
            self.qs_timer.start(1000, 1)
        else:
            self.qs_timer.stop()
            self.lastKey = -1
            self.curr_pos = -1
            self.quickselect = ''

    def __repr__(self):
        return str(type(self)) + '(' + self.text + ')'


def MovieLocationBox(session, text, dir, minFree = None):
    return LocationBox(session, text=text, currDir=dir, bookmarks=config.movielist.videodirs, autoAdd=True, editDir=True, inhibitDirs=defaultInhibitDirs, minFree=minFree)


class EPGLocationBox(LocationBox):

    def __init__(self, session):
        LocationBox.__init__(self, session, text=_('Where to save temporary EPG?'), currDir=config.misc.epgcachepath.value, bookmarks=config.misc.allowed_epgcachepath, autoAdd=True, editDir=True, inhibitDirs=['/bin',
         '/boot',
         '/dev',
         '/proc',
         '/sbin',
         '/sys'], minFree=None)
        self.skinName = 'LocationBox'

    def cancel(self):
        config.misc.epgcachepath.cancel()
        LocationBox.cancel(self)

    def selectConfirmed(self, ret):
        if ret:
            config.misc.epgcachepath.value = self.getPreferredFolder()
            config.misc.epgcachepath.save()
            LocationBox.selectConfirmed(self, ret)


class PiconLocationBox(LocationBox):

    def __init__(self, session):
        LocationBox.__init__(self, session, text=_('Where to load picon images?'), currDir=config.misc.picon_path.value, bookmarks=config.misc.allowed_picon_paths, autoAdd=True, editDir=True, inhibitDirs=['/bin',
         '/boot',
         '/dev',
         '/proc',
         '/sbin',
         '/sys'], minFree=None)
        self.skinName = 'LocationBox'

    def cancel(self):
        config.misc.picon_path.cancel()
        LocationBox.cancel(self)

    def selectConfirmed(self, ret):
        if ret:
            config.misc.picon_path.value = self.getPreferredFolder()
            config.misc.picon_path.save()
            LocationBox.selectConfirmed(self, ret)


class TimeshiftLocationBox(LocationBox):

    def __init__(self, session):
        LocationBox.__init__(self, session, text=_('Where to save temporary timeshift recordings?'), currDir=config.usage.timeshift_path.value, bookmarks=config.usage.allowed_timeshift_paths, autoAdd=True, editDir=True, inhibitDirs=defaultInhibitDirs, minFree=1024)
        self.skinName = 'LocationBox'

    def cancel(self):
        config.usage.timeshift_path.cancel()
        LocationBox.cancel(self)

    def selectConfirmed(self, ret):
        if ret:
            config.usage.timeshift_path.value = self.getPreferredFolder()
            config.usage.timeshift_path.save()
            LocationBox.selectConfirmed(self, ret)


class AutorecordLocationBox(LocationBox):

    def __init__(self, session):
        LocationBox.__init__(self, session, text=_('Where to save temporary timeshift recordings?'), currDir=config.usage.autorecord_path.value, bookmarks=config.usage.allowed_autorecord_paths, autoAdd=True, editDir=True, inhibitDirs=defaultInhibitDirs, minFree=1024)
        self.skinName = 'LocationBox'

    def cancel(self):
        config.usage.autorecord_path.cancel()
        LocationBox.cancel(self)

    def selectConfirmed(self, ret):
        if ret:
            config.usage.autorecord_path.setValue(self.getPreferredFolder())
            config.usage.autorecord_path.save()
            LocationBox.selectConfirmed(self, ret)
