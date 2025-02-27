import pytz
import requests
from itertools import count
from datetime import datetime, time


def main():
    try:
        attempts = list(load_attempts())
        print_midnighters(get_midnighters(attempts))
    except requests.exceptions.RequestException as e:
        exit(e)


def print_midnighters(midnighters):
    for midnighter in midnighters:
        print(midnighter)


def get_midnighters(attempts):
    midnighters = set()
    start_morning = 4
    for attempt in attempts:
        timezone = pytz.timezone(attempt['timezone'])
        date_attempt = datetime.fromtimestamp(attempt['timestamp'], tz=timezone)
        if date_attempt.time() < time(start_morning):
            midnighters.add(attempt['username'])
    return midnighters


def load_attempts():
    url = 'http://devman.org/api/challenges/solution_attempts/'
    for page in count(start=1):
        response = requests.get(url, params={'page': page})
        response.raise_for_status()
        page_data = response.json()
        yield from page_data['records']
        if page >= page_data['number_of_pages']:
            break


if __name__ == '__main__':
    main()
