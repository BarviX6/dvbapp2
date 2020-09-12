import struct
import os
import datetime
from fcntl import ioctl
from enigma import eTimer, eHdmiCEC, eActionMap
from config import config, ConfigSelection, ConfigYesNo, ConfigSubsection, ConfigText, NoSave
from Components.Console import Console
from Tools.Directories import fileExists, pathExists
from time import time
import Screens.Standby
from sys import maxint
config.hdmicec = ConfigSubsection()
config.hdmicec.enabled = ConfigYesNo(default=False)
config.hdmicec.control_tv_standby = ConfigYesNo(default=True)
config.hdmicec.control_tv_wakeup = ConfigYesNo(default=True)
config.hdmicec.report_active_source = ConfigYesNo(default=True)
config.hdmicec.report_active_menu = ConfigYesNo(default=True)
choicelist = [('disabled', _('Disabled')), ('standby', _('Standby')), ('deepstandby', _('Deep standby'))]
config.hdmicec.handle_tv_standby = ConfigSelection(default='standby', choices=choicelist)
config.hdmicec.handle_tv_input = ConfigSelection(default='disabled', choices=choicelist)
config.hdmicec.handle_tv_wakeup = ConfigSelection(choices={'disabled': _('Disabled'),
 'wakeup': _('Wakeup'),
 'tvreportphysicaladdress': _('TV physical address report'),
 'routingrequest': _('Routing request'),
 'sourcerequest': _('Source request'),
 'streamrequest': _('Stream request'),
 'osdnamerequest': _('OSD name request'),
 'activity': _('Any activity')}, default='streamrequest')
config.hdmicec.fixed_physical_address = ConfigText(default='0.0.0.0')
config.hdmicec.volume_forwarding = ConfigYesNo(default=False)
config.hdmicec.control_receiver_wakeup = ConfigYesNo(default=False)
config.hdmicec.control_receiver_standby = ConfigYesNo(default=False)
config.hdmicec.handle_deepstandby_events = ConfigYesNo(default=True)
config.hdmicec.preemphasis = ConfigYesNo(default=False)
choicelist = []
for i in (10,
 50,
 100,
 150,
 250,
 500,
 750,
 1000):
    choicelist.append(('%d' % i, _('%d ms') % i))

config.hdmicec.minimum_send_interval = ConfigSelection(default='250', choices=[('0', _('Disabled'))] + choicelist)
choicelist = []
for i in range(1, 6):
    choicelist.append(('%d' % i, _('%d times') % i))

config.hdmicec.messages_repeat = ConfigSelection(default='0', choices=[('0', _('Disabled'))] + choicelist)
config.hdmicec.messages_repeat_standby = ConfigYesNo(default=False)
choicelist = []
for i in (500,
 1000,
 2000,
 3000,
 4000,
 5000):
    choicelist.append(('%d' % i, _('%d ms') % i))

config.hdmicec.messages_repeat_slowdown = ConfigSelection(default='1000', choices=[('0', _('None'))] + choicelist)
choicelist = []
for i in (5,
 10,
 30,
 60,
 120,
 300,
 600,
 900,
 1800,
 3600):
    if i / 60 < 1:
        choicelist.append(('%d' % i, _('%d sec') % i))
    else:
        choicelist.append(('%d' % i, _('%d min') % (i / 60)))

config.hdmicec.handle_tv_delaytime = ConfigSelection(default='0', choices=[('0', _('None'))] + choicelist)
config.hdmicec.deepstandby_waitfortimesync = ConfigYesNo(default=True)
config.hdmicec.tv_wakeup_zaptimer = ConfigYesNo(default=True)
config.hdmicec.tv_wakeup_zapandrecordtimer = ConfigYesNo(default=True)
config.hdmicec.tv_wakeup_wakeuppowertimer = ConfigYesNo(default=True)
config.hdmicec.tv_standby_notinputactive = ConfigYesNo(default=True)
config.hdmicec.check_tv_state = ConfigYesNo(default=False)
config.hdmicec.workaround_activesource = ConfigYesNo(default=False)
choicelist = []
for i in (5,
 10,
 15,
 30,
 45,
 60):
    choicelist.append(('%d' % i, _('%d sec') % i))

config.hdmicec.workaround_turnbackon = ConfigSelection(default='0', choices=[('0', _('Disabled'))] + choicelist)
config.hdmicec.advanced_settings = ConfigYesNo(default=False)
config.hdmicec.default_settings = NoSave(ConfigYesNo(default=False))
config.hdmicec.debug = ConfigYesNo(default=False)
config.hdmicec.commandline = ConfigYesNo(default=False)
cmdfile = '/tmp/hdmicec_cmd'
msgfile = '/tmp/hdmicec_msg'
errfile = '/tmp/hdmicec_cmd_err.log'
hlpfile = '/tmp/hdmicec_cmd_hlp.txt'
cecinfo = 'http://www.cec-o-matic.com'
CECintcmd = {'Active Source': 'sourceactive',
 'Device Vendor ID': 'vendorid',
 'Give Device Power Status': 'powerstate',
 'Give System Audio Mode Status': 'givesystemaudiostatus',
 'Image View On': 'wakeup',
 'Inactive Source': 'sourceinactive',
 'Menu Status Activated': 'menuactive',
 'Menu Status Deactivated': 'menuinactive',
 'Report Physical Address': 'reportaddress',
 'Report Power Status On': 'poweractive',
 'Report Power Status Standby': 'powerinactive',
 'Routing Information': 'routinginfo',
 'Set OSD Name': 'osdname',
 'Set System Audio Mode Off': 'deactivatesystemaudiomode',
 'Set System Audio Mode On': 'activatesystemaudiomode',
 'Standby': 'standby',
 'System Audio Mode Request': 'setsystemaudiomode',
 'User Control Pressed Power Off': 'keypoweroff',
 'User Control Pressed Power On': 'keypoweron'}
CECaddr = {0: '<TV>',
 1: '<Recording 1>',
 2: '<Recording 2>',
 3: '<Tuner 1>',
 4: '<Playback 1>',
 5: '<Audio System>',
 6: '<Tuner 2>',
 7: '<Tuner 3>',
 8: '<Playback 2>',
 9: '<Playback 3>',
 10: '<Tuner 4>',
 11: '<Playback 2>',
 12: '<Reserved>',
 13: '<Reserved>',
 14: '<Specific>',
 15: '<Broadcast>'}
