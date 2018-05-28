import os
import json
from operator import itemgetter
import datetime
import time 

import requests
import humanize
import emoji


def get_projects(user, year=2010, min_stars=3):
    all_projects = []
    if not os.path.isfile('projects_{}_{}.json'.format(user, year)):
        for y in range(year, datetime.datetime.now().year+1):
            url = "https://api.github.com/search/repositories?q=user:{}+created:{}".format(user, y)
            print(url)
            r = requests.get(url)
            time.sleep(5)
            try:
                all_projects += r.json()['items']
            except:
                print(r.json())
                pass
        with open('projects_{}_{}.json'.format(user, year), 'w') as f:
            f.write(json.dumps(all_projects))
    data = json.load(open('projects_{}_{}.json'.format(user, year), 'r'))
    projects = sorted(data, key=itemgetter(
        'stargazers_count'), reverse=True)

    s = """
[{p[name]}]({p[html_url]}) <small>({stars} stars)</small>
: {p[description]}
"""

    project_text = ""
    for project in projects:
        if project['fork'] or project['stargazers_count'] < min_stars or project['description'] == None:
            continue

        project['description'] = emoji.emojize(project['description']).strip()
        if project['description'][-1] != '.':
            project['description'] += '.'
        project_text += (s.format(p=project,
                                  stars=humanize.intcomma(project['stargazers_count'])))
    return project_text

# Get new projects
with open('new_projects.txt', 'w') as f:
    f.write(get_projects("schollz", year=2017))

# Get all projects
with open('all_projects.txt', 'w') as f:
    f.write(get_projects("schollz"))
