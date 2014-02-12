# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import json
from flask import make_response

import urllib
import urlparse
import re

from html_parser import ProdInfoParser, JdInfoParser, YhdInfoParser

TEST_URL = r'http://www.yhd.com/ctg/s2/c33708-0/'
SCRIPT_TAG = re.compile(r'<!%.*%!>', re.IGNORECASE)


app = Flask(__name__)

@app.route('/')
def serve_unit_price():
    url = request.args.get('url', TEST_URL)
    url_parse_result = urlparse.urlparse(url)
    if 'jd.com' in url_parse_result.netloc:
        parser = JdInfoParser()
    elif 'yhd.com' in url_parse_result.netloc and '/' != url_parse_result.path:
        parser = YhdInfoParser()
    else:
        parser = ProdInfoParser()
    parser.feed(rm_script(get_content(url)))
    parser.close()
    body = parser.output()
    return (make_response(json.dumps(body)), '200', {'Content-type': 'application/json'})
    

def get_content(url):
    try:
        f = urllib.urlopen(url)
    except:
        app.logger.error("This url %s cannot be opened." % url)
    else:
        c = f.read()
    finally:
        f.close()
    return c

def rm_script(c):
    m = SCRIPT_TAG.findall(c)
    if m:
        for e in m:
            c = re.sub(SCRIPT_TAG, '', c)
    return c

if __name__ == "__main__":
    app.run(debug=True)
