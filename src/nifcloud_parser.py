from bs4 import BeautifulSoup as soup

class NifCloudParser():

    def __init__(self, response):
        self.response = response

    def natural(self):
        self.response.text

    def xml(self):
        soup(self.response.text, "lxml-xml").prettify()