CECcmd = {0: '<Feature Abort>',
 4: '<Image View On>',
 5: '<Tuner Step Increment>',
 6: '<Tuner Step Decrement>',
 7: '<Tuner Device Status>',
 8: '<Give Tuner Device Status>',
 9: '<Record On>',
 10: '<Record Status>',
 11: '<Record Off>',
 13: '<Text View On>',
 15: '<Record TV Screen>',
 26: '<Give Deck Status>',
 27: '<Deck Status>',
 50: '<Set Menu Language>',
 51: '<Clear Analogue Timer>',
 52: '<Set Analogue Timer>',
 53: '<Timer Status>',
 54: '<Standby>',
 65: '<Play>',
 66: '<Deck Control>',
 67: '<Timer Cleared Status>',
 68: '<User Control Pressed>',
 69: '<User Control Released>',
 70: '<Give OSD Name>',
 71: '<Set OSD Name>',
 100: '<Set OSD String>',
 103: '<Set Timer Program Title>',
 112: '<System Audio Mode Request>',
 113: '<Give Audio Status>',
 114: '<Set System Audio Mode>',
 122: '<Report Audio Status>',
 125: '<Give System Audio Mode Status>',
 126: '<System Audio Mode Status>',
 128: '<Routing Change>',
 129: '<Routing Information>',
 130: '<Active Source>',
 131: '<Give Physical Address>',
 132: '<Report Physical Address>',
 133: '<Request Active Source>',
 134: '<Set Stream Path>',
 135: '<Device Vendor ID>',
 137: '<Vendor Command><Vendor Specific Data>',
 138: '<Vendor Remote Button Down><Vendor Specific RC Code>',
 139: '<Vendor Remote Button Up>',
 140: '<Give Device Vendor ID>',
 141: '<Menu Request>',
 142: '<Menu Status>',
 143: '<Give Device Power Status>',
 144: '<Report Power Status>',
 145: '<Get Menu Language>',
 146: '<Select Analogue Service>',
 147: '<Select Digital Service>',
 151: '<Set Digital Timer>',
 153: '<Clear Digital Timer>',
 154: '<Set Audio Rate>',
 157: '<Inactive Source>',
 158: '<CEC Version>',
 159: '<Get CEC Version>',
 160: '<Vendor Command With ID>',
 161: '<Clear External Timer>',
 162: '<Set External Timer>',
 255: '<Abort>'}
CECdat = {0: {0: '<Unrecognized opcode>',
     1: '<Not in correct mode to respond>',
     2: '<Cannot provide source>',
     3: '<Invalid operand>',
     4: '<Refused>'},
 8: {1: '<On>',
     2: '<Off>',
     3: '<Once>'},
 10: {1: '<Recording currently selected source>',
      2: '<Recording Digital Service>',
      3: '<Recording Analogue Service>',
      4: '<Recording External Input>',
      5: '<No recording - unable to record Digital Service>',
      6: '<No recording - unable to record Analogue Service>',
      7: '<No recording - unable to select required Service>',
      9: '<No recording - unable External plug number>',
      10: '<No recording - unable External plug number>',
      11: '<No recording - CA system not supported>',
      12: '<No recording - No or Insufficent CA Entitlements>',
      13: '<No recording - No allowed to copy source>',
      14: '<No recording - No futher copies allowed>',
      16: '<No recording - no media>',
      17: '<No recording - playing>',
      18: '<No recording - already recording>',
      19: '<No recording - media protected>',
      20: '<No recording - no source signa>',
      21: '<No recording - media problem>',
      22: '<No recording - no enough space available>',
      23: '<No recording - Parental Lock On>',
      26: '<Recording terminated normally>',
      27: '<Recording has already terminated>',
      31: '<No recording - other reason>'},
 27: {17: '<Play>',
      18: '<Record',
      19: '<Play Reverse>',
      20: '<Still>',
      21: '<Slow>',
      22: '<Slow Reverse>',
      23: '<Fast Forward>',
      24: '<Fast Reverse>',
      25: '<No Media>',
      26: '<Stop>',
      27: '<Skip Forward / Wind>',
      28: '<Skip Reverse / Rewind>',
      29: '<Index Search Forward>',
      30: '<Index Search Reverse>',
      31: '<Other Status>'},
 26: {1: '<On>',
      2: '<Off>',
      3: '<Once>'},
 65: {5: '<Play Forward Min Speed>',
      6: '<Play Forward Medium Speed>',
      7: '<Play Forward Max Speed>',
      9: '<Play Reverse Min Speed>',
      10: '<Play Reverse Medium Speed>',
      11: '<Play Reverse Max Speed>',
      21: '<Slow Forward Min Speed>',
      22: '<Slow Forward Medium Speed>',
      23: '<Slow Forward Max Speed>',
      25: '<Slow Reverse Min Speed>',
      26: '<Slow Reverse Medium Speed>',
      27: '<Slow Reverse Max Speed>',
      32: '<Play Reverse>',
      36: '<Play Forward>',
      37: '<Play Still>'},
 66: {1: '<Skip Forward / Wind>',
      2: '<Skip Reverse / Rewind',
      3: '<Stop>',
      4: '<Eject>'},
 67: {0: '<Timer not cleared - recording>',
      1: '<Timer not cleared - no matching>',
      2: '<Timer not cleared - no info available>',
      128: '<Timer cleared>'},
 68: {0: '<Select>',
      1: '<Up>',
      2: '<Down>',
      3: '<Left>',
      4: '<Right>',
      5: '<Right-Up>',
      6: '<Right-Down>',
      7: '<Left-Up>',
      8: '<Left-Down>',
      9: '<Root Menu>',
      10: '<Setup Menu>',
      11: '<Contents Menu>',
      12: '<Favorite Menu>',
      13: '<Exit>',
      14: '<Reserved 0x0E>',
      15: '<Reserved 0x0F>',
      16: '<Media Top Menu>',
      17: '<Media Context-sensitive Menu>',
      18: '<Reserved 0x12>',
      19: '<Reserved 0x13>',
      20: '<Reserved 0x14>',
      21: '<Reserved 0x15>',
      22: '<Reserved 0x16>',
      23: '<Reserved 0x17>',
      24: '<Reserved 0x18>',
      25: '<Reserved 0x19>',
      26: '<Reserved 0x1A>',
      27: '<Reserved 0x1B>',
      28: '<Reserved 0x1C>',
      29: '<Number Entry Mode>',
      30: '<Number 11>',
      31: '<Number 12>',
      32: '<Number 0 or Number 10>',
      33: '<Number 1>',
      34: '<Number 2>',
      35: '<Number 3>',
      36: '<Number 4>',
      37: '<Number 5>',
      38: '<Number 6>',
      39: '<Number 7>',
      40: '<Number 8>',
      41: '<Number 9>',
      42: '<Dot>',
      43: '<Enter>',
      44: '<Clear>',
      45: '<Reserved 0x2D>',
      46: '<Reserved 0x2E>',
      47: '<Next Favorite>',
      48: '<Channel Up>',
      49: '<Channel Down>',
      50: '<Previous Channel>',
      51: '<Sound Select>',
      52: '<Input Select>',
      53: '<Display Informationen>',
      54: '<Help>',
      55: '<Page Up>',
      56: '<Page Down>',
      57: '<Reserved 0x39>',
      58: '<Reserved 0x3A>',
      59: '<Reserved 0x3B>',
      60: '<Reserved 0x3C>',
      61: '<Reserved 0x3D>',
      62: '<Reserved 0x3E>',
      63: '<Reserved 0x3F>',
      64: '<Power>',
      65: '<Volume Up>',
      66: '<Volume Down>',
      67: '<Mute>',
      68: '<Play>',
      69: '<Stop>',
      70: '<Pause>',
      71: '<Record>',
      72: '<Rewind>',
      73: '<Fast Forward>',
      74: '<Eject>',
      75: '<Forward>',
      76: '<Backward>',
      77: '<Stop-Record>',
      78: '<Pause-Record>',
      79: '<Reserved 0x4F>',
      80: '<Angle>',
      81: '<Sub Picture>',
      82: '<Video On Demand>',
      83: '<Electronic Program Guide>',
      84: '<Timer programming>',
      85: '<Initial Configuration>',
      86: '<Reserved 0x56>',
      87: '<Reserved 0x57>',
      88: '<Reserved 0x58>',
      89: '<Reserved 0x59>',
      90: '<Reserved 0x5A>',
      91: '<Reserved 0x5B>',
      92: '<Reserved 0x5C>',
      93: '<Reserved 0x5D>',
      94: '<Reserved 0x5E>',
      95: '<Reserved 0x5F>',
      96: '<Play Function>',
      97: '<Pause-Play Function>',
      98: '<Record Function>',
      99: '<Pause-Record Function>',
      100: '<Stop Function>',
      101: '<Mute Function>',
      102: '<Restore Volume Function>',
      103: '<Tune Function>',
      104: '<Select Media Function>',
      105: '<Select A/V Input Function>',
      106: '<Select Audio Input Function>',
      107: '<Power Toggle Function>',
      108: '<Power Off Function>',
      109: '<Power On Function>',
      110: '<Reserved 0x6E>',
      111: '<Reserved 0x6E>',
      112: '<Reserved 0x70>',
      113: '<F1 (Blue)>',
      114: '<F2 (Red)>',
      115: '<F3 (Green)>',
      116: '<F4 (Yellow)>',
      117: '<F5>',
      118: '<Data>',
      119: '<Reserved 0x77>',
      120: '<Reserved 0x78>',
      121: '<Reserved 0x79>',
      122: '<Reserved 0x7A>',
      123: '<Reserved 0x7B>',
      124: '<Reserved 0x7C>',
      125: '<Reserved 0x7D>',
      126: '<Reserved 0x7E>',
      127: '<Reserved 0x7F>'},
 100: {0: '<Display for default time>',
       64: '<Display until cleared>',
       128: '<Clear previous message>',
       192: '<Reserved for future use>'},
 114: {0: '<Off>',
       1: '<On>'},
 126: {0: '<Off>',
       1: '<On>'},
 132: {0: '<TV>',
       1: '<Recording Device>',
       2: '<Reserved>',
       3: '<Tuner>',
       4: '<Playback Devive>',
       5: '<Audio System>',
       6: '<Pure CEC Switch>',
       7: '<Video Processor>'},
 141: {0: '<Activate>',
       1: '<Deactivate>',
       2: '<Query>'},
 142: {0: '<Activated>',
       1: '<Deactivated>'},
 144: {0: '<On>',
       1: '<Standby>',
       2: '<In transition Standby to On>',
       3: '<In transition On to Standby>'},
 154: {0: '<Rate Control Off>',
       1: '<WRC Standard Rate: 100% rate>',
       2: '<WRC Fast Rate: Max 101% rate>',
       3: '<WRC Slow Rate: Min 99% rate',
       4: '<NRC Standard Rate: 100% rate>',
       5: '<NRC Fast Rate: Max 100.1% rate>',
       6: '<NRC Slow Rate: Min 99.9% rate'},
 158: {0: '<1.1>',
       1: '<1.2>',
       2: '<1.2a>',
       3: '<1.3>',
       4: '<1.3a>',
       5: '<1.4>',
       6: '<2.0>'}}

