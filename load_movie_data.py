import json

from movies.models import Actor, Movie

with open('data/movie_merged.json', encoding='utf-8') as f:
    for movie in json.load(f):
        movie_model = Movie(id=movie['id'],
                            title=movie['title'],
                            year=movie['year'],
                            actor_1=movie['actorId1'],
                            actor_2=movie['actorId2'],
                            genre=movie['genre'],
                            time=movie['time'],
                            rating=movie['rating'],
                            img=movie['img'],
                            director=movie['director'] if 'director' in movie else '',
                            screen_writer=movie['screenWriter'] if 'screenWriter' in movie else '',
                            location=movie['location'] if 'location' in movie else '',
                            company=movie['company'] if 'company' in movie else '',
                            alias=movie['alias'] if 'alias' in movie else '')
        movie_model.save()
        for actor in movie['actors']:
            try:
                movie_model.actors.add(Actor.objects.get(pk=actor))
            except Exception as e:
                print('%s Actor id is %s.' % (e, actor))
