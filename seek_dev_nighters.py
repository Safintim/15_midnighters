import pytz
import requests
from itertools import count
from datetime import datetime, time


def main():
    get_midnighters()


def load_attempts():
    url = 'http://devman.org/api/challenges/solution_attempts/'
    for page in count(1):
        page_data = requests.get(url, params={'page': page}).json()
        if page >= page_data['number_of_pages']:
            break
        for attempt in page_data['records']:
            yield attempt


def get_midnighters():
    for attempt in load_attempts():
        timezone = pytz.timezone(attempt['timezone'])
        date_attempt = datetime.fromtimestamp(attempt['timestamp'], tz=timezone)
        if date_attempt.time() < time(4):
            print(date_attempt.strftime("%m/%d/%Y, %H:%M:%S"), attempt['username'])


if __name__ == '__main__':
    main()
