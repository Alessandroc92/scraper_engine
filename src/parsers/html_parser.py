"""A module containing parsing functs for different types of inputs."""

from typing import Any

from bs4 import BeautifulSoup
from bs4.element import Tag


class HtmlParser:
    """A class that creates an HTML parser for HTML-like files."""

    def __init__(
        self,
        html_object: str,
        parser_engine: str = "html.parser",
    ) -> None:
        """The class inizializer.

        Args:
            html_object (str): The text HTML object.
            parser_engine (str, optional): An engine to parse the document.
            Defaults to "html.parser".
        """
        self.html_object = html_object
        self.parser_engine = parser_engine
        self._soup_object: BeautifulSoup | None = None

    def _get_soup(self) -> BeautifulSoup:
        """A method that saves and HTML string into a parsed bs4 object."""
        if self._soup_object is None:
            self._soup_object = BeautifulSoup(self.html_object, self.parser_engine)
        return self._soup_object
    
    def prettify_response(self):
        return self._get_soup().prettify()

    def select_elements(self, css_selector: str, **kwargs: Any) -> list[Tag]:
        """A method that returns html elements via a CSS selector.

        Args:
            css_selector (str): A CSS selector for an HTML file.
            **kwargs: Optional parameters for the bs4.select method.

        Returns:
            list[Tag | None]: Bs4 Tag elements from the html file.
        """
        elements: list[Tag] = self._get_soup().select(css_selector, **kwargs)
        return elements

    def select_attr(self, css_selector: str, attr: str, **kwargs: Any) -> list[str]:
        """A method that returns the attribute of HTML elements.

        Args:
            css_selector (str): A CSS selector for an html file.
            attr (str): The name of the attribute to be returned.
            **kwargs: Optional parameters for the bs4.select method.

        Returns:
            list[str | None]: The element attributes in string format.
        """
        elements = self.select_elements(css_selector=css_selector, **kwargs)
        return [element.get(attr) for element in elements if element.get(attr) is not None]

    def select_text(self, css_selector: str, **kwargs: Any) -> list[str]:
        """A method that returns the text from an HTML element.

        Args:
            css_selector (str): A CSS selector for an html file.
            **kwargs: Optional parameters for the bs4.select method.

        Returns:
            list[str | None]: The text from each element found.
        """
        elements = self.select_elements(css_selector=css_selector, **kwargs)
        return [element.get_text(strip=True) for element in elements]
