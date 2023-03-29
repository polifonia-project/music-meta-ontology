"""
Functions for aligning classes and properties of the Music Ontology and Doremus
ontology.
"""

import os
from pathlib import Path

import pandas as pd
from jellyfish import jaro_winkler_similarity as jaro

from scrape_ontologies import scrape_mo, scrape_doremus


def preprocess_ontologies() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Preprocess the ontologies by scraping them if they are not already saved as
    CSV files. Otherwise, load the CSV files.
    :return: a tuple with the Doremus and Music Ontology ontologies as pandas
    DataFrames
    :rtype: tuple[pd.DataFrame, pd.DataFrame]
    """
    if 'doremus.csv' not in os.listdir('data'):
        doremus = scrape_doremus(save=False)
    else:
        doremus = pd.read_csv('data/doremus.csv', index_col=False)

    if 'musicontology.csv' not in os.listdir('data'):
        musicontology = scrape_mo(save=False)
    else:
        musicontology = pd.read_csv('data/musicontology.csv', index_col=False)

    return doremus, musicontology


def align_parents() -> pd.DataFrame:
    """
    Align the classes of the Music Ontology and Doremus ontology based on their
    FRBR and FRBRoo parents.
    :return: a pandas DataFrame with the aligned classes and their URIs in the
    two ontologies as well as their FRBR and FRBRoo parents
    """
    doremus, musicontology = preprocess_ontologies()

    doremus_frbr = doremus[doremus['FRBRElement'].notna()]
    musicontology_frbr = musicontology[musicontology['FRBRElement'].notna()]

    parents_alignment = pd.DataFrame(columns=['DoremusClass',
                                              'MusicOntologyClass',
                                              'FRBRClass',
                                              'FRBRooClass',
                                              'DoremusURI',
                                              'MusicOntologyURI'])

    for i, row in musicontology_frbr.iterrows():
        for j, row2 in doremus_frbr.iterrows():
            if row['FRBRElement'] in row2['FRBRElement']:
                parents_alignment = parents_alignment.append({
                    'DoremusClass': row2['Name'],
                    'MusicOntologyClass': row['Name'],
                    'FRBRClass': row['FRBRElement'],
                    'FRBRooClass': row2['FRBRElement'],
                    'DoremusURI': row2['URI'],
                    'MusicOntologyURI': row['URI']
                }, ignore_index=True)

    return parents_alignment


def align_similar() -> pd.DataFrame:
    """
    Align the classes of the Music Ontology and Doremus ontology based on their
    Name similarity. The similarity is calculated using the Jaro distance and
    has to be considered as a purely syntactic similarity.
    :return: a pandas DataFrame with the aligned classes and their URIs in the
    two ontologies as well as their similarity score (Jaro distance).
    """
    doremus, musicontology = preprocess_ontologies()

    similar_alignment = pd.DataFrame(columns=['DoremusClass',
                                              'MusicOntologyClass',
                                              'Similarity',
                                              'DoremusURI',
                                              'MusicOntologyURI'])

    for i, row in musicontology.iterrows():
        for j, row2 in doremus.iterrows():
            similarity = jaro(row['Name'], row2['Name'])
            if similarity > 0.76:
                similar_alignment = similar_alignment.append({
                    'DoremusClass': row2['Name'],
                    'MusicOntologyClass': row['Name'],
                    'DoremusType': row2['Element'],
                    'MusicOntologyType': row['Element'],
                    'Similarity': similarity,
                    'DoremusURI': row2['URI'],
                    'MusicOntologyURI': row['URI']
                }, ignore_index=True)

    return similar_alignment


def align_others() -> pd.DataFrame:
    """
    Align the classes and properties of the Music Ontology and Doremus ontology
    based on their parents.
    :return: a pandas DataFrame with the aligned classes and their URIs in the
    two ontologies as well as their FRBR and FRBRoo parents
    """
    doremus, musicontology = preprocess_ontologies()

    parents_alignment = pd.DataFrame(columns=['DoremusClass',
                                              'MusicOntologyClass',
                                              'DoremusURI',
                                              'MusicOntologyURI'])

    for i, row in musicontology.iterrows():
        for j, row2 in doremus.iterrows():
            mo_parent = row['ParentClass'].split('#')[-1] if isinstance(
                row['ParentClass'], str) and 'http' in row['ParentClass'] else \
                row['ParentClass']

            similarity_a = jaro(mo_parent, row2['ParentClass']) if isinstance(
                mo_parent, str) and isinstance(row2['ParentClass'], str) else 0
            similarity_b = jaro(row['Name'], row2['ParentClass']) if isinstance(
                row['Name'], str) and isinstance(row2['ParentClass'],
                                                 str) else 0
            similarity_c = jaro(mo_parent, row2['Name']) if isinstance(
                mo_parent, str) and isinstance(row2['Name'], str) else 0

            similarity_type = 'mo_parent-doremus_parent' if similarity_a > 0.8 \
                else 'mo_parent-doremus_class' if similarity_b > 0.8 \
                else 'mo_class-doremus_parent' if similarity_c > 0.8 \
                else None

            if similarity_a > 0.76 or similarity_b > 0.76 or similarity_c > 0.76:
                parents_alignment = parents_alignment.append({
                    'DoremusClass': row2['Name'],
                    'MusicOntologyClass': row['Name'],
                    'DoremusType': row2['Element'],
                    'MusicOntologyType': row['Element'],
                    'DoremusParent': row2['ParentClass'],
                    'MusicOntologyParent': row['ParentClass'],
                    'SimilarityType': similarity_type,
                    'DoremusURI': row2['URI'],
                    'MusicOntologyURI': row['URI']
                }, ignore_index=True)

    return parents_alignment


def save_alignment(filename: str | Path, similarities=None):
    """
    Save the alignments of the Music Ontology and Doremus ontology to CSV files.
    :param filename: the name of the file to save the alignments to.
    :type filename: str or Path
    :param similarities: a list of the similarities to save. The possible
    values are 'parents', 'similar' and 'others'.
    :type similarities: list
    """
    if isinstance(filename, str):
        filename = Path(filename)

    if similarities is None:
        similarities = ['parents', 'similar', 'others']

    doremus, musicontology = preprocess_ontologies()

    with pd.ExcelWriter(filename) as writer:

        if 'parents' in similarities:
            parents_alignment = align_parents()
            parents_alignment.to_excel(writer,
                                       sheet_name='parent_similarities',
                                       index=False)

        if 'similar' in similarities:
            similar_alignment = align_similar()
            similar_alignment.to_excel(writer,
                                       sheet_name='string_similarities',
                                       index=False)

        if 'others' in similarities:
            others_alignment = align_others()
            others_alignment.to_excel(writer,
                                      sheet_name='other_similarities',
                                      index=False)

        doremus.to_excel(writer, sheet_name='doremus', index=False)
        musicontology.to_excel(writer, sheet_name='musicontology', index=False)


if __name__ == '__main__':
    save_alignment('data/alignments.xlsx',
                   similarities=['parents', 'similar'])
