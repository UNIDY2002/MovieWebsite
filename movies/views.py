from django.views import generic

from movies.models import Actor


class ActorView(generic.DetailView):
    template_name = 'actor.html'
    model = Actor

    def get_context_data(self, **kwargs):
        self.object.collaborators = [Actor.objects.get(pk=int(x)) for x in self.object.collaboration.split()]
        return super().get_context_data(**kwargs)
