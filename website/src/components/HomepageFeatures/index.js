import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Expressive and flexible',
    Svg: require('@site/static/img/placeholder.svg').default,
    description: (
      <>
        Music Meta provides an abstraction to describe music metadata across
        different genres and periods, for various stakeholders and datasets. It 
        is thought to be specialised and extended.
      </>
    ),
  },
  {
    title: 'Focus on your music data',
    Svg: require('@site/static/img/placeholder.svg').default,
    description: (
      <>
        The creation of Music Knowledge Graphs from your data is streamlined by
        the pyMusicMeta library. No need to know the details of Music Meta,    
        and we also produce alignments with other ontologies.
      </>
    ),
  },
  {
    title: 'Provenance at the core',
    Svg: require('@site/static/img/placeholder.svg').default,
    description: (
      <>
        Who said that Beethoven is the composer of this piece? How was this link
        to MusicBrainz obtained? With wich confidence? Provenance is the core of
        Music Meta, and you can always include reference.  
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
