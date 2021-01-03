import requests
import json
r = []

def ApiSearch(url):
    r = requests.get(url)
    r = json.loads(r.text)
    #print(r)
    return (r)
#I DONT UNDERSTAND, CONFUSION HAS HIT, THE WORLDS ENDING, WHY DIDNT I GITHUB A CLEAN VERSION!
def AddToUrl(params, url):
    size = params[0]
    page = params[1]
    sort = params[2]
    fields = params[3]
    if size:
        url = url+size
    if page:
        url = url+page
    if sort:
        url = url+sort
    if fields:
        url = url+fields
    return url

def variableAdjust(size, page, sort, fields):
    size = f"size={size}&"
    page = f"page={page}&"
    sort = f"sort={sort}&"
    fields = f"fields={fields}&"
    return(size, page, sort, fields)

class Categories():
    def __init__(self, size=None, page=None, sort=None, fields=None, categoryid=None):
        self.size = f"size={size}&"
        self.page = f"page={page}&"
        self.sort = f"sort={sort}&"
        self.fields = f"fields={fields}&"
        self.categoryid = categoryid

    def CategoryList(self):
        url = AddToUrl(self, 'https://api.spiget.org/v2/categories?')
        return ApiSearch(url)

    def CategoryDetails(self):
        url = f'https://api.spiget.org/v2/categories/{self.categoryid}'
        return ApiSearch(url)

    def CategoryResources(self):
        url = AddToUrl(self, f'https://api.spiget.org/v2/categories/{self.categoryid}/resources?')
        return ApiSearch(url)

class Authors():
    def __init__ (self, size=None, page=None, sort=None, fields=None, author=None, searchtype=""):
        self.size = f"size={size}&"
        self.page = f"page={page}&"
        self.sort = f"sort={sort}&"
        self.fields = f"fields={fields}&"
        self.author = author
        self.searchtype = searchtype

    def AuthorList (self):
        url = AddToUrl(self, 'https://api.spiget.org/v2/authors?')
        return ApiSearch(url)

    def AuthorDetails (self):
        url = f'https://api.spiget.org/v2/authors/{self.author}'
        print(ApiSearch(url))
        return ApiSearch(url)

    def AuthorResources(author, size=None, page=None, sort=None, fields=None):
        url = AddToUrl(variableAdjust(size, page, sort, fields), f'https://api.spiget.org/v2/authors/{author}/resources?')
        print(url)
        return ApiSearch(url)

    def AuthorReviews(author, size=None, page=None, sort=None, fields=None):
        url = AddToUrl(variableAdjust(size, page, sort, fields), f'https://api.spiget.org/v2/authors/{author}/reviews?')
        return ApiSearch(url)

    def AuthorSearch(searchtype, size=None, page=None, sort=None, fields=None):
        url = AddToUrl(variableAdjust(size, page, sort, fields), f'https://api.spiget.org/v2/search/authors/{searchtype}?')
        print(url)
        return ApiSearch(url)

class Resources():
    def __init__ (self, size=None, page=None, sort=None, fields=None, gameversion=None, method=None, id=None, pluginversion=None, searchfield="name", query=None):
        self.size = f"size={size}&"
        self.page = f"page={page}&"
        self.sort = f"sort={sort}&"
        self.game_version = f"{gameversion}"
        self.method = f"method={method}"
        self.fields = f"fields={fields}&"
        self.id = id
        self.pluginversion = pluginversion
        self.searchfield = searchfield
        self.query = query

    def ResourceList(self):
        """Page - Use +/- prefix for ascending/descending order. Acceptiable Values include anything in the dictonary"""
        url = AddToUrl(self, 'https://api.spiget.org/v2/resources?')
        return ApiSearch(url)

    def ResourceForVersion(self):
        """Version is required, method options include: any or all"""
        url = AddToUrl(self, f'https://api.spiget.org/v2/resources/for/{self.version}?')
        if self.method:
            url = url+self.method
        return ApiSearch(url)

    def FreeResourceList(self):
        url = AddToUrl(self, 'https://api.spiget.org/v2/resources/free?')
        return ApiSearch(url)

    def NewResources(self):
        url = AddToUrl(self, 'https://api.spiget.org/v2/resources/new?')
        return ApiSearch(url)

    def PremiumResourceList(self):
        url = AddToUrl(self, 'https://api.spiget.org/v2/resources/premium?')
        return ApiSearch(url)

    def ResourceDetails(self):
        url = f'https://api.spiget.org/v2/resources/{self.id}'
        return ApiSearch(url)

    def ResourceAuthor(self):
        url = f'https://api.spiget.org/v2/resources/{self.id}/author'
        return ApiSearch(url)

    def ResourceDownload(self):
        url = f'https://api.spiget.org/v2/resources/{self.id}/download'
        return ApiSearch(url)

    def ResourceReviews(self):
        url = AddToUrl(self, f'https://api.spiget.org/v2/resources/{self.id}/reviews?')
        return ApiSearch(url)

    def ResourceUpdates(self):
        url = AddToUrl(self, f'https://api.spiget.org/v2/resources/{self.id}/updates?')
        return ApiSearch(url)

    def LatestResourceUpdate(self):
        url = AddToUrl(self, f'https://api.spiget.org/v2/resources/{self.id}/updates/latest?')
        return ApiSearch(url)

    def ResourceVersions(resource, size=None, page=None, sort=None, fields=None):
        url = AddToUrl(variableAdjust(size, page, sort, fields), f'https://api.spiget.org/v2/resources/{resource}/versions?')
        print(url)
        return ApiSearch(url)

    def LastestResourceVersion(self):
        url = f'https://api.spiget.org/v2/resources/{self.id}/versions/latest'
        return ApiSearch(url)

    def ResourceVersion(self):
        url = f'https://api.spiget.org/v2/resources/{self.id}/versions/{self.pluginversion}'
        return ApiSearch(url)

    def ResourceVersionDownload(resourceID, version):
        url = f'https://api.spiget.org/v2/resources/{resourceID}/versions/{version}/download'
        return url

    def ResourceSearch(query, searchfield="name", size=None, page=None, sort=None, fields=None):
        url = AddToUrl(variableAdjust(size, page, sort, fields), f'https://api.spiget.org/v2/search/resources/{query}?field={searchfield}&')
        print(url)
        return ApiSearch(url)

class status():
    def ApiStatus():
        s = requests.get('https://api.spiget.org/v2/status')
        s = s.status_code
        return(s)
#Resourcecall = Resources(size = 1, gameversion = 1.16, method ="any", id=2124, pluginversion=369799, query="test", searchfield="name", page=0)
#Resourcecall.ResourceList()
#Authorcall = Authors(author="md678685")
#Authorcall.AuthorSearch()
#Categoriescall = categories(1, categoryid=15)
#Categoriescall.CategoryList()
#status.ApiStatus()