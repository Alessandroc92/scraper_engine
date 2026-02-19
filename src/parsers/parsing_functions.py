"""A module containing parsing functs for different types of inputs"""
import extruct
from bs4 import BeautifulSoup


def json_ld_parser(html_object: str) -> list:
    """Parsing JSON Linked Data from HTML string object

    Args:
        html_object (str): An html string object.

    Returns:
        list: A list of all the elements in the JSON Linked data
    """
    jslde = extruct.jsonld.JsonLdExtractor()
    data = jslde.extract(html_object)
    return data
