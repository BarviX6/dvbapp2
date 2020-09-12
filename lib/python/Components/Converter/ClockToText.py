from Converter import Converter
from time import localtime, strftime
from Components.Element import cached
from Components.config import config

class ClockToText(Converter, object):
    TIME_OPTIONS = {'': lambda t: strftime(config.usage.time.short.value, localtime(t)),
     'AsLength': lambda t: ('' if t < 0 else '%d:%02d' % (t / 60, t % 60)),
     'AsLengthHours': lambda t: ('' if t < 0 else '%d:%02d' % (t / 3600, t / 60 % 60)),
     'AsLengthSeconds': lambda t: ('' if t < 0 else '%d:%02d:%02d' % (t / 3600, t / 60 % 60, t % 60)),
     'Date': lambda t: strftime(config.usage.date.dayfull.value, localtime(t)),
     'Default': lambda t: strftime(config.usage.time.short.value, localtime(t)),
     'Display': lambda t: strftime(config.usage.time.display.value, localtime(t)),
     'DisplayDate': lambda t: strftime(config.usage.date.display.value, localtime(t)),
     'DisplayDayDate': lambda t: strftime(config.usage.date.displayday.value, localtime(t)),
     'DisplayTime': lambda t: strftime(config.usage.time.display.value, localtime(t)),
     'Full': lambda t: strftime(config.usage.date.dayshort.value + ' ' + config.usage.time.short.value, localtime(t)),
     'FullDate': lambda t: strftime(config.usage.date.shortdayfull.value, localtime(t)),
     'InMinutes': lambda t: ngettext('%d Min', '%d Mins', t / 60) % (t / 60),
     'LongDate': lambda t: strftime(config.usage.date.dayshortfull.value, localtime(t)),
     'LongFullDate': lambda t: strftime(config.usage.date.daylong.value + '  ' + config.usage.time.short.value, localtime(t)),
     'Mixed': lambda t: strftime(config.usage.time.mixed.value, localtime(t)),
     'ShortDate': lambda t: strftime(config.usage.date.dayshort.value, localtime(t)),
     'ShortFullDate': lambda t: strftime(config.usage.date.daylong.value, localtime(t)),
     'Timestamp': lambda t: str(t),
     'VFD': lambda t: strftime(config.usage.date.compact.value + config.usage.time.display.value, localtime(t)),
     'VFD08': lambda t: strftime(config.usage.time.display.value, localtime(t)),
     'VFD11': lambda t: strftime(config.usage.date.compressed.value + config.usage.time.display.value, localtime(t)),
     'VFD12': lambda t: strftime(config.usage.date.compact.value + config.usage.time.display.value, localtime(t)),
     'VFD14': lambda t: strftime(config.usage.date.short.value + ' ' + config.usage.time.display.value, localtime(t)),
     'VFD18': lambda t: strftime(config.usage.date.dayshort.value + ' ' + config.usage.time.display.value, localtime(t)),
     'WithSeconds': lambda t: strftime(config.usage.time.long.value, localtime(t))}

    def __init__(self, type):
        Converter.__init__(self, type)
        self.separator = ' - '
        self.formats = []
        type = type.lstrip()
        if type[0:5] == 'Parse':
            parse = type[5:6]
        else:
            parse = ';'
            if type[0:6] != 'Format':
                type = type.replace(',', ';')
        args = [ arg.lstrip() for arg in type.split(parse) ]
        for arg in args:
            if arg[0:6] == 'Format':
                self.formats.append(eval('lambda t: strftime("%s", localtime(t))' % arg[7:]))
                continue
            if arg[0:7] == 'NoSpace':
                continue
            if arg[0:5] == 'Parse':
                continue
            if arg[0:12] == 'Proportional':
                continue
            if arg[0:9] == 'Separator':
                self.separator = arg[10:]
                continue
            self.formats.append(self.TIME_OPTIONS.get(arg, lambda t: '???'))

        if len(self.formats) == 0:
            self.formats.append(self.TIME_OPTIONS.get('Default', lambda t: '???'))

    @cached
    def getText(self):
        time = self.source.time
        if time is None:
            return ''
        elif isinstance(time, tuple):
            entries = len(self.formats)
            index = 0
            results = []
            for t in time:
                if index < entries:
                    results.append(self.formats[index](t))
                else:
                    results.append(self.formats[-1](t))
                index += 1

            return self.separator.join(results)
        else:
            return self.formats[0](time)

    text = property(getText)
