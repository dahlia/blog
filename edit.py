#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import cgi
import json
import logging
import sys
import urlparse

from pytumblr import TumblrRestClient


logger = logging.getLogger('edit')
base_url = 'http://blog.hongminhee.org/'

with open('index.json') as f:
    post_index = {int(post_id): path for post_id, path in json.load(f).items()}


def edit_post_to_redirect(client, blog_id, post_id, redirect_url):
    l = logger.getChild('edit_post_to_redirect')
    tpl = u'''\
<h3>홍민희 블로그가 이전됐습니다.</h3>
<p>내용은 위치만 다음 URL로 이동했을 뿐, 여전히 보존되어 있습니다.</p>
<p><a href="{url_escaped}" rel="canonical">{url_escaped}</a></p>
'''
    url = urlparse.urljoin(base_url, redirect_url)
    body = tpl.format(url=url,
                      url_escaped=cgi.escape(url, True)).encode('utf-8')
    client.edit_post(blog_id, id=post_id, type='text',
                     body=body, format='html')
    l.info('post #%d -> %s', post_id, url)


def edit_all_posts(client, blog_id, post_index):
    for post_id, url in post_index.items():
        edit_post_to_redirect(client, blog_id, post_id, url)


def main():
    if len(sys.argv) < 6:
        print('usage:', sys.argv[0], 'BLOG_ID', 'CONSUMER_KEY',
              'CONSUMER_SECRET', 'OAUTH_TOKEN', 'OAUTH_TOKEN_SECRET',
              file=sys.stderr)
        raise SystemExit(1)
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(levelname).1s | %(message)s'
    )
    edit_all_posts(
        client=TumblrRestClient(
            sys.argv[2], sys.argv[3],
            sys.argv[4], sys.argv[5]
        ),
        blog_id=sys.argv[1],
        post_index=post_index
    )


if __name__ == '__main__':
    main()
