import hashlib
import json
import pickle
import time
from datetime import datetime, timedelta

import requests

from app.twitter_learning_journal.services.logging_service import LoggingService

logger = LoggingService('github')

pickle_dir = './data/pickle/github/'
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
        logger.info(f'Cache Load: {url}')
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise Exception()
    except:
        response = requests.get(url)
        pickle.dump(response, open(url_sha, 'wb'))
        if response.status_code == 403:
            print("RATE LIMITED!!! TRY AGAIN LATER")
            return None
        logger.info(f'Retrieved/Cached: {url}')
        time.sleep(2)

    return response


if __name__ == '__main__':
    # run until all hits are cache loads or 403 github rate limit
    github_user = 'stahlscott'
    repositories_url = f'https://api.github.com/users/{github_user}/repos'

    response = _get_url(repositories_url)

    repository_participations = []
    response_repositories = [repository for repository in response.json() if not repository['private']]
    logger.info(f'Total repositories: {len(response_repositories)}')

    for repository in response_repositories:
        logger.info(repository)
        participation_url = f'https://api.github.com/repos/{github_user}/{repository["name"]}/stats/participation'
        response = _get_url(participation_url)

        if not response:
            continue

        repository_participations.append((repository["name"], response.json()))

    repository_commits = {}

    for repository_name, repository_participation in repository_participations:
        repository_commit_history = []

        try:
            owner_commits = repository_participation['owner']
        except:
            logger.warning("Cache bad: " + repository_name)
            continue

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
