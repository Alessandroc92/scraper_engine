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


def parse_html_docs(html_object: str):
    soup = BeautifulSoup(html_object, 'html.parser')
    return soup


def find_element_in_soup(soup_object: BeautifulSoup, element_name: str, element_type: str, single: str):
    finder = soup_object.find_all if not single else soup_object.find
    elements = finder(element_type=element_type)
    return [element.text for element in elements]
        