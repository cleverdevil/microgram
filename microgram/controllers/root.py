from pecan import expose, redirect, request
from pecan.hooks import PecanHook, HookController
from webob.exc import status_map
from urllib.parse import urlparse

import requests


JAVASCRIPT = '''var container = document.getElementById('microgram');

function renderImage(image) {
    var linkEl = document.createElement('a');
    linkEl.href = image['url'];
    linkEl.className = 'photo-link';
    container.appendChild(linkEl);

    var imageEl = document.createElement('div');
    imageEl.className = 'photo';
    var url = image['_microblog']['thumbnail_url'];
    imageEl.style.backgroundImage = 'url(' + url + ')';
    linkEl.appendChild(imageEl);
}

function renderNoContent() {
    var noPostsEl = document.createElement('p');
    noPostsEl.innerText = 'No recent photos.';
    container.appendChild(noPostsEl);
}

var xhr = new XMLHttpRequest();
xhr.responseType = "json";
xhr.open('GET', "https://microgram.cleverdevil.io/", true);
xhr.send();

xhr.onreadystatechange = function(e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
        container.innerHTML = '';
        if (xhr.response.length == 0) {
            renderNoContent();
        } else {
            var count = 0;
            xhr.response['items'].forEach(function(image) {
                if (count <= 200) {
                    renderImage(image);
                    count++;
                }
            });
        }
    }
}'''

CSS = '''
#microgram {
  overflow: hidden;
}
#microgram .photo-link {
  width: %(size)spx;
  height: %(size)spx;
  display: inline-block;
  margin: 10px;
}
#microgram div.photo {
  width: %(size)spx;
  height: %(size)spx;
  border-radius: 5px;
  background-size: cover;
  background-position: center;
  transition: all 200ms ease-in-out;
}
#microgram div.photo:hover {
  cursor: pointer;
  opacity: 0.75;
}
'''

class CorsHook(PecanHook):

    def after(self, state):
        state.response.headers['Access-Control-Allow-Origin'] = '*'
        state.response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        state.response.headers['Access-Control-Allow-Headers'] = 'origin, referer, authorization, accept'


class RootController(HookController):

    __hooks__ = [CorsHook()]

    @expose('json')
    def index(self, url=None):
        if url is None:
            referer = request.headers.get('Referer')
            if not referer:
                return []

            referer = urlparse(referer)
            url = '%s://%s/photos/index.json' % (
                referer.scheme,
                referer.netloc
            )

            print('Fetching ->', url)
            response = requests.get(url)
            if response.status_code == 404:
                return []
        else:
            print('Fetching ->', url)
            response = requests.get(url)

        response.encoding = 'utf-8'
        if response.headers['Content-Type'] != 'application/json':
            return dict()
        return response.json()

    @expose(content_type='application/javascript')
    def js(self):
        return JAVASCRIPT

    @expose(content_type='text/css')
    def css(self, size='200'):
        assert int(size)
        return CSS % dict(size=size)

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
