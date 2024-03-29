from http.client import InvalidURL
from urllib.error import URLError, HTTPError
import urllib.request
import urllib.parse
import ssl
import socket
import rule34Py

class PageGet:
    def __init__(self):
        self.url = 'https://rule34.xxx/'
        self.tag_amount = 0
        self.newposts = 0
        self.number_page = 0
        self.tag = ""
        self.hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }
        self.context = ssl._create_unverified_context()
        self.r34 = rule34Py.rule34Py()

    
    def get_url(self):
        return self.url
    
    def get_tag_amount(self):
        return self.tag_amount

    def get_newposts(self):
        return self.newposts
    
    def get_tag(self):
        return self.tag
    
    def get_number_page(self):
        return self.number_page
    
    def add_tag(self, given_tag: str) -> bool:
        """
        checks if the tag given raises an error (see error_handle())

        :return True or False depending on the outcome 
        :if True changes self.url 
        """
        querystring = "index.php?page=post&s=list&tags=" + given_tag
        verif = "{}{}".format(self.url, querystring)
        req = urllib.request.Request(verif, headers = self.hdr)
        if (self.error_handle(req, self.context)):
            self.url = verif
            self.tag = given_tag
            return True
        else:
            return False
    
    def net_check(self) -> bool:
        """
        checks if connexion to rule34 is successful

        :uses error_handle()
        :return True if success, else False (webUrl.getcode() == 200 -> success)
        """
        req = urllib.request.Request(self.url, headers = self.hdr)

        if (self.error_handle(req, self.context)):
            webUrl: urllib.request._UrlopenRet = urllib.request.urlopen(req, context = self.context)
            if (webUrl.getcode() == 200):
                return True
            else:
                return False
        return False
        
    def error_handle(self, link: urllib.request.Request, cont: ssl.SSLContext = None) -> bool:
        """
        handles error that may happen with encoding the url to a tag

        :return False if error, else True
        """
        try:
            url = urllib.request.urlopen(link)
        except InvalidURL:
            return False
        except URLError:
            return False
        except HTTPError:
            return False
        return True
    
    def page_amount(self):
        """
        determines how many pages of posts there are with the given tag

        :return None
        :changes self.number_page
        """
        numberpage =0
        while True:
            if 0 < len(self.r34.search([self.tag], page_id=numberpage, limit=42)) <= 42:
                numberpage += 100
            else:
                break
        add = 25
        numberpage -= 50
        while True:
            if len(self.r34.search([self.tag], page_id=numberpage, limit=42)) != 0 and len(self.r34.search([self.tag], page_id=numberpage + 1, limit=42)) == 0:
                self.number_page = numberpage + 1
                break
            if len(self.r34.search([self.tag], page_id=numberpage, limit=42)) != 0:
                numberpage += add
            else:
                numberpage -= add
            if add != 1:
                add = add // 2
    
    def number_post_by_tag(self):
        """
        determines the number of posts that have the given tag

        :return None
        :changes self.tag_amount
        """
        self.tag_amount = (self.number_page - 1)*42 +len(self.r34.search([self.tag], page_id=(self.number_page-1), limit = 42))
    
    def calc_new_posts(self, old_save: int, new_save: int):
            """
            determines the amount of new posts since last save

            :return None
            :changes self.newposts
            """
            self.newposts = new_save - old_save

    def is_tag_none(self) -> bool:
        """
        checks if tag exists or not

        :return True if it doesn't exist, else False
        """
        if len(self.r34.search([self.tag], page_id=0, limit=42)) == 0:
            return True
        else:
            return False