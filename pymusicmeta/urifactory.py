"""

"""
from pathlib import Path
from typing import List

class URIFactory:

    def __init__(self, source_uri:str) -> None:
        self.source_uri = source_uri

    def mint_from_strings(self,  strings: list[str]):
        raise NotImplementedError()

    def mint_from_file(self, str: Path):
        raise NotImplementedError()
    

class SimpleConcatenationURIFactory(URIFactory):

    def mint_from_strings(self, class_name: str, strings: List[str]):
        return self.source_uri + class_name + "/_".join(strings)
    


