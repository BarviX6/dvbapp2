from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Components.NimManager import nimmanager

class FrontendInfop(Converter, object):
    BER = 0
    SNR = 1
    AGC = 2
    LOCK = 3
    SNRdB = 4
    SLOT_NUMBER = 5
    TUNER_TYPE = 6
    STRING = 7
    NIMACTIVEA = 8
    NIMACTIVEB = 9
    NIMACTIVEC = 10
    NIMACTIVED = 11
    NIMACTIVEE = 12
    NIMACTIVEF = 13
    NIMACTIVEG = 14
    NIMACTIVEH = 15
    NIMACTIVEI = 16
    NIMACTIVEJ = 17
    NIMACTIVEK = 18
    NIMACTIVEL = 19
    NIMACTIVEM = 20
    NIMACTIVEN = 21
    NIMACTIVEO = 22
    NIMACTIVEP = 23
    NIMACTIVEQ = 24
    NIMACTIVER = 25

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'BER':
            self.type = self.BER
        elif type == 'SNR':
            self.type = self.SNR
        elif type == 'SNRdB':
            self.type = self.SNRdB
        elif type == 'AGC':
            self.type = self.AGC
        elif type == 'NUMBER':
            self.type = self.SLOT_NUMBER
        elif type == 'TYPE':
            self.type = self.TUNER_TYPE
        elif type == 'STRING':
            self.type = self.STRING
        elif type == 'NIMACTIVEA':
            self.type = self.NIMACTIVEA
        elif type == 'NIMACTIVEB':
            self.type = self.NIMACTIVEB
        elif type == 'NIMACTIVEC':
            self.type = self.NIMACTIVEC
        elif type == 'NIMACTIVED':
            self.type = self.NIMACTIVED
        elif type == 'NIMACTIVEE':
            self.type = self.NIMACTIVEE
        elif type == 'NIMACTIVEF':
            self.type = self.NIMACTIVEF
        elif type == 'NIMACTIVEG':
            self.type = self.NIMACTIVEG
        elif type == 'NIMACTIVEH':
            self.type = self.NIMACTIVEH
        elif type == 'NIMACTIVEI':
            self.type = self.NIMACTIVEI
        elif type == 'NIMACTIVEJ':
            self.type = self.NIMACTIVEJ
        elif type == 'NIMACTIVEK':
            self.type = self.NIMACTIVEK
        elif type == 'NIMACTIVEL':
            self.type = self.NIMACTIVEL
        elif type == 'NIMACTIVEM':
            self.type = self.NIMACTIVEM
        elif type == 'NIMACTIVEN':
            self.type = self.NIMACTIVEN
        elif type == 'NIMACTIVEO':
            self.type = self.NIMACTIVEO
        elif type == 'NIMACTIVEP':
            self.type = self.NIMACTIVEP
        elif type == 'NIMACTIVEQ':
            self.type = self.NIMACTIVEQ
        elif type == 'NIMACTIVER':
            self.type = self.NIMACTIVER
        else:
            self.type = self.LOCK

    def getText(self):
        percent = None
        swapsnr = config.usage.swap_snr_on_osd.value
        if self.type == self.BER:
            count = self.source.ber
            if count is not None:
                return str(count)
            else:
                return 'N/A'
        elif self.type == self.AGC:
            percent = self.source.agc
        elif self.type == self.SNR and not swapsnr or self.type == self.SNRdB and swapsnr:
            percent = self.source.snr
        elif self.type == self.SNR or self.type == self.SNRdB:
            if self.source.snr_db is not None:
                return '%3.01f dB' % (self.source.snr_db / 100.0)
            if self.source.snr is not None:
                percent = self.source.snr
        else:
            if self.type == self.TUNER_TYPE:
                return self.source.frontend_type and self.frontend_type or 'Unknown'
            if self.type == self.STRING:
                string = ''
                for n in nimmanager.nim_slots:
                    if n.type:
                        if string:
                            string += ' '
                        if n.slot == self.source.slot_number:
                            string += '\\c0000??00'
                        elif self.source.tuner_mask & 1 << n.slot:
                            string += '\\c00????00'
                        else:
                            string += '\\c007?7?7?'
                        string += chr(ord('A') + n.slot)

                return string
        if percent is None:
            return 'N/A'
        return '%d %%' % (percent * 100 / 65536)

    @cached
    def getBool(self):
        if self.type == self.LOCK:
            lock = self.source.lock
            if lock is None:
                lock = False
            return lock
        if self.type > 7:
            nims = len(nimmanager.nimList())
            if self.type == self.NIMACTIVEA:
                return nims > 0
            if self.type == self.NIMACTIVEB:
                return nims > 1
            if self.type == self.NIMACTIVEC:
                return nims > 2
            if self.type == self.NIMACTIVED:
                return nims > 3
            if self.type == self.NIMACTIVEE:
                return nims > 4
            if self.type == self.NIMACTIVEF:
                return nims > 5
            if self.type == self.NIMACTIVEG:
                return nims > 6
            if self.type == self.NIMACTIVEH:
                return nims > 7
            if self.type == self.NIMACTIVEI:
                return nims > 8
            if self.type == self.NIMACTIVEJ:
                return nims > 9
            if self.type == self.NIMACTIVEK:
                return nims > 10
            if self.type == self.NIMACTIVEL:
                return nims > 11
            if self.type == self.NIMACTIVEM:
                return nims > 12
            if self.type == self.NIMACTIVEN:
                return nims > 13
            if self.type == self.NIMACTIVEO:
                return nims > 14
            if self.type == self.NIMACTIVEP:
                return nims > 15
            if self.type == self.NIMACTIVEQ:
                return nims > 16
            if self.type == self.NIMACTIVER:
                return nims > 17
        else:
            ber = self.source.ber
            if ber is None:
                ber = 0
            return ber > 0

    text = property(getText)
    boolean = property(getBool)

    @cached
    def getValue(self):
        if self.type == self.AGC:
            return self.source.agc or 0
        if self.type == self.SNR:
            return self.source.snr or 0
        if self.type == self.BER:
            if self.BER < self.range:
                return self.BER or 0
            else:
                return self.range
        else:
            if self.type == self.TUNER_TYPE:
                type = self.source.frontend_type
                if type == 'DVB-S':
                    return 0
                if type == 'DVB-C':
                    return 1
                if type == 'DVB-T':
                    return 2
                if type == 'ATSC':
                    return 3
                return -1
            if self.type == self.SLOT_NUMBER:
                num = self.source.slot_number
                return num is None and -1 or num

    range = 65536
    value = property(getValue)
