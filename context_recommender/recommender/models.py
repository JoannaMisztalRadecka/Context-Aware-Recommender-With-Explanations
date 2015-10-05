from django.db import models


class User(models.Model):
    name = models.CharField(max_length=256, default='Anonymous')
    gender = models.IntegerField()
    age = models.PositiveIntegerField()
    country = models.CharField(max_length=256)
    city = models.CharField(max_length=256)

    def __unicode__(self):
        return u'{}, Age: {} gender: {}.'.format(self.name, self.age, self.gender)


class Movie(models.Model):
    title = models.CharField(max_length=256)
    year = models.IntegerField(default=None, null=True)
    director = models.CharField(max_length=256, null=True)
    country = models.CharField(max_length=256, null=True)
    language = models.CharField(max_length=256, null=True)
    budget = models.IntegerField(null=True)
    genre = models.CharField(max_length=256, null=True)
    imdb_url = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return u'{} ({})'.format(self.title, self.year)

#
# class Genre(models.Model):
#     name = models.CharField(max_length=256)
#     movie = models.ManyToManyField(Movie)
#


class Actor(models.Model):
    name = models.CharField(max_length=256)


class Rating(models.Model):

    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(User)

    rating = models.IntegerField()

    time = models.IntegerField()
    daytype = models.IntegerField()
    season = models.IntegerField()
    location = models.IntegerField()
    weather = models.IntegerField()
    social = models.IntegerField()
    physical = models.IntegerField()
    decision = models.IntegerField()
    interaction = models.IntegerField()

    end_emotion = models.IntegerField()
    dominant_emotion = models.IntegerField()
    mood = models.IntegerField()

    genre = models.IntegerField()

    def __unicode__(self):
        return u'Movie: {}, User: {}, Rating: {}'.format(self.movie_id, self.user_id, self.rating)





