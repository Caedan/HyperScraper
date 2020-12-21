from scrapy import Selector
from urllib.parse import urlparse
import requests as req


class Website:

    def __init__(self, url: str):
        # If the last character of the url string contains /, remove it and assign to variable
        self.url = url[0:-1] if url[-1] == '/' else url
        # Download html document and save it in html_doc variable
        self.html_doc = req.get(url).content
        # Create Selector object
        self.sel = Selector(text=self.html_doc)
        # Domain property extracted from url
        self.domain = urlparse(url).netloc

    def get_hyperlinks(self) -> set:
        # Create an empty set to contain all links
        hyperlinks = set()

        # Loop through selector items
        for link in self.sel.xpath('//a/@href'):
            data = link.extract()
            # Hyperlink can by definition also include ids
            if data[0] == '/' or data[0] == '#':
                # Add link to hyperlinks set
                hyperlinks.add(self.url + data)

        return hyperlinks

    def get_external_resources(self) -> list:
        # Create an empty list to contain all resources
        resources = []

        # Loop through all tags (excluding the <a> tag) containing 'href' and 'src' attributes
        for link in self.sel.xpath('//*[not(self::a)]/@*[name()="href" or name()="src"]'):
            data = link.extract()
            # Check if link starts with 'https://'
            if data[0:8] == 'https://':
                domain = urlparse(data).netloc
                # ... and does not point to the same domain
                if domain != self.domain:
                    resources.append(data)

        return resources

    def to_json(self) -> dict:
        json_object = {
            'Hyperlinks': {},
            'External Resources': self.get_external_resources(),
            'Privacy Policy': {}
        }
        i = 1

        for link in self.get_hyperlinks():
            json_object['Hyperlinks'][i] = link
            if "privacy" in link:
                json_object['Privacy Policy']['url'] = link
            i += 1

        return json_object
