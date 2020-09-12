from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import re
import os
import urllib2
api = 'your api key'

class infoMovie(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = type

    @cached
    def getText(self):
        event = self.source.event
        if event:
            if self.type == 'INFO':
                try:
                    evnt = event.getEventName()
                    try:
                        p = '((.*?))[;=:-].*?(.*?)'
                        e1 = re.search(p, evnt)
                        ffilm = re.sub('\\W+', '+', e1.group(1))
                    except:
                        w = re.sub('([\\(\\[]).*?([\\)\\]])', ' ', evnt)
                        ffilm = re.sub('\\W+', '+', w)

                    url = 'https://www.omdbapi.com/?apikey=%s&t=%s' % (api, ffilm.lower())
                    data = json.load(urllib2.urlopen(url))
                    title = data['Title']
                    rtng = data['imdbRating']
                    country = data['Country']
                    year = data['Year']
                    rate = data['Rated']
                    genre = data['Genre']
                    award = data['Awards']
                    if title:
                        return 'Title : %s' % str(title) + '\nImdb : %s' % str(rtng) + '\nYear : %s, %s' % (str(country), str(year.encode('utf-8'))) + '\nRate : %s' % str(rate) + '\nGenre : %s' % str(genre) + '\nAwards : %s' % str(award)
                except:
                    return ''

        else:
            return ''

    text = property(getText)

    @cached
    def getValue(self):
        event = self.source.event
        if event:
            if self.type == 'STARS':
                try:
                    evnt = event.getEventName()
                    try:
                        p = '((.*?))[;=:-].*?(.*?)'
                        e1 = re.search(p, evnt)
                        ffilm = re.sub('\\W+', '+', e1.group(1))
                    except:
                        w = re.sub('([\\(\\[]).*?([\\)\\]])', ' ', evnt)
                        ffilm = re.sub('\\W+', '+', w)

                    url = 'https://www.omdbapi.com/?apikey=%s&t=%s' % (api, ffilm.lower())
                    data = json.load(urllib2.urlopen(url))
                    rtng = data['imdbRating']
                    if rtng == 'N/A' or rtng == '':
                        return 0
                    return int(10 * float(rtng))
                except:
                    return 0

        else:
            return 0

    value = property(getValue)
    range = 100
