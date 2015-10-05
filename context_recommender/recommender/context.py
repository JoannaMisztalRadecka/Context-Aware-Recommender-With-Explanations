from abc import abstractmethod


class Context(object):
    context = ''
    names = {}

    def __init__(self, context):
        self.value = context
        self.name = self.names[context]

    def get_description(self):
        return 'it is {}'.format(self.name)


class NoContext(Context):
    NO_CONTEXT = 1

    names = {NO_CONTEXT: 'no context'}
    def __init__(self):
        super(NoContext, self).__init__(self.NO_CONTEXT)

    def get_description(self):
        return 'it is something in your taste'


class Gender(Context):
    context = 'gender'

    MALE = 1
    FEMALE = 2

    names = {MALE: 'man',
             FEMALE: 'woman'}



class Time(Context):
    context = 'time'

    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    NIGHT = 4

    names = {MORNING:'morning',
             AFTERNOON: 'afternoon',
             EVENING: 'evening',
             NIGHT: 'night'}



class DayType(Context):
    context = 'daytype'

    WORKING_DAY = 1
    WEEKEND = 2
    HOLIDAY = 3

    names = {WORKING_DAY: 'working day',
             WEEKEND: 'weekend',
             HOLIDAY: 'holiday'}


class Season(Context):
    context = 'season'

    SPRING = 1
    SUMMER = 2
    AUTUMN = 3
    WINTER = 4

    names = {
        SPRING: 'spring',
        SUMMER: 'summer',
        AUTUMN: 'autumn',
        WINTER: 'winter'
    }


class Location(Context):
    context = 'location'

    HOME = 1
    PUBLIC = 2
    FRIEND = 3

    names = {
        FRIEND: 'friend',
        PUBLIC: 'public',
        HOME: 'home'
    }

    def get_description(self):
        return 'you watch it at {}'.format(self.name)


class Weather(Context):
    context = 'weather'

    SUNNY = 1
    RAINY = 2
    STORMY = 3
    SNOWY = 4
    CLOUDY = 5

    names = {
        SUNNY: 'sunny',
        RAINY: 'rainy',
        STORMY: 'stormy',
        SNOWY: 'snowy',
        CLOUDY: 'cloudy'
    }

    def get_description(self):
        return 'it is a {} day today'.format(self.name)


class Social(Context):
    context = 'social'
    ALONE = 1
    MY_PARTNER = 2
    FRIENDS = 3
    COLLEAGUES = 4
    PARENTS = 5
    PUBLIC = 6
    FAMILY = 7

    names = {
        ALONE: 'alone',
        MY_PARTNER: 'with partner',
        FRIENDS: 'with friends',
        COLLEAGUES: 'with colleagues',
        PARENTS: 'with parents',
        PUBLIC: 'in public',
        FAMILY: 'with family'
    }

    def get_description(self):
        return 'you will watch it {}'.format(self.name)

class Emotion(object):

    SAD = 1
    HAPPY = 2
    SCARED = 3
    SURPRISED = 4
    ANGRY = 5
    DISGUSTED = 6
    NEUTRAL = 7

    names = {
        SAD: 'sad',
        HAPPY: 'happy',
        SCARED: 'scared',
        SURPRISED: 'surprised',
        ANGRY: 'angry',
        DISGUSTED: 'disgusted',
        NEUTRAL: 'neutral'
    }


class Mood(object):
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3

    names = {
        POSITIVE: 'positive',
        NEUTRAL: 'neutral',
        NEGATIVE: 'negative'
    }


class Physical(object):
    HEALTHY = 1
    ILL = 2


class Decision(object):
    DECIDED = 1
    GIVEN = 2


class Genre(object):
    ACTION = 1
    ADULT = 2
    ADVENTURE = 3
    ANIMATION = 4
    ART = 5
    BIOGRAPHY = 6
    COMEDY = 7
    CRIME = 8
    DOCUMENTARY = 9
    DRAMA = 10
    FAMILY = 11
    FANTASY = 12
    HISTORY = 13
    HORROR = 14
    MUSIC = 15
    MUSICAL = 16
    MYSTERY = 17
    ROMANCE = 18
    SCI_FICTION = 19
    SPORT = 20
    THRILLER = 21

    names = {ACTION: 'action movie',
             ADULT: 'movie for adults',
             ADVENTURE: 'adventure movie',
             ANIMATION: 'animated movie',
             ART: 'movie about arts',
             BIOGRAPHY: 'biography',
             COMEDY: 'comedy',
             CRIME: 'crime movie',
             DOCUMENTARY: 'documentary',
             DRAMA: 'drama',
             FAMILY: 'family movie',
             FANTASY: 'fantasy',
             HISTORY: 'historical movie',
             HORROR: 'horror',
             MUSIC: 'movie about musics',
             MUSICAL: 'musical',
             MYSTERY: 'mystery movie',
             ROMANCE: 'romance',
             SCI_FICTION: 'science fiction movie',
             SPORT: 'movie about sports',
             THRILLER: 'thriller'
             }
