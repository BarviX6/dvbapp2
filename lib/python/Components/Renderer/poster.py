from Renderer import Renderer
from enigma import ePixmap, ePicLoad, eTimer
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
from Components.config import config
from Components.Language import language
from urllib2 import urlopen, quote
import json
import re
import os
import socket
try:
    if config.plugins.blackpanel.apitmdb.value != '':
        tmdb_api = config.plugins.blackpanel.apitmdb.value
    else:
        tmdb_api = '8fedefb08d7138abbb6d19ff66c9170c'
except:
    tmdb_api = '8fedefb08d7138abbb6d19ff66c9170c'

print 'apitmdb: ', tmdb_api
if os.path.isdir('/media/usb'):
    path_folder = '/media/usb/poster/'
else:
    path_folder = '/media/hdd/poster/'
try:
    folder_size = sum([ sum(map(lambda fname: os.path.getsize(os.path.join(path_folder, fname)), files)) for path_folder, folders, files in os.walk(path_folder) ])
    posters_sz = '%0.f' % (folder_size / 1048576.0)
    if posters_sz >= '10':
        import shutil
        shutil.rmtree(path_folder)
except:
    pass

class poster(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.pstrNm = ''
        self.evntNm = ''
        self.intCheck()

    def intCheck(self):
        try:
            socket.setdefaulttimeout(0.5)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
            return True
        except:
            return False

    GUI_WIDGET = ePixmap

    def changed(self, what):
        try:
            if not self.instance:
                return
            if what[0] == self.CHANGED_CLEAR:
                self.instance.hide()
            if what[0] != self.CHANGED_CLEAR:
                self.delay()
        except:
            pass

    def showPoster(self):
        self.event = self.source.event
        if self.event:
            evnt = self.event.getEventName()
            try:
                filterNm = re.sub('([\\(\\[]).*?([\\)\\]])|(: odc.\\d+)', ' ', evnt)
                evntNm = filterNm
            except:
                evntNm = evnt

            self.evntNm = evntNm
            self.dwn_poster = path_folder + '{}.jpg'.format(evntNm.replace(':', '-').replace('\xc2\xbf', '').replace('?', ''))
            pstrNm = path_folder + evntNm.replace(':', '-').replace('\xc2\xbf', '').replace('?', '') + '.jpg'
            if os.path.exists(pstrNm):
                size = self.instance.size()
                self.picload = ePicLoad()
                sc = AVSwitch().getFramebufferScale()
                if self.picload:
                    self.picload.setPara((size.width(),
                     size.height(),
                     sc[0],
                     sc[1],
                     False,
                     1,
                     '#00000000'))
                result = self.picload.startDecode(pstrNm, 0, 0, False)
                if result == 0:
                    ptr = self.picload.getData()
                    if ptr != None:
                        self.instance.setPixmap(ptr)
                        self.instance.show()
            else:
                self.downloadPoster()
                self.instance.hide()
        else:
            self.instance.hide()
            return

    def downloadPoster(self):
        try:
            if self.intCheck():
                self.year = self.filterSearch()
                url_tmdb = 'https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}'.format(self.srch, tmdb_api, quote(self.evntNm), language.getLanguage().replace('_', '-'))
                if self.year:
                    url_tmdb += '&primary_release_year={}&year={}'.format(self.year, self.year)
                poster = json.load(urlopen(url_tmdb))['results'][0]['poster_path']
                if poster:
                    self.url_poster = 'https://image.tmdb.org/t/p/w185{}'.format(poster)
                    self.savePoster()
            else:
                return
        except:
            try:
                if not os.path.exists(path_folder + self.evntNm + '.jpg'):
                    url_tmdb = 'https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}'.format(self.srch, tmdb_api, quote(self.evntNm), language.getLanguage().replace('_', '-'))
                    if self.year:
                        url_tmdb += '&primary_release_year={}&year={}'.format(self.year, self.year)
                    poster = json.load(urlopen(url_tmdb))['results'][0]['poster_path']
                    if poster:
                        self.url_poster = 'https://image.tmdb.org/t/p/w185{}'.format(poster)
                        self.savePoster()
            except:
                try:
                    url_tvdb = 'https://thetvdb.com/api/GetSeries.php?seriesname={}'.format(quote(self.evntNm))
                    url_read = urlopen(url_tvdb).read()
                    series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
                    if series_id:
                        url_tvdb = 'https://thetvdb.com/api/a99d487bb3426e5f3a60dea6d3d3c7ef/series/{}/en.xml'.format(series_id)
                        url_read = urlopen(url_tvdb).read()
                        poster = re.findall('<poster>(.*?)</poster>', url_read)[0]
                        if poster:
                            self.url_poster = 'https://artworks.thetvdb.com/banners/{}'.format(poster)
                            self.url_poster = self.url_poster.replace('.jpg', '_t.jpg')
                            self.savePoster()
                            url_read.close()
                        else:
                            return
                    else:
                        return
                except:
                    return

    def filterSearch(self):
        try:
            sd = self.event.getShortDescription() + '\n' + self.event.getExtendedDescription()
            w = ['serial',
             'series',
             'serie',
             'serien',
             's\xc3\xa9ries',
             'serious',
             'folge',
             'episodio',
             'episode',
             'ep.',
             'staffel',
             'soap',
             'doku',
             'tv',
             'talk',
             'show',
             'news',
             'factual',
             'entertainment',
             'telenovela',
             'dokumentation',
             'dokutainment',
             'documentary',
             'informercial',
             'information',
             'sitcom',
             'reality',
             'program',
             'magazine',
             'mittagsmagazin']
            for i in w:
                if i in sd.lower():
                    self.srch = 'tv'
                    break
                else:
                    self.srch = 'multi'

            pattern = ['(19[0-9][0-9])', '(20[0-9][0-9])']
            for i in pattern:
                yr = re.search(i, sd)
                if yr:
                    jr = yr.group(1)
                    return '{}'.format(jr)

            return ''
        except:
            return

    def delay(self):
        self.timer = eTimer()
        self.timer.callback.append(self.showPoster)
        self.timer.start(30, True)

    def savePoster(self):
        if not os.path.isdir(path_folder):
            os.makedirs(path_folder)
        with open(self.dwn_poster, 'wb') as f:
            f.write(urlopen(self.url_poster).read())
            f.close()
