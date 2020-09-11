from time import time

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from movies.models import Actor, Movie, Review


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


def search(request):
    start = time()
    params = {}
    category = request.GET['type'] \
        if 'type' in request.GET and request.GET['type'] in ['movie', 'actor', 'review'] else 'movie'
    q = request.GET['q'] if 'q' in request.GET and request.GET['q'].strip() != '' else 'YOU WILL NEVER GET A RESULT'
    if category == 'movie':
        r = Movie.objects.filter(Q(title__icontains=q) | Q(actors__name__icontains=q)).distinct()
        params['results'] = [{
            'title': x.title,
            'img': x.img,
            'href': '/movie/%s/' % x.id,
        } for x in r]
    elif category == 'actor':
        r = Actor.objects.filter(Q(name__icontains=q) | Q(movie__title__icontains=q)).distinct()
        params['results'] = [{
            'title': x.name,
            'img': x.photo,
            'href': '/actor/%s/' % x.id,
        } for x in r]
    elif category == 'review':
        r = Review.objects.filter(content__icontains=q)
        params['results'] = [{
            'title': x.movie.title,
            'img': x.movie.img,
            'href': '/movie/%s/' % x.movie.id,
            'brief': x.content[:100] + ('' if len(x.content) <= 100 else '...'),
        } for x in r]
    paginator = Paginator(params['results'], 10)
    if 'page' in request.GET:
        page = int(request.GET['page'])
        if page > paginator.num_pages:
            page = paginator.num_pages
    else:
        page = 1
    params['results'] = paginator.page(page)
    params['page_id'] = page
    params['page_num'] = paginator.num_pages
    params['visible_pages'] = [p for p in range(page - 2, page + 6) if p in paginator.page_range]
    params['total'] = paginator.count
    params['front'] = 1 not in params['visible_pages']
    params['end'] = paginator.num_pages not in params['visible_pages']
    end = time()
    params['time'] = "%.6f" % (end - start)
    return render(request, 'search.html', params)
