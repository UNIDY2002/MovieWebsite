from django.db import models


class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    photo = models.CharField(max_length=1024)
    constellation = models.CharField(max_length=16)
    height = models.CharField(max_length=16)
    weight = models.CharField(max_length=16)
    birthday = models.CharField(max_length=16)
    birth_place = models.CharField(max_length=128)
    biography = models.CharField(max_length=8192)
    collaboration = models.CharField(max_length=256)

    def __repr__(self):
        return self.name


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    year = models.CharField(max_length=8)
    actor_1 = models.IntegerField()
    actor_2 = models.IntegerField()
    genre = models.CharField(max_length=256)
    time = models.IntegerField()
    rating = models.CharField(max_length=8)
    img = models.CharField(max_length=1024)
    director = models.CharField(max_length=128)
    screen_writer = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    company = models.CharField(max_length=1024)
    alias = models.CharField(max_length=512)
    actors = models.ManyToManyField(Actor)

    def __repr__(self):
        return self.title


class Plot(models.Model):
    content = models.CharField(max_length=16384)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __repr__(self):
        return self.movie.title


class Review(models.Model):
    content = models.CharField(max_length=16384)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __repr__(self):
        return self.movie.title
