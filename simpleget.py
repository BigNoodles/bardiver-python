#!/usr/bin/env python3

#imports
from requests import get
from contextlib import closing


def simple_get(url):
    """
    Makes a get request to 'url'
    If response is valid HTML, returns page text; otherwise None.
    """

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except Exception as e:
        print(f'Error getting response from {url}: {e}')
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be valid HTML
    """

    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


