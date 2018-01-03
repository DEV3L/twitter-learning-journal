import hashlib
import json
import pickle
import time
from datetime import datetime, timedelta

import requests

pickle_dir = './data/pickle/'
json_dir = './data/json/'

repository_commits_json_file = f'{json_dir}repository_commits.json'


def _sha_url(url):
    hash_object = hashlib.sha1(url.encode())
    return hash_object.hexdigest()

    pass


def _get_url(url):
    url_sha = f'{pickle_dir}{_sha_url(url)}'

    try:
        response = pickle.load(open(url_sha, 'rb'))
    except:
        response = requests.get(url)
        pickle.dump(response, open(url_sha, 'wb'))
        time.sleep(5)

    return response


if __name__ == '__main__':
    github_user = 'DEV3L'
    repositories_url = f'https://api.github.com/users/{github_user}/repos'

    response = _get_url(repositories_url)

    repository_participations = []
    response_repositories = [repository for repository in response.json() if not repository['private']]
    for repository in response_repositories:
        participation_url = f'https://api.github.com/repos/DEV3L/{repository["name"]}/stats/participation'
        response = _get_url(participation_url)
        repository_participations.append((repository["name"], response.json()))

    repository_commits = {}

    for repository_name, repository_participation in repository_participations:
        repository_commit_history = []

        owner_commits = repository_participation['owner']

        if not sum(owner_commits) or repository_name == 'angular-starter':
            continue

        owner_commits.reverse()

        current_date = datetime.now().date() - timedelta(weeks=1)
        week_day_start = datetime.now().date()
        week_day_stop = datetime.now().date()

        year, week_num, day_of_week = current_date.isocalendar()  # DOW = day of week

        week_day_start -= timedelta(days=(day_of_week))
        week_day_stop += timedelta(days=(6 - day_of_week))

        print(year, week_num, day_of_week)

        for owner_commit in owner_commits:
            commits = {
                'start_date': str(week_day_start),
                'stop_date': str(week_day_stop),
                'count': owner_commit,
                'repository': repository_name
            }

            repository_commit_history.append(commits)

            week_day_start -= timedelta(weeks=1)
            week_day_stop -= timedelta(weeks=1)

        repository_commits[repository_name] = repository_commit_history

    with open(repository_commits_json_file, 'w') as outfile:
        json.dump(repository_commits, outfile)
