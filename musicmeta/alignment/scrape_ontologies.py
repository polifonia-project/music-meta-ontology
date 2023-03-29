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
    df = pd.DataFrame(items).T
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
                       'skos:scopeNote': 'ScopeNote',
                       },
              inplace=True)
    df.to_csv(filename, index=True, index_label='Name')


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

        # add value if FRBR parent class
        if 'ParentClass' in attributes and 'frbr' in attributes['ParentClass']:
            print(attributes['ParentClass'].split('#')[-1])
            attributes['FRBRElement'] = attributes['ParentClass'].split('#')[-1]

        items[name] = {
            'element': element,
            'description': description
        }
        items[name].update(attributes)

    # save if the save parameter is True
    if save:
        save_csv(items, 'musicontology.csv')

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
    cp = classes.find_all('li') + properties.find_all('li')
    cp = filter(lambda x: x.find('h2') is not None, cp)

    for c in cp:
        name = c.find('h2')
        name = name.find('span').text

        uri = c.find('small').text
        element = 'class' if name[0] == 'M' else 'property'
        features = c.find_all('ul', class_='features')
        attributes = {}
        for e in features:
            try:
                for f in e.find_all('li'):
                    key = f.find_all('div', class_='prop')[0].text
                    value = f.find_all('div', class_='obj')[0].text
                    attributes[key] = value
            except IndexError:
                pass

        # add FRBRoo parent class
        if 'rdfs:subClassOf' in attributes and 'frbr' in attributes[
            'rdfs:subClassOf']:
            attributes['FRBRElement'] = \
            attributes['rdfs:subClassOf'].split(':')[-1]

        # add C-CRM parent class
        if 'rdfs:subClassOf' in attributes and 'crm' in attributes[
            'rdfs:subClassOf']:
            attributes['CCRMElement'] = \
            attributes['rdfs:subClassOf'].split(':')[-1]

        items[name] = {
            'element': element,
            'uri': uri
        }
        items[name].update(attributes)

    # save if the save parameter is True
    if save:
        save_csv(items, 'doremus.csv')

    return items


if __name__ == '__main__':
    mo = scrape_mo()
    doremus = scrape_doremus()
