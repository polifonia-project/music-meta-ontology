"""
General utils for strings, logger, system variables.
"""
import os
import re
from typing import Union, List

from rdflib import URIRef


def uri_join(*strings):
    os.path.join(*strings)


def recontextaulise_uri(uri: Union[str, URIRef], class_name: str, *context):
    """

    Parameters
    ----------
    uri : Union[str, URIRef]
        _description_
    class_name : str
        _description_

    Returns
    -------
    _type_
        _description_
    """
    uri_split = [a if a != "" else "/" for a in str(uri).split("/")]
    uri_split[-2] = "{}"  # this is expected to denote the class
    uri_template = re.sub(r"/{3,}", "//", "/".join(uri_split))
    # It is now the time to contextualise the template
    uri_infill = uri_template.format(class_name)
    # Finally, add all the string/URIs suffixes given
    for uri_context in [c for c in context if c is not None]:
        uri_suffix = [t for t in str(uri_context).split("/") if t != ""][-1] 
        uri_infill += f"_{uri_suffix}"

    return uri_infill
