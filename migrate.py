#!/usr/bin/env python3
import datetime
import io
import json
import logging
import pathlib
import pprint
import re
import sys
import typing
import unicodedata
import urllib.error
import urllib.parse
import urllib.request


logger = logging.getLogger('migrate')
list_url = 'https://api.tumblr.com/v2/blog/{blog_id}/posts?'
tz = datetime.timezone(datetime.timedelta(hours=9), 'KST')

Post = typing.Mapping[str, typing.Any]
PostList = typing.Sequence[Post]


def fetch_posts(consumer_key: str, blog_id: str, offset: int):
    url = list_url.format(blog_id=blog_id) + urllib.parse.urlencode({
        'api_key': consumer_key,
        'offset': str(offset * 20),
        'limit': '20',
        'filter': 'raw',
    })
    with urllib.request.urlopen(url) as response:
        f = io.TextIOWrapper(response, encoding='utf-8')
        result = json.load(f)
    posts = result['response']['posts']
    assert len(posts) <= 20
    return posts


def get_posts(consumer_key: str, blog_id: str) -> typing.Iterable[Post]:
    offset = 0
    while True:
        posts = fetch_posts(consumer_key, blog_id, offset=offset)
        yield from posts
        if len(posts) < 20:
            break
        offset += 1


def width(string: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) == 'W' else 1
               for c in string)


def download_posts(consumer_key: str,
                   blog_id: str,
                   download_dir: pathlib.Path):
    l = logger.getChild('download_posts')
    posts = get_posts(consumer_key, blog_id)
    redirects = {}
    for post in posts:
        try:
            if post['state'] != 'published':
                continue
            url = post['post_url']
            l.info(url)
            if post['format'] != 'markdown':
                l.warning('Only markdown format is supported; skip...')
                continue
            published = datetime.datetime.fromtimestamp(post['timestamp']) \
                                .replace(tzinfo=datetime.timezone.utc) \
                                .astimezone(tz)
            type_ = post['type']
            slug = post.get('slug') or None
            # type: text, quote, link, answer, video, audio, photo, chat
            if type_ == 'text':
                body = post['body']
                title = post.get('title')
                if title:
                    body = '{0}\n{1}\n\n{2}'.format(
                        title, '=' * width(title), body
                    )
            elif type_ == 'quote':
                if post.get('source_url'):
                    body = '> {0}\n\n[<cite>{1}</cite>]({2})'.format(
                        post['text'].replace('\n', '\n> '),
                        post['source_title'],
                        post['source_url']
                    )
                else:
                    body = '> {0}\n\n<cite>{1}</cite>'.format(
                        post['text'].replace('\n', '\n> '),
                        post['source']
                    )
            elif type_ in ('link', 'photo'):
                if type_ == 'link':
                    caption = '[{0}][source]\n{1}'.format(
                        post['title'],
                        '=' * (width(post['title']) + 4 + 6)
                    )
                else:
                    caption = post['caption']
                if any(p.get('alt_sizes') for p in post.get('photos', [])):
                    body = '{0}\n\n{1}'.format(
                        '\n'.join(
                            '![]({0})'.format(
                                max(
                                    p['alt_sizes'],
                                    key=lambda i: i['width']
                                )['url']
                            )
                            for p in post['photos']
                        ),
                        post['caption']
                    )
                else:
                    body = caption
                if type_ == 'link':
                    body = '{0}\n\n{1}\n\n[source]: {2}\n'.format(
                        body, post['description'], post['url']
                    )
            else:
                l.warning('Post type %r is not supported; skip...', type_)
                continue
        except Exception as e:
            l.debug('post data: %s', pprint.pformat(post))
            l.exception(e)
            break
        if not body.endswith('\n'):
            body += '\n'
        if slug and not re.match(r'^[_A-Za-z0-9-]+$', slug):
            slug = None
        filename = '{0:%Y-%m-%d}-{1}.md'.format(
            published,
            slug or published.strftime('%H-%M-%S')
        )
        with (download_dir / filename).open('w') as f:
            f.write(body)
        redirects[post['id']] = {
            'published': published.isoformat(),
            'filename': filename,
            'slug': slug,
            'url': post['url'],
        }
    redirects_map_path = download_dir / 'redirects_map.json'
    with redirects_map_path.open('w') as f:
        json.dump(redirects, f,
                  indent='  ', separators=(', ', ': '), sort_keys=True)
    l.info('Redirects map file: %s', redirects_map_path)


def main():
    if len(sys.argv) < 4:
        print('usage:', sys.argv[0], 'CONSUMER_KEY', 'BLOG_ID', 'DIR',
              file=sys.stderr)
        raise SystemExit(1)
    download_dir = pathlib.Path(sys.argv[3])
    if not download_dir.exists():
        download_dir.mkdir()
    elif not download_dir.is_dir():
        print(sys.argv[0] + ':', download_dir, 'is not a directory.')
        raise SystemExit(1)
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(levelname).1s | %(message)s'
    )
    download_posts(
        consumer_key=sys.argv[1],
        blog_id=sys.argv[2],
        download_dir=download_dir
    )


if __name__ == '__main__':
    main()
