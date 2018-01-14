import sys
import json
from datetime import date
import requests

DEATH_PLACEHOLDER = 'now'


# url = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles={}&rvprop=content&format=json'.format(title)

def get_entity_id(title):
    url_entity = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&language=en&limit=1&format=json'.format(
        title)
    res_entity = requests.get(url_entity)
    data_entity = json.loads(res_entity.text)
    return data_entity['search'][0]['id']


def get_date_of_birth(entity_id):
    url_birth = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={}&property=P569&format=json'.format(
        entity_id)
    res_birth = requests.get(url_birth)
    data_birth = json.loads(res_birth.text)
    return data_birth['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']


def get_date_of_death(entity_id):
    url_death = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={}&property=P570&format=json'.format(
        entity_id)
    res_death = requests.get(url_death)
    data_death = json.loads(res_death.text)
    if 'P570' in data_death['claims']:
        return data_death['claims']['P570'][0]['mainsnak']['datavalue']['value']['time']
    else:
        return DEATH_PLACEHOLDER


def get_existence_range(entity_id):
    url = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={}&format=json'.format(entity_id)
    res = requests.get(url)
    data = json.loads(res.text)
    date_of_birth = data['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
    if 'P570' in data['claims']:
        date_of_death = data['claims']['P570'][0]['mainsnak']['datavalue']['value']['time']
    else:
        date_of_death = DEATH_PLACEHOLDER
    return date_of_birth, date_of_death


def get_age(date_of_birth, date_of_death):
    start = int(date_of_birth[1:5])
    end = int(date_of_death[1:5]) if date_of_death != DEATH_PLACEHOLDER else date.today().year
    return end - start


def pretty_print_date(date):
    payload = date.split('-')
    if len(payload) != 3:
        return date
    return '{}/{}/{}'.format(payload[2][:2], payload[1], payload[0][1:])


def fetch_entity(title):
    title = str(title).replace(' ', '%20').replace('_', '%20')
    entity_id = get_entity_id(title)
    date_of_birth, date_of_death = get_existence_range(entity_id)
    age = get_age(date_of_birth, date_of_death)
    return '{} : {} ans ({} - {})'.format(
        title.replace('%20', ' '),
        age,
        pretty_print_date(date_of_birth),
        pretty_print_date(date_of_death))


if __name__ == '__main__':
    people = sys.argv[1:]
    for person in people:
        fetch_entity(person)