class HdmiCec():
    instance = None

    def __init__(self):
        if config.hdmicec.enabled.value:
            HdmiCec.instance = self
            self.wait = eTimer()
            self.wait.timeout.get().append(self.sendCmd)
            self.queue = []
            self.messages = []
            self.handleTimer = eTimer()
            self.stateTimer = eTimer()
            self.stateTimer.callback.append(self.stateTimeout)
            self.repeatTimer = eTimer()
            self.repeatTimer.callback.append(self.repeatMessages)
            self.cmdPollTimer = eTimer()
            self.cmdPollTimer.callback.append(self.CECcmdline)
            self.cmdWaitTimer = eTimer()
            self.repeatCounter = 0
            self.what = ''
            self.tv_lastrequest = ''
            self.tv_powerstate = 'unknown'
            self.tv_skip_messages = False
            self.activesource = False
            self.firstrun = True
            self.standbytime = 0
            self.disk_full = False
            self.start_log = True
            self.sethdmipreemphasis()
            self.checkifPowerupWithoutWakingTv()
            eHdmiCEC.getInstance().messageReceived.get().append(self.messageReceived)
            config.misc.standbyCounter.addNotifier(self.onEnterStandby, initial_call=False)
            config.misc.DeepStandby.addNotifier(self.onEnterDeepStandby, initial_call=False)
            self.setFixedPhysicalAddress(config.hdmicec.fixed_physical_address.value)
            self.volumeForwardingEnabled = False
            self.volumeForwardingDestination = 0
            eActionMap.getInstance().bindAction('', -maxint - 1, self.keyEvent)
            config.hdmicec.volume_forwarding.addNotifier(self.configVolumeForwarding, initial_call=False)
            config.hdmicec.enabled.addNotifier(self.configVolumeForwarding)
            self.old_configReportActiveMenu = config.hdmicec.report_active_menu.value
            self.old_configTVstate = config.hdmicec.check_tv_state.value or config.hdmicec.tv_standby_notinputactive.value and config.hdmicec.control_tv_standby.value
            config.hdmicec.report_active_menu.addNotifier(self.configReportActiveMenu, initial_call=False)
            config.hdmicec.check_tv_state.addNotifier(self.configTVstate, initial_call=False)
            config.hdmicec.tv_standby_notinputactive.addNotifier(self.configTVstate, initial_call=False)
            config.hdmicec.control_tv_standby.addNotifier(self.configTVstate, initial_call=False)
            config.hdmicec.commandline.addNotifier(self.CECcmdstart)
            self.timerwakeup = True
            self.checkTVstate('firstrun')

    def getPhysicalAddress(self):
        physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
        hexstring = '%04x' % physicaladdress
        return hexstring[0] + '.' + hexstring[1] + '.' + hexstring[2] + '.' + hexstring[3]

    def setFixedPhysicalAddress(self, address):
        if address != config.hdmicec.fixed_physical_address.value:
            config.hdmicec.fixed_physical_address.value = address
            config.hdmicec.fixed_physical_address.save()
        hexstring = address[0] + address[2] + address[4] + address[6]
        eHdmiCEC.getInstance().setFixedPhysicalAddress(int(float.fromhex(hexstring)))

    def messageReceived(self, message):
        if config.hdmicec.enabled.value:
            checkstate = self.stateTimer.isActive()
            data = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            cmd = message.getCommand()
            length = message.getData(data, len(data))
            address = message.getAddress()
            cmdReceived = config.hdmicec.commandline.value and self.cmdWaitTimer.isActive()
            if config.hdmicec.debug.value or cmdReceived:
                self.CECdebug('Rx', address, cmd, data, length - 1, cmdReceived)
            if address > 15:
                self.CECwritedebug('[HdmiCec] workaround for wrong address active', True)
                address = 0
            if cmd == 0:
                if data[0] == 'D':
                    self.CECwritedebug('[HdmiCec] volume forwarding not supported by device %02x' % address, True)
                    self.volumeForwardingEnabled = False
            elif cmd == 70:
                self.sendMessage(address, 'osdname')
            elif cmd in (126, 114):
                if data[0] == '\x01':
                    self.volumeForwardingDestination = 5
                else:
                    self.volumeForwardingDestination = 0
                if config.hdmicec.volume_forwarding.value:
                    self.CECwritedebug('[HdmiCec] volume forwarding to device %02x enabled' % self.volumeForwardingDestination, True)
                    self.volumeForwardingEnabled = True
            elif cmd == 143:
                if Screens.Standby.inStandby:
                    self.sendMessage(address, 'powerinactive')
                else:
                    self.sendMessage(address, 'poweractive')
            elif cmd == 131:
                self.sendMessage(address, 'reportaddress')
            elif cmd == 133:
                if not Screens.Standby.inStandby and config.hdmicec.report_active_source.value:
                    self.sendMessage(address, 'sourceactive')
            elif cmd == 140:
                self.sendMessage(address, 'vendorid')
            elif cmd == 141:
                requesttype = ord(data[0])
                if requesttype == 2:
                    if Screens.Standby.inStandby:
                        self.sendMessage(address, 'menuinactive')
                    else:
                        self.sendMessage(address, 'menuactive')
            elif address == 0 and cmd == 144:
                if data[0] == '\x00':
                    self.tv_powerstate = 'on'
                elif data[0] == '\x01':
                    self.tv_powerstate = 'standby'
                elif data[0] == '\x02':
                    self.tv_powerstate = 'get_on'
                elif data[0] == '\x03':
                    self.tv_powerstate = 'get_standby'
                if checkstate and not self.firstrun:
                    self.checkTVstate('powerstate')
                elif self.firstrun and not config.hdmicec.handle_deepstandby_events.value:
                    self.firstrun = False
                else:
                    self.checkTVstate()
            elif address == 0 and cmd == 54:
                if config.hdmicec.handle_tv_standby.value != 'disabled':
                    self.handleTVRequest('tvstandby')
                self.checkTVstate('tvstandby')
            elif cmd == 128:
                oldaddress = ord(data[0]) * 256 + ord(data[1])
                newaddress = ord(data[2]) * 256 + ord(data[3])
                ouraddress = eHdmiCEC.getInstance().getPhysicalAddress()
                active = newaddress == ouraddress
                hexstring = '%04x' % oldaddress
                oldaddress = hexstring[0] + '.' + hexstring[1] + '.' + hexstring[2] + '.' + hexstring[3]
                hexstring = '%04x' % newaddress
                newaddress = hexstring[0] + '.' + hexstring[1] + '.' + hexstring[2] + '.' + hexstring[3]
                self.CECwritedebug("[HdmiCec] routing has changed... from '%s' to '%s' (to our address: %s)" % (oldaddress, newaddress, active), True)
            elif cmd in (134, 130):
                newaddress = ord(data[0]) * 256 + ord(data[1])
                ouraddress = eHdmiCEC.getInstance().getPhysicalAddress()
                active = newaddress == ouraddress
                if checkstate or self.activesource != active:
                    if checkstate:
                        txt = 'our receiver is active source'
                    else:
                        txt = 'active source'
                        if cmd == 134:
                            txt = 'streaming path'
                        txt += ' has changed... to our address'
                    self.CECwritedebug('[HdmiCec] %s: %s' % (txt, active), True)
                self.activesource = active
                if not checkstate:
                    if cmd == 134 and not Screens.Standby.inStandby and self.activesource:
                        self.sendMessage(address, 'sourceactive')
                        if config.hdmicec.report_active_menu.value:
                            self.sendMessage(0, 'menuactive')
                    if config.hdmicec.handle_tv_input.value != 'disabled':
                        self.handleTVRequest('activesource')
                    self.checkTVstate('changesource')
                else:
                    self.checkTVstate('activesource')
            wakeup = False
            if address == 0 and cmd == 68 and data[0] in ('@', 'm'):
                wakeup = True
            elif not checkstate and config.hdmicec.handle_tv_wakeup.value != 'disabled':
                if address == 0:
                    if cmd == 4 and config.hdmicec.handle_tv_wakeup.value == 'wakeup' or cmd == 133 and config.hdmicec.handle_tv_wakeup.value == 'sourcerequest' or cmd == 70 and config.hdmicec.handle_tv_wakeup.value == 'osdnamerequest' or cmd != 54 and config.hdmicec.handle_tv_wakeup.value == 'activity':
                        wakeup = True
                    elif cmd == 132 and config.hdmicec.handle_tv_wakeup.value == 'tvreportphysicaladdress':
                        if ord(data[0]) * 256 + ord(data[1]) == 0 and ord(data[2]) == 0:
                            wakeup = True
                if cmd == 128 and config.hdmicec.handle_tv_wakeup.value == 'routingrequest' or cmd == 134 and config.hdmicec.handle_tv_wakeup.value == 'streamrequest':
                    if active:
                        wakeup = True
            if wakeup:
                self.wakeup()

    def sendMessage(self, address, message):
        if config.hdmicec.enabled.value:
            cmd = 0
            data = ''
            if message == 'wakeup':
                from Screens.InfoBar import InfoBar
                noaction = InfoBar and InfoBar.instance and self.timerwakeup and InfoBar.instance.session.nav.wasTimerWakeup() and abs(time() - InfoBar.instance.session.nav.getWakeupTime()) <= 250
                self.timerwakeup = False
                if not noaction:
                    cmd = 4
            elif message == 'sourceactive':
                address = 15
                cmd = 130
                physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
                data = str(struct.pack('BB', int(physicaladdress / 256), int(physicaladdress % 256)))
            elif message == 'routinginfo':
                address = 15
                cmd = 129
                physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
                data = str(struct.pack('BB', int(physicaladdress / 256), int(physicaladdress % 256)))
            elif message == 'standby':
                cmd = 54
            elif message == 'sourceinactive':
                physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
                cmd = 157
                data = str(struct.pack('BB', int(physicaladdress / 256), int(physicaladdress % 256)))
            elif message == 'menuactive':
                cmd = 142
                data = str(struct.pack('B', 0))
            elif message == 'menuinactive':
                cmd = 142
                data = str(struct.pack('B', 1))
            elif message == 'givesystemaudiostatus':
                cmd = 125
            elif message == 'setsystemaudiomode':
                cmd = 112
                physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
                data = str(struct.pack('BB', int(physicaladdress / 256), int(physicaladdress % 256)))
            elif message == 'activatesystemaudiomode':
                cmd = 114
                data = str(struct.pack('B', 1))
            elif message == 'deactivatesystemaudiomode':
                cmd = 114
                data = str(struct.pack('B', 0))
            elif message == 'osdname':
                cmd = 71
                data = os.uname()[1]
                data = data[:14]
            elif message == 'poweractive':
                cmd = 144
                data = str(struct.pack('B', 0))
            elif message == 'powerinactive':
                cmd = 144
                data = str(struct.pack('B', 1))
            elif message == 'reportaddress':
                address = 15
                cmd = 132
                physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
                devicetype = eHdmiCEC.getInstance().getDeviceType()
                data = str(struct.pack('BBB', int(physicaladdress / 256), int(physicaladdress % 256), devicetype))
            elif message == 'vendorid':
                cmd = 135
                data = '\x00\x00\x00'
            elif message == 'keypoweron':
                cmd = 68
                data = str(struct.pack('B', 109))
            elif message == 'keypoweroff':
                cmd = 68
                data = str(struct.pack('B', 108))
            elif message == 'powerstate':
                cmd = 143
            if cmd:
                if config.misc.DeepStandby.value:
                    if config.hdmicec.debug.value:
                        self.CECdebug('Tx', address, cmd, data, len(data))
                    eHdmiCEC.getInstance().sendMessage(address, cmd, data, len(data))
                else:
                    self.queue.append((address, cmd, data))
                    if not self.wait.isActive():
                        self.wait.start(int(config.hdmicec.minimum_send_interval.value), True)

    def sendCmd(self):
        if len(self.queue):
            address, cmd, data = self.queue.pop(0)
            if config.hdmicec.debug.value:
                self.CECdebug('Tx', address, cmd, data, len(data))
            eHdmiCEC.getInstance().sendMessage(address, cmd, data, len(data))
            self.wait.start(int(config.hdmicec.minimum_send_interval.value), True)

    def sendMessages(self, messages):
        self.firstrun = False
        self.queue = []
        self.sendMessagesIsActive(True)
        sendCnt = 0
        for send in messages:
            address = send[0]
            message = send[1]
            if self.what == 'on' and (self.repeatCounter > 0 or self.activesource) and (message == 'standby' or message == 'wakeup' and not config.hdmicec.control_tv_wakeup.value):
                continue
            self.sendMessage(address, message)
            sendCnt += 1

        if sendCnt:
            self.repeatTimer.start(int(config.hdmicec.minimum_send_interval.value) * (len(messages) + 1) + self.sendSlower(), True)

    def repeatMessages(self):
        if len(self.queue):
            self.repeatTimer.start(1000, True)
        elif self.firstrun:
            if self.stateTimer.isActive():
                self.repeatTimer.start(1000, True)
            else:
                self.sendMessages(self.messages)
        elif self.repeatCounter < int(config.hdmicec.messages_repeat.value) and (self.what == 'on' or config.hdmicec.messages_repeat_standby.value and self.what == 'standby'):
            self.repeatCounter += 1
            self.sendMessages(self.messages)
        else:
            self.repeatCounter = 0
            self.checkTVstate(self.what)

    def sendSlower(self):
        if int(config.hdmicec.messages_repeat.value) and self.repeatCounter != int(config.hdmicec.messages_repeat.value):
            return int(config.hdmicec.messages_repeat_slowdown.value) * (self.repeatCounter or 1)
        return 0

    def wakeupMessages(self):
        self.handleTimerStop()
        if self.tv_skip_messages:
            self.tv_skip_messages = False
            self.CECwritedebug('[HdmiCec] Skip turning on TV', True)
        elif self.checkifPowerupWithoutWakingTv() == 'True':
            self.CECwritedebug("[HdmiCec] Skip waking TV, found 'True' in '/tmp/powerup_without_waking_tv.txt' (usually written by openWebif)", True)
        else:
            if config.hdmicec.enabled.value:
                self.messages = []
                self.what = 'on'
                self.repeatCounter = 0
                if config.hdmicec.workaround_activesource.value and config.hdmicec.report_active_source.value and not self.activesource and 'standby' not in self.tv_powerstate:
                    self.messages.append((0, 'standby'))
                    if not config.hdmicec.control_tv_wakeup.value:
                        self.messages.append((0, 'wakeup'))
                if config.hdmicec.control_tv_wakeup.value:
                    self.messages.append((0, 'wakeup'))
                if config.hdmicec.report_active_source.value:
                    self.messages.append((0, 'sourceactive'))
                if config.hdmicec.report_active_menu.value:
                    if not config.hdmicec.report_active_source.value and self.activesource:
                        self.messages.append((0, 'sourceactive'))
                    self.messages.append((0, 'menuactive'))
                if config.hdmicec.control_receiver_wakeup.value:
                    self.messages.append((5, 'keypoweron'))
                    self.messages.append((5, 'setsystemaudiomode'))
                if self.firstrun:
                    self.repeatTimer.start(1000, True)
                else:
                    self.sendMessages(self.messages)
            if os.path.exists('/usr/script/TvOn.sh'):
                Console().ePopen('/usr/script/TvOn.sh &')

    def standbyMessages(self):
        self.handleTimerStop()
        if self.tv_skip_messages:
            self.tv_skip_messages = False
            self.CECwritedebug('[HdmiCec] Skip turning off TV', True)
        elif config.hdmicec.control_tv_standby.value and not config.hdmicec.tv_standby_notinputactive.value and not self.sendMessagesIsActive() and not self.activesource and 'on' in self.tv_powerstate:
            self.CECwritedebug('[HdmiCec] Skip turning off TV - config: tv has another input active', True)
        else:
            if config.hdmicec.enabled.value:
                self.messages = []
                self.what = 'standby'
                self.repeatCounter = 0
                if config.hdmicec.control_tv_standby.value:
                    self.messages.append((0, 'standby'))
                else:
                    if config.hdmicec.report_active_source.value:
                        self.messages.append((0, 'sourceinactive'))
                    if config.hdmicec.report_active_menu.value:
                        self.messages.append((0, 'menuinactive'))
                if config.hdmicec.control_receiver_standby.value:
                    self.messages.append((5, 'keypoweroff'))
                self.sendMessages(self.messages)
            if os.path.exists('/usr/script/TvOff.sh'):
                Console().ePopen('/usr/script/TvOff.sh &')

    def sendMessagesIsActive(self, stopMessages = False):
        if stopMessages:
            active = False
            if self.wait.isActive():
                self.wait.stop()
                active = True
            if self.repeatTimer.isActive():
                self.repeatTimer.stop()
                active = True
            if self.stateTimer.isActive():
                self.stateTimer.stop()
                active = True
            return active
        else:
            return self.repeatTimer.isActive() or self.stateTimer.isActive()

    def stateTimeout(self):
        self.CECwritedebug('[HdmiCec] timeout for check TV state!', True)
        if 'on' in self.tv_powerstate:
            self.checkTVstate('activesource')
        elif self.tv_powerstate == 'unknown':
            self.checkTVstate('getpowerstate')
        elif self.firstrun and not config.hdmicec.handle_deepstandby_events.value:
            self.firstrun = False

    def checkTVstate(self, state = ''):
        if self.stateTimer.isActive():
            self.stateTimer.stop()
        timeout = 3000
        need_routinginfo = config.hdmicec.control_tv_standby.value and not config.hdmicec.tv_standby_notinputactive.value
        if 'source' in state:
            self.tv_powerstate = 'on'
            if state == 'activesource' and self.what == 'on' and config.hdmicec.report_active_source.value and not self.activesource and not self.firstrun:
                self.sendMessage(0, 'sourceactive')
                if need_routinginfo or config.hdmicec.check_tv_state.value:
                    self.sendMessage(0, 'routinginfo')
            if self.firstrun and not config.hdmicec.handle_deepstandby_events.value:
                self.firstrun = False
        elif state == 'tvstandby':
            self.activesource = False
            self.tv_powerstate = 'standby'
        elif state == 'firstrun' and (not config.hdmicec.handle_deepstandby_events.value and (need_routinginfo or config.hdmicec.report_active_menu.value) or config.hdmicec.check_tv_state.value or config.hdmicec.workaround_activesource.value):
            self.stateTimer.start(timeout, True)
            self.sendMessage(0, 'routinginfo')
        elif state == 'firstrun' and not config.hdmicec.handle_deepstandby_events.value:
            self.firstrun = False
        elif config.hdmicec.check_tv_state.value or 'powerstate' in state:
            if state == 'getpowerstate' or state in ('on', 'standby'):
                self.activesource = False
                if state in ('on', 'standby'):
                    self.tv_powerstate = 'unknown'
                else:
                    self.tv_powerstate = 'getpowerstate'
                self.stateTimer.start(timeout, True)
                self.sendMessage(0, 'powerstate')
            elif state == 'powerstate' and 'on' in self.tv_powerstate:
                self.stateTimer.start(timeout, True)
                self.sendMessage(0, 'routinginfo')
        elif state == 'on' and need_routinginfo:
            self.activesource = False
            self.tv_powerstate = 'unknown'
            self.stateTimer.start(timeout, True)
            self.sendMessage(0, 'routinginfo')
        elif state == 'standby' and config.hdmicec.control_tv_standby.value:
            self.activesource = False
            self.tv_powerstate = 'standby'

    def handleTimerStop(self, reset = False):
        if reset:
            self.tv_skip_messages = False
        if self.handleTimer.isActive():
            self.handleTimer.stop()
            if len(self.handleTimer.callback):
                target = 'standby'
                if 'deep' in str(self.handleTimer.callback[0]):
                    target = 'deep ' + target
                self.CECwritedebug('[HdmiCec] stopping Timer to %s' % target, True)

    def handleTVRequest(self, request):
        if request == 'activesource' and self.activesource or self.tv_lastrequest == 'tvstandby' and request == 'activesource' and self.handleTimer.isActive():
            self.handleTimerStop(True)
        else:
            if (request == self.tv_lastrequest or self.tv_lastrequest == 'tvstandby') and self.handleTimer.isActive() or request == 'activesource' and not self.activesource and self.sendMessagesIsActive():
                return
            self.handleTimerStop(True)
            self.tv_lastrequest = request
            standby = deepstandby = False
            if config.hdmicec.handle_tv_standby.value != 'disabled' and request == 'tvstandby':
                self.tv_skip_messages = False
                if config.hdmicec.handle_tv_standby.value == 'standby':
                    standby = True
                elif config.hdmicec.handle_tv_standby.value == 'deepstandby':
                    deepstandby = True
            elif config.hdmicec.handle_tv_input.value != 'disabled' and request == 'activesource':
                self.tv_skip_messages = True
                if config.hdmicec.handle_tv_input.value == 'standby':
                    standby = True
                elif config.hdmicec.handle_tv_input.value == 'deepstandby':
                    deepstandby = True
            if standby and Screens.Standby.inStandby:
                self.tv_skip_messages = False
                return
            if standby or deepstandby:
                while len(self.handleTimer.callback):
                    self.handleTimer.callback.pop()

            if standby:
                if int(config.hdmicec.handle_tv_delaytime.value):
                    self.handleTimer.callback.append(self.standby)
                    self.handleTimer.startLongTimer(int(config.hdmicec.handle_tv_delaytime.value))
                    self.CECwritedebug('[HdmiCec] starting Timer to standby in %s s' % config.hdmicec.handle_tv_delaytime.value, True)
                else:
                    self.standby()
            elif deepstandby:
                if int(config.hdmicec.handle_tv_delaytime.value):
                    self.handleTimer.callback.append(self.deepstandby)
                    self.handleTimer.startLongTimer(int(config.hdmicec.handle_tv_delaytime.value))
                    self.CECwritedebug('[HdmiCec] starting Timer to deep standby in %s s' % config.hdmicec.handle_tv_delaytime.value, True)
                else:
                    self.deepstandby()

    def deepstandby(self):
        import NavigationInstance
        now = time()
        recording = NavigationInstance.instance.getRecordingsCheckBeforeActivateDeepStandby()
        rectimer = abs(NavigationInstance.instance.RecordTimer.getNextRecordingTime() - now) <= 900 or NavigationInstance.instance.RecordTimer.getStillRecording() or abs(NavigationInstance.instance.RecordTimer.getNextZapTime() - now) <= 900
        pwrtimer = abs(NavigationInstance.instance.PowerTimer.getNextPowerManagerTime() - now) <= 900 or NavigationInstance.instance.PowerTimer.isProcessing(exceptTimer=0) or not NavigationInstance.instance.PowerTimer.isAutoDeepstandbyEnabled()
        if recording or rectimer or pwrtimer:
            self.CECwritedebug('[HdmiCec] go not into deepstandby... recording=%s, rectimer=%s, pwrtimer=%s' % (recording, rectimer, pwrtimer), True)
            self.standby()
        else:
            from Screens.InfoBar import InfoBar
            if InfoBar and InfoBar.instance:
                self.CECwritedebug('[HdmiCec] go into deepstandby...', True)
                InfoBar.instance.openInfoBarSession(Screens.Standby.TryQuitMainloop, 1)

    def standby(self):
        if not Screens.Standby.inStandby:
            import NavigationInstance
            NavigationInstance.instance.skipWakeup = True
            from Screens.InfoBar import InfoBar
            if InfoBar and InfoBar.instance:
                self.CECwritedebug('[HdmiCec] go into standby...', True)
                InfoBar.instance.openInfoBarSession(Screens.Standby.Standby)

    def wakeup(self):
        if int(config.hdmicec.workaround_turnbackon.value) and self.standbytime > time():
            self.CECwritedebug('[HdmiCec] ignore wakeup for %d seconds ...' % int(self.standbytime - time()), True)
            return
        self.standbytime = 0
        self.handleTimerStop(True)
        if Screens.Standby.inStandby:
            self.CECwritedebug('[HdmiCec] wake up...', True)
            Screens.Standby.inStandby.Power()

    def onLeaveStandby(self):
        self.wakeupMessages()

    def onEnterStandby(self, configElement):
        self.standbytime = time() + int(config.hdmicec.workaround_turnbackon.value)
        Screens.Standby.inStandby.onClose.append(self.onLeaveStandby)
        self.standbyMessages()

    def onEnterDeepStandby(self, configElement):
        if config.hdmicec.handle_deepstandby_events.value:
            self.standbyMessages()

    def configVolumeForwarding(self, configElement):
        if config.hdmicec.enabled.value and config.hdmicec.volume_forwarding.value:
            self.volumeForwardingEnabled = True
            self.sendMessage(5, 'givesystemaudiostatus')
        else:
            self.volumeForwardingEnabled = False

    def configReportActiveMenu(self, configElement):
        if self.old_configReportActiveMenu == config.hdmicec.report_active_menu.value:
            return
        self.old_configReportActiveMenu = config.hdmicec.report_active_menu.value
        if config.hdmicec.report_active_menu.value:
            self.sendMessage(0, 'sourceactive')
            self.sendMessage(0, 'menuactive')
        else:
            self.sendMessage(0, 'menuinactive')

    def configTVstate(self, configElement):
        if self.old_configTVstate == (config.hdmicec.check_tv_state.value or config.hdmicec.check_tv_state.value or config.hdmicec.tv_standby_notinputactive.value and config.hdmicec.control_tv_standby.value):
            return
        self.old_configTVstate = config.hdmicec.check_tv_state.value or config.hdmicec.check_tv_state.value or config.hdmicec.tv_standby_notinputactive.value and config.hdmicec.control_tv_standby.value
        if not self.sendMessagesIsActive() and self.old_configTVstate:
            self.sendMessage(0, 'powerstate')
            self.sendMessage(0, 'routinginfo')

    def keyEvent(self, keyCode, keyEvent):
        if not self.volumeForwardingEnabled:
            return
        cmd = 0
        address = keyEvent
        data = ''
        if keyEvent in (0, 2):
            if keyCode == 115:
                cmd = 68
                data = str(struct.pack('B', 65))
            elif keyCode == 114:
                cmd = 68
                data = str(struct.pack('B', 66))
            elif keyCode == 113:
                cmd = 68
                data = str(struct.pack('B', 67))
        elif keyEvent == 1 and keyCode in (113, 114, 115):
            cmd = 69
        if cmd:
            if config.hdmicec.debug.value:
                self.CECdebug('Tx', address, cmd, data, len(data))
            eHdmiCEC.getInstance().sendMessage(self.volumeForwardingDestination, cmd, data, len(data))
            return 1
        else:
            return 0

    def sethdmipreemphasis(self):
        f = '/proc/stb/hdmi/preemphasis'
        if fileExists(f):
            if config.hdmicec.preemphasis.value == True:
                self.CECwritefile(f, 'w', 'on')
            else:
                self.CECwritefile(f, 'w', 'off')

    def checkifPowerupWithoutWakingTv(self):
        f = '/tmp/powerup_without_waking_tv.txt'
        powerupWithoutWakingTv = self.CECreadfile(f) or 'False' if fileExists(f) else 'False'
        self.CECwritefile(f, 'w', 'False')
        return powerupWithoutWakingTv

    def CECdebug(self, type, address, cmd, data, length, cmdmsg = False):
        txt = '<%s:> ' % type
        tmp = '%02X ' % address
        tmp += '%02X ' % cmd
        for i in range(length):
            tmp += '%02X ' % ord(data[i])

        if cmdmsg:
            self.CECcmdline(tmp)
            if not config.hdmicec.debug.value:
                return
        txt += '%s ' % (tmp.rstrip() + (47 - len(tmp.rstrip())) * ' ')
        txt += CECaddr.get(address, '<unknown>')
        if not cmd and not length:
            txt += '<Polling Message>'
        else:
            txt += CECcmd.get(cmd, '<Polling Message>')
            if cmd in (7, 9, 51, 52, 53, 146, 147, 151, 153, 161, 162):
                txt += '<unknown (not implemented yet)>'
            elif cmd == 0:
                if length == 2:
                    txt += CECcmd.get(ord(data[0]), '<unknown>')
                    txt += CECdat.get(cmd, '').get(ord(data[1]), '<unknown>')
                else:
                    txt += '<wrong data length>'
            elif cmd in (112, 128, 129, 130, 132, 134, 157):
                if cmd == 128 and length == 4 or cmd == 132 and length == 3 or cmd not in (128, 132) and length == 2:
                    hexstring = '%04x' % (ord(data[0]) * 256 + ord(data[1]))
                    txt += '<%s.%s.%s.%s>' % (hexstring[0],
                     hexstring[1],
                     hexstring[2],
                     hexstring[3])
                    if cmd == 128:
                        hexstring = '%04x' % (ord(data[2]) * 256 + ord(data[3]))
                        txt += '<%s.%s.%s.%s>' % (hexstring[0],
                         hexstring[1],
                         hexstring[2],
                         hexstring[3])
                    elif cmd == 132:
                        txt += CECdat.get(cmd, '').get(ord(data[2]), '<unknown>')
                else:
                    txt += '<wrong data length>'
            elif cmd in (135, 160):
                if length > 2:
                    txt += '<%d>' % (ord(data[0]) * 256 * 256 + ord(data[1]) * 256 + ord(data[2]))
                    if cmd == 160:
                        txt += '<Vendor Specific Data>'
                else:
                    txt += '<wrong data length>'
            elif cmd in (50, 71, 100, 103):
                if length:
                    s = 0
                    if cmd == 100:
                        s = 1
                        txt += CECdat.get(cmd, '').get(ord(data[0]), '<unknown>')
                    txt += '<'
                    for i in range(s, length):
                        txt += '%s' % data[i]

                    txt += '>'
                else:
                    txt += '<wrong data length>'
            elif cmd == 122:
                if length == 1:
                    val = ord(data[0])
                    txt += '<Audio Mute On>' if val >= 128 else '<Audio Mute Off>'
                    txt += '<Volume %d>' % (val - 128) if val >= 128 else '<Volume %d>' % val
                else:
                    txt += '<wrong data length>'
            elif length:
                txt += CECdat.get(cmd, '').get(ord(data[0]), '<unknown>') if CECdat.has_key(cmd) else ''
            else:
                txt += CECdat.get(cmd, '')
        self.CECwritedebug(txt)

    def CECwritedebug(self, debugtext, debugprint = False):
        if debugprint and not config.hdmicec.debug.value:
            print debugtext
            return
        log_path = config.crash.debug_path.value
        if pathExists(log_path):
            stat = os.statvfs(log_path)
            disk_free = stat.f_bavail * stat.f_bsize / 1024
            if self.disk_full:
                self.start_log = True
            if not self.disk_full and disk_free < 500:
                print '[HdmiCec] write debug file failed - disk full!'
                self.disk_full = True
                return
            if not self.disk_full and disk_free < 1000:
                self.disk_full = True
            elif disk_free >= 1000:
                self.disk_full = False
            else:
                return
            now = datetime.datetime.now()
            debugfile = os.path.join(log_path, now.strftime('Enigma2-hdmicec-%Y%m%d.log'))
            timestamp = now.strftime('%H:%M:%S.%f')[:-2]
            debugtext = '%s %s%s\n' % (timestamp, '[   ] ' if debugprint else '', debugtext.replace('[HdmiCec] ', ''))
            if self.start_log:
                self.start_log = False
                la = eHdmiCEC.getInstance().getLogicalAddress()
                debugtext = '%s  +++  start logging  +++  physical address: %s  -  logical address: %d  -  device type: %s\n%s' % (timestamp,
                 self.getPhysicalAddress(),
                 la,
                 CECaddr.get(la, '<unknown>'),
                 debugtext)
            if self.disk_full:
                debugtext += '%s  +++  stop logging  +++  disk full!\n' % timestamp
            self.CECwritefile(debugfile, 'a', debugtext)
        else:
            print '[HdmiCec] write debug file failed - log path (%s) not found!' % log_path

    def CECcmdstart(self, configElement):
        if config.hdmicec.commandline.value:
            self.CECcmdline('start')
        else:
            self.CECcmdline('stop')

    def CECcmdline(self, received = None):
        polltime = 1
        waittime = 3
        if self.cmdPollTimer.isActive():
            self.cmdPollTimer.stop()
        if not config.hdmicec.enabled.value or received in ('start', 'stop'):
            self.CECremovefiles((cmdfile, msgfile, errfile))
            if received == 'start':
                self.cmdPollTimer.startLongTimer(polltime)
            return
        if received:
            self.CECwritefile(msgfile, 'w', received.rstrip().replace(' ', ':') + '\n')
            if self.cmdWaitTimer.isActive():
                self.cmdWaitTimer.stop()
        if self.firstrun or self.sendMessagesIsActive():
            self.cmdPollTimer.startLongTimer(polltime)
            return
        if fileExists(cmdfile):
            files = [cmdfile, errfile]
            if received is None and not self.cmdWaitTimer.isActive():
                files.append(msgfile)
            ceccmd = self.CECreadfile(cmdfile).strip().split(':')
            self.CECremovefiles(files)
            if len(ceccmd) == 1 and not ceccmd[0]:
                e = 'Empty input file!'
                self.CECwritedebug('[HdmiCec] CECcmdline - error: %s' % e, True)
                txt = '%s\n' % e
                self.CECwritefile(errfile, 'w', txt)
            elif ceccmd[0] in ('help', '?'):
                internaltxt = '  Available internal commands: '
                space = len(internaltxt) * ' '
                addspace = False
                for key in sorted(CECintcmd.keys()):
                    internaltxt += "%s'%s' or '%s'\n" % (space if addspace else '', key, CECintcmd[key])
                    addspace = True

                txt = 'Help for the hdmi-cec command line function\n'
                txt += '-------------------------------------------\n\n'
                txt += 'Files:\n'
                txt += "- Input file to send the hdmi-cec command line: '%s'\n" % cmdfile
                txt += "- Output file for received hdmi-cec messages:   '%s'\n" % msgfile
                txt += "- Error file for hdmi-cec command line errors:  '%s'\n" % errfile
                txt += "- This help file:                               '%s'\n\n" % hlpfile
                txt += 'Functions:\n'
                txt += "- Help: Type 'echo help > %s' to create this file.\n\n" % cmdfile
                txt += "- Send internal commands: address:command (e.g. Type 'echo 00:wakeup > %s' for wakeup the TV device.)\n" % cmdfile
                txt += '%s\n' % internaltxt
                txt += "- Send individual commands: address:command:data (e.g. Type 'echo 00:04 > %s' for wakeup the TV device.)\n" % cmdfile
                txt += '  Available individual commands: %s\n\n' % cecinfo
                txt += 'Info:\n'
                txt += '- Input and error file will removed with send a new command line. Output file will removed if not waiting for a message.\n'
                txt += '  (If the command was accepted successfully, the input file is deleted and no error file exist.)\n'
                txt += '- Poll time for new command line is %d second. Maximum wait time for one received message is %d seconds after send the hdmi-cec command.\n' % (polltime, waittime)
                txt += "  (After the first incoming message and outside this waiting time no more received messages will be write to '%s'.)\n" % msgfile
                txt += '- Address, command and optional data must write as hex values and text for internal command must write exactly!\n\n'
                txt += 'End\n'
                self.CECwritefile(hlpfile, 'w', txt)
            else:
                try:
                    if not ceccmd[0] or ceccmd[0] and len(ceccmd[0].strip()) > 2:
                        raise Exception("Wrong address detected - '%s'" % ceccmd[0])
                    address = int(ceccmd[0] or '0', 16)
                    if len(ceccmd) > 1:
                        if ceccmd[1] in CECintcmd.keys():
                            self.sendMessage(address, CECintcmd[ceccmd[1]])
                        elif ceccmd[1] in CECintcmd.values():
                            self.sendMessage(address, ceccmd[1])
                        else:
                            for x in ceccmd[1:]:
                                if len(x.strip()) > 2:
                                    raise Exception("Wrong command or incorrect data detected - '%s'" % x)

                            data = ''
                            cmd = int(ceccmd[1] or '0', 16)
                            if len(ceccmd) > 2:
                                for d in ceccmd[2:]:
                                    data += str(struct.pack('B', int(d or '0', 16)))

                            if config.hdmicec.debug.value:
                                self.CECdebug('Tx', address, cmd, data, len(data))
                            eHdmiCEC.getInstance().sendMessage(address, cmd, data, len(data))
                        self.cmdWaitTimer.startLongTimer(waittime)
                except Exception as e:
                    self.CECwritedebug('[HdmiCec] CECcmdline - error: %s' % e, True)
                    txt = '%s\n' % e
                    self.CECwritefile(errfile, 'w', txt)

        self.cmdPollTimer.startLongTimer(polltime)

    def CECreadfile(self, FILE):
        try:
            with open(FILE) as f:
                return f.read()
        except Exception as e:
            self.CECwritedebug("[HdmiCec] read file '%s' failed - error: %s" % (FILE, e), True)

        return ''

    def CECwritefile(self, FILE, MODE, INPUT):
        try:
            with open(FILE, MODE) as f:
                f.write(INPUT)
        except Exception as e:
            txt = "[HdmiCec] write file '%s' failed - error: %s" % (FILE, e)
            print txt if 'Enigma2-hdmicec-' in FILE else self.CECwritedebug(txt, True)

    def CECremovefiles(self, FILES):
        for f in FILES:
            if fileExists(f):
                try:
                    os.remove(f)
                except Exception as e:
                    self.CECwritedebug("[HdmiCec] remove file '%s' failed - error: %s" % (f, e), True)


hdmi_cec = HdmiCec()
