from bs4 import BeautifulSoup as soup

class NiftyCloudParser():

    def __init__(self, response):
        self.response = response

    def simple(self):
        for tag in soup(self.response.text, "html.parser").findAll(True):
            if tag.text is not '' and len(tag.contents) is 1:
                print(" : ".join([tag.name, tag.text]))
    def natural(self):
        print(self.response.text)
