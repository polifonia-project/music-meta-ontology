"""
URI Factories are responsible for minting or retrieving URIs given various
formats as input.
"""
from pathlib import Path
from typing import List
from utils import uri_join


class URIFactory:

    def __init__(self, base_uri:str) -> None:
        """
        Creates and initialises a factory from a base URI. The creation of each
        URI varies on the specific factory extending this interface.
        """
        if base_uri[-1] != "/":
            base_uri += "/"
        self.base_uri = base_uri

    def mint_from_strings(self,  *strings):
        raise NotImplementedError()

    def mint_from_file(self, str: Path):
        raise NotImplementedError()


class BseConcatenationURIFactory(URIFactory):

    def mint_from_strings(self, class_name: str, *strings):
        return self.base_uri + "/".join([class_name] + strings)

    def mint_from_file(self, str: Path):
        # TODO Hashing the file and concatenating
        return None




