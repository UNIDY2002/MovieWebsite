from django.views import generic

from movies.models import Actor, Movie


class ActorView(generic.DetailView):
    template_name = 'actor.html'
    model = Actor

    def get_context_data(self, **kwargs):
        self.object.movies = list(self.object.movie_set.all())
        self.object.collaborators = [Actor.objects.get(pk=int(x)) for x in self.object.collaboration.split()]
        return super().get_context_data(**kwargs)


class MovieView(generic.DetailView):
    template_name = 'movie.html'
    model = Movie

    def get_context_data(self, **kwargs):
        self.object.actor_set = list(self.object.actors.all())
        self.object.plots = list(self.object.plot_set.all())
        self.object.reviews = list(self.object.review_set.all())
        return super().get_context_data(**kwargs)
