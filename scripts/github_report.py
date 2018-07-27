import json
from collections import defaultdict
from datetime import datetime, timedelta

from scripts import github_commit_minute_count
from scripts.github import repository_commits_json_file
from scripts.models.aggregate_result import AggregateResult
from scripts.models.report_entry import ReportEntry


def process_github(report_start_date, report_stop_date):
    start_date = report_start_date.date()
    stop_date = report_stop_date.date()

    aggregate_result = AggregateResult('GitHub')

    with open(repository_commits_json_file, 'r') as infile:
        github_commits = json.load(infile)

    filtered_commits = []
    for repository, weekly_commits in github_commits.items():
        for weekly_commit in weekly_commits:
            if not weekly_commit['count']:
                continue

            commit_start_date = datetime.strptime(weekly_commit['start_date'], '%Y-%m-%d').date()
            commit_stop_date = datetime.strptime(weekly_commit['stop_date'], '%Y-%m-%d').date()

            if commit_start_date <= stop_date and commit_stop_date >= start_date:
                filtered_commits.append(weekly_commit)

    for weekly_commit in filtered_commits:
        number_days_week = 7
        minutes_per_hour = 60

        commits_per_day = weekly_commit['count'] / 7
        minutes = weekly_commit['count'] * github_commit_minute_count
        minutes_per_day = minutes / number_days_week
        hours_per_day = minutes_per_day / minutes_per_hour

        commit_day = datetime.strptime(weekly_commit['start_date'], '%Y-%m-%d').date()
        weekly_commit_stop_date = datetime.strptime(weekly_commit['stop_date'], '%Y-%m-%d').date()
        days_overlap = 0

        while commit_day <= weekly_commit_stop_date:
            if start_date <= commit_day <= stop_date:

                days_overlap += 1
                tweet_date_key = commit_day.isoformat()

                if tweet_date_key not in aggregate_result.timeline:
                    aggregate_result.timeline[tweet_date_key] = defaultdict(int)

                aggregate_result.timeline[tweet_date_key]['engineering'] += hours_per_day
                aggregate_result.item_count += commits_per_day
                aggregate_result.kcv += hours_per_day
            else:
                print()

            commit_day += timedelta(days=1)

        overlap = days_overlap / number_days_week

        github_report_entry = create_github_report_entry(weekly_commit, minutes_per_day, overlap)
        aggregate_result.report_entries.append(github_report_entry)

    # aggregate_result.report_entries.sort(key=lambda github_report_entry: github_report_entry.start_date, reverse=True)

    return aggregate_result


def create_github_report_entry(weekly_commit, minutes_per_day, overlap):
    report_entry = ReportEntry()

    title = weekly_commit['repository']

    report_entry.title = title
    report_entry.url = f'https://github.com/jrj92280/{title}'
    report_entry.classification = 'engineering'
    report_entry.start_date = weekly_commit['start_date']
    report_entry.stop_date = weekly_commit['stop_date']
    report_entry.length = f'{weekly_commit["count"]} commits -- {minutes_per_day:.2f} minutes/day'
    report_entry.distribution_percent = f'{overlap:.2f}'

    return report_entry
