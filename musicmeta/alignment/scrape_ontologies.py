"""
Scrape utilities for aggregating data from existing ontologies in the music
domain.
At the moment, the following ontologies are scraped:
- Music Ontology
- Doremus Ontology

The scraper returns a dictionary with the classes, properties and instances of
the ontology. The dictionary can be saved as a CSV file.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

MUSIC_ONTOLOGY_URL = 'http://musicontology.com/specification/'
DOREMUS_URL = 'http://data.doremus.org/ontology#'


def save_csv(items: dict, filename: str):
    """
    Save the dictionary as a CSV file.
    :param items: the dictionary to save
    :param filename: the name of the file
    """
    df = pd.DataFrame(items, index=None).T
    df.rename(columns={'element': 'Element',
                       'rdfs:comment': 'Description',
                       'uri': 'URI',
                       'rdfs:label': 'Label',
                       'rdfs:subClassOf': 'ParentClass',
                       'rdfs:subPropertyOf': 'ParentProperty',
                       'rdfs:domain': 'Domain',
                       'rdfs:range': 'Range',
                       'owl:equivalentClass': 'EquivalentClass',
                       'owl:equivalentProperty': 'EquivalentProperty',
                       'owl:inverseOf': 'InverseOf',
                       'owl:disjointWith': 'DisjointWith',
                       'owl:unionOf': 'UnionOf',
                       },
              inplace=True)
    df.to_csv(filename)


def scrape_mo(save: bool = True) -> dict:
    """
    Scraper for the Music Ontology. It returns a dictionary with the classes,
    properties and instances of the ontology.
    :param save: if True, save the dictionary as a CSV file
    :type save: bool
    :return: a dictionary with the classes, properties and instances of the
    ontology
    :rtype: dict
    """
    items = {}

    # Get the HTML page
    page = requests.get(MUSIC_ONTOLOGY_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    for c in soup.find_all('section'):
        name = c.find('h3').text
        element = 'class' if name[0].isupper() else 'property'
        description = c.find('p').text.strip().replace('\n', ' ')
        attributes = {}
        for row in c.find_all('tr'):
            type = row.find('th').text.strip(':').replace(' ', '')
            value = row.find('td').text
            if type == 'Type':
                element = 'individual'
            else:
                attributes[type] = value
        items[name] = {
            'element': element,
            'description': description
        }
        items[name].update(attributes)

        # add value if FRBR parent class
        if 'ParentClass' in attributes and 'frbr' in attributes['ParentClass']:
            attributes['FRBRElement'] = attributes['ParentClass'].split('#')[-1]

    # save if the save parameter is True
    if save:
        save_csv(items, './data/musicontology.csv')

    return items


def scrape_doremus(save: bool = True) -> dict:
    """
    Scraper for the Doremus ontology. It returns a dictionary with the classes,
    properties and instances of the ontology.
    :param save: define if the dictionary should be saved as a CSV file or not
    :type save: bool
    :return: a dictionary with the classes, properties and instances of the
    ontology
    :rtype: dict
    """
    items = {}

    # Get the HTML page
    page = requests.get(DOREMUS_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    classes = soup.find('section', class_='classes card')
    properties = soup.find('section', class_='properties card')

    for c in (classes.find_all('li') + properties.find_all('li')):
        name = c.find('span').text
        uri = c.find('small').text
        element = 'class' if name[0] == 'M' else 'property'
        features = c.find_all('ul', class_='features')
        for e in features:
            try:
                for f in e.find_all('li'):
                    key = f.find_all('div', class_='prop')[0].text
                    value = f.find_all('div', class_='obj')[0].text
                    items[name] = {
                        'element': element,
                        'uri': uri,
                        key: value
                    }
            except IndexError:
                pass

    # save if the save parameter is True
    if save:
        save_csv(items, './data/doremus.csv')

    return items


if __name__ == '__main__':
    # mo = scrape_mo()
    doremus = scrape_doremus()
    # print(doremus)
