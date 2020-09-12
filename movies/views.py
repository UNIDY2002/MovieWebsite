from time import time

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from movies.models import Actor, Movie, Review


class MovieList(generic.ListView):
    model = Movie
    paginate_by = 10
    template_name = 'movies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headerTitle'] = '电影'
        return context


class ActorList(generic.ListView):
    model = Actor
    paginate_by = 12
    template_name = 'actors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headerTitle'] = '演员'
        return context


class ActorView(generic.DetailView):
    template_name = 'actor.html'
    model = Actor

    def get_context_data(self, **kwargs):
        self.object.movies = self.object.movie_set.all()
        self.object.collaborators = []
        for x in self.object.collaboration.split():
            try:
                self.object.collaborators.append(Actor.objects.get(pk=int(x)))
            except Actor.DoesNotExist:
                pass
        context = super().get_context_data(**kwargs)
        context['headerTitle'] = '演员'
        return context


class MovieView(generic.DetailView):
    template_name = 'movie.html'
    model = Movie

    def get_context_data(self, **kwargs):
        self.object.actor_set = self.object.actors.all()
        self.object.plots = self.object.plot_set.all()
        self.object.reviews = self.object.review_set.all()
        context = super().get_context_data(**kwargs)
        context['headerTitle'] = '电影'
        return context


def shorten(src, keyword):
    threshold = 300
    if len(src) > threshold:
        begin = src.index(keyword) - 7 if keyword in src else - 1
        if begin <= 0:
            return src[0: threshold] + '...'
        else:
            return '...' + src[begin: begin + threshold] + ('...' if begin + threshold < len(src) else '')
    else:
        return src


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
        params['hasBrief'] = False
    elif category == 'actor':
        r = Actor.objects.filter(Q(name__icontains=q) | Q(movie__title__icontains=q)).distinct()
        params['results'] = [{
            'title': x.name,
            'img': x.photo,
            'href': '/actor/%s/' % x.id,
        } for x in r]
        params['hasBrief'] = False
    elif category == 'review':
        r = Review.objects.filter(content__icontains=q)
        params['results'] = [{
            'title': x.movie.title,
            'img': x.movie.img,
            'href': '/movie/%s/' % x.movie.id,
            'brief': shorten(x.content, q),
        } for x in r]
        params['hasBrief'] = True
    paginator = Paginator(params['results'], 12)
    if 'page' in request.GET:
        page = int(request.GET['page'])
        if page > paginator.num_pages:
            page = paginator.num_pages
    else:
        page = 1
    params['page_obj'] = paginator.page(page)
    params['headerTitle'] = '搜索'
    end = time()
    params['time'] = "%.6f" % (end - start)
    return render(request, 'search.html', params)
