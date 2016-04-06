#!/usr/bin/env python3
"""Redirect old blog.dahlia.kr urls to new blog.hongminhee.org urls."""
import os
import pathlib

from flask import Flask, Response, json, make_response
from werkzeug.exceptions import NotFound
from werkzeug.urls import url_join
from werkzeug.utils import escape
from waitress import serve


base_url = 'http://blog.hongminhee.org/'
app = Flask(__name__)


def redirect(url: str) -> Response:
    tpl = '''\
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>홍민희 블로그가 이전됐습니다.</title>
    <meta http-equiv="refresh" content="0; url={url_escaped}">
  </head>
  <body>
    <h1>홍민희 블로그가 이전됐습니다.</h1>
    <p>내용은 위치만 다음 URL로 이동했을 뿐, 여전히 보존되어 있습니다.</p>
    <p><a href="{url_escaped}" rel="canonical">{url_escaped}</a></p>
  </body>
</html>
'''
    url = url_join(base_url, url)
    html = tpl.format(url=url, url_escaped=escape(url))
    return make_response(html, 301, {'Location': url})


@app.route('/')
@app.route('/archive')
@app.route('/archive/')
@app.route('/page')
@app.route('/page/')
@app.route('/page/<int:page>')
@app.route('/page/<int:page>/')
def index(page: int=0):
    # page is ignored
    return redirect('.')


@app.route('/archive/<int:year>')
@app.route('/archive/<int:year>/')
@app.route('/archive/<int:year>/<int:month>')
@app.route('/archive/<int:year>/<int:month>/')
def annual_archive(year: int, month: int=0):
    # month is ignored
    return redirect('{0:4d}/'.format(year))


@app.route('/rss')
@app.route('/rss.xml')
@app.route('/rss/')
def feed():
    return redirect('feed.xml')


with (pathlib.Path(__file__).parent / 'index.json').open() as f:
    post_index = {int(post_id): path for post_id, path in json.load(f).items()}


@app.route('/<int:post_id>')
@app.route('/<int:post_id>/')
@app.route('/<int:post_id>/<slug>')
@app.route('/<int:post_id>/<slug>/')
@app.route('/post/<int:post_id>')
@app.route('/post/<int:post_id>/')
@app.route('/post/<int:post_id>/<slug>')
@app.route('/post/<int:post_id>/<slug>/')
def post(post_id: int, slug: str=''):
    # slug is ignored
    try:
        url = post_index[post_id]
    except KeyError:
        raise NotFound()
    return redirect(url)


def main():
    port = int(os.environ.get('PORT', 5000))
    serve(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
