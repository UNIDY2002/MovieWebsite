import json

from movies.models import Actor

with open('data/actor_merged.json', encoding='utf-8') as f:
    for actor in json.load(f):
        Actor.objects.create(id=actor['id'],
                             name=actor['name'],
                             photo=actor['photo'],
                             constellation=actor['constellation'],
                             height=actor['height'],
                             weight=actor['weight'],
                             birthday=actor['birthday'],
                             birth_place=actor['birth_place'],
                             biography=actor['biography'],
                             collaboration=' '.join(str(x) for x in actor['collaborators']))
