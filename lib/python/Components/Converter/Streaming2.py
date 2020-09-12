from Converter import Converter
from Components.Element import cached
from pprint import pprint

class Streaming2(Converter):

    @cached
    def getText(self):
        service = self.source.service
        if service is None:
            return _('-NO SERVICE\n')
        streaming = service.stream()
        s = streaming and streaming.getStreamingData()
        if s is None or not any(s):
            err = hasattr(service, 'getError') and service.getError()
            if err:
                return _('-SERVICE ERROR:%d\n') % err
            else:
                return _('=NO STREAM\n')
        retval = '+%d:%s' % (s['demux'], ','.join([ '%x:%s' % (x[0], x[1]) for x in s['pids'] ]))
        if 'default_audio_pid' in s:
            retval += ',%x:%s' % (s['default_audio_pid'], 'default_audio_pid')
        retval += '\n'
        return retval

    text = property(getText)
