

class GenresETSI:
    maintype = (_('Reserved'),
     _('Movie/Drama'),
     _('News/Current Affairs'),
     _('Show/Games show'),
     _('Sports'),
     _('Children/Youth'),
     _('Music/Ballet/Dance'),
     _('Arts/Culture'),
     _('Social/Political/Economics'),
     _('Education/Science/Factual'),
     _('Leisure hobbies'),
     _('Other'))
    subtype = {1: (_('movie/drama (general)'),
         _('detective/thriller'),
         _('adventure/western/war'),
         _('science fiction/fantasy/horror'),
         _('comedy'),
         _('soap/melodrama/folkloric'),
         _('romance'),
         _('serious/classical/religious/historical movie/drama'),
         _('adult movie/drama')),
     2: (_('news/current affairs (general)'),
         _('news/weather report'),
         _('news magazine'),
         _('documentary'),
         _('discussion/interview/debate')),
     3: (_('show/game show (general)'),
         _('game show/quiz/contest'),
         _('variety show'),
         _('talk show')),
     4: (_('sports (general)'),
         _('special events'),
         _('sports magazine'),
         _('football/soccer'),
         _('tennis/squash'),
         _('team sports'),
         _('athletics'),
         _('motor sport'),
         _('water sport'),
         _('winter sport'),
         _('equestrian'),
         _('martial sports')),
     5: (_("children's/youth program (general)"),
         _("pre-school children's program"),
         _('entertainment (6-14 year old)'),
         _('entertainment (10-16 year old)'),
         _('information/education/school program'),
         _('cartoon/puppets')),
     6: (_('music/ballet/dance (general)'),
         _('rock/pop'),
         _('serious music/classic music'),
         _('folk/traditional music'),
         _('jazz'),
         _('musical/opera'),
         _('ballet')),
     7: (_('arts/culture (without music, general)'),
         _('performing arts'),
         _('fine arts'),
         _('religion'),
         _('popular culture/traditional arts'),
         _('literature'),
         _('film/cinema'),
         _('experimental film/video'),
         _('broadcasting/press'),
         _('new media'),
         _('arts/culture magazine'),
         _('fashion')),
     8: (_('social/political issues/economics (general)'),
         _('magazines/reports/documentary'),
         _('economics/social advisory'),
         _('remarkable people')),
     9: (_('education/science/factual topics (general)'),
         _('nature/animals/environment'),
         _('technology/natural science'),
         _('medicine/physiology/psychology'),
         _('foreign countries/expeditions'),
         _('social/spiritual science'),
         _('further education'),
         _('languages')),
     10: (_('leisure hobbies (general)'),
          _('tourism/travel'),
          _('handicraft'),
          _('motoring'),
          _('fitness & health'),
          _('cooking'),
          _('advertisement/shopping'),
          _('gardening')),
     11: (_('original language'),
          _('black & white'),
          _('unpublished'),
          _('live broadcast'))}


class GenresAUS:
    maintype = (_('Undefined'),
     _('Movie'),
     _('News'),
     _('Entertainment'),
     _('Sport'),
     _('Childrens'),
     _('Music'),
     _('Arts/Culture'),
     _('Current Affairs'),
     _('Education/Information'),
     _('Infotainment'),
     _('Special'),
     _('Comedy'),
     _('Drama'),
     _('Documentary'))
    subtype = {1: (_('movie (general)'),),
     2: (_('news (general)'),),
     3: (_('entertainment (general)'),),
     4: (_('sport (general)'),),
     5: (_('childrens (general)'),),
     6: (_('music (general)'),),
     7: (_('arts/culture (general)'),),
     8: (_('current affairs (general)'),),
     9: (_('education/information (general)'),),
     10: (_('infotainment (general)'),),
     11: (_('special (general)'),),
     12: (_('comedy (general)'),),
     13: (_('drama (general)'),),
     14: (_('documentary (general)'),)}


def __getGenreStringMain(hn, ln, genres):
    if hn == 15:
        return _('User defined')
    if 0 < hn < len(genres.maintype):
        return genres.maintype[hn]
    return ''


def __getGenreStringSub(hn, ln, genres):
    if hn == 15:
        return _('User defined') + ' ' + str(ln)
    if 0 < hn < len(genres.maintype):
        if ln == 15:
            return _('User defined')
        if ln < len(genres.subtype[hn]):
            return genres.subtype[hn][ln]
    return ''


countries = {'AUS': (__getGenreStringMain, __getGenreStringMain, GenresAUS())}
defaultGenre = GenresETSI()
defaultCountryInfo = (__getGenreStringMain, __getGenreStringSub, defaultGenre)
maintype = defaultGenre.maintype
subtype = defaultGenre.subtype

def getGenreStringMain(hn, ln, country = None):
    countryInfo = countries.get(country, defaultCountryInfo)
    return countryInfo[0](hn, ln, countryInfo[2])


def getGenreStringSub(hn, ln, country = None):
    countryInfo = countries.get(country, defaultCountryInfo)
    return countryInfo[1](hn, ln, countryInfo[2])


def getGenreStringLong(hn, ln, country = None):
    if hn == 15:
        return _('User defined') + ' ' + str(ln)
    main = getGenreStringMain(hn, ln, country=country)
    sub = getGenreStringSub(hn, ln)
    if main and main != sub:
        return main + ': ' + sub
    else:
        return main
