import random
from urllib import parse

PATH_DICT = {
    '10.47.123.123:8092': 'hcq',
    '10.47.132.123:8082': 'hcq2'
}

def created_url(url, netloc_list):
    o = parse.urlparse(url)
    netloc = '{0}/{1}'.format(random.choice(netloc_list), PATH_DICT.get(o.netloc, ''))
    return parse.urlunparse((o.scheme, netloc, o.path, o.params, o.query, o.fragment))
