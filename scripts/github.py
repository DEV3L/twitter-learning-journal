import hashlib
import json
import pickle
import time

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
    repositories_url = 'https://api.github.com/users/DEV3L/repos'
    response = _get_url(repositories_url)

    repository_participations = []
    response_repositories = [repository for repository in response.json() if not repository['private']]
    for repository in response_repositories:
        participation_url = f'https://api.github.com/repos/DEV3L/{repository["name"]}/stats/participation'
        response = _get_url(participation_url)
        repository_participations.append((repository["name"], response.json()))

    repository_commits = {}

    for repository_name, repository_participation in repository_participations:
        repository_commit_history = {}

        owner_commits = repository_participation['owner']
        owner_commits.reverse()

        for week_index, count in enumerate(owner_commits):
            pass

        start_date = None
        stop_date = None
        print(repository_name, repository_participation)

        repository_commit_history['start_date'] = None
        repository_commit_history['stop_date'] = None
        repository_commit_history['_data'] = owner_commits

        repository_commits[repository_name] = repository_commit_history

    with open(repository_commits_json_file, 'w') as outfile:
        json.dump(repository_commits, outfile)

    print()
