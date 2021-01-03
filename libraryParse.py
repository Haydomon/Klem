from library import Authors
def AuthorDetailsParsed(authorName, size=None, page=None, sort=None, fields=None):
    return(Authors.AuthorSearch(authorName, size, page, sort, fields)["name"])