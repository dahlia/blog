#!/usr/bin/env python3
# Hong Minhee's DIY static blog generator
# Copyright (C) 2016 Hong Minhee <http://hongminhee.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import argparse
import collections
import contextlib
import datetime
import enum
import functools
import itertools
import json
import logging
import multiprocessing
import operator
import pathlib
import re
import subprocess
import sys
import typing
import urllib.parse

from jinja2 import (Environment, FileSystemLoader, Markup, Template,
                    contextfunction)


PANDOC_OPTIONS = (
    '--from=markdown_phpextra+auto_identifiers',
    '--parse-raw', # Allow HTML fragments in Markdown
    '--smart',     # SmartyPants
    '--html-q-tags',
    '--email-obfuscation=references',
)


class Format(enum.Enum):

    html = 'html5'
    ast = 'json'


class Post:

    FILENAME_PATTERN = re.compile(
        r'^(?P<y>\d{4})-(?P<m>\d\d)-(?P<d>\d\d)-(?P<slug>[^.]+)\.(?:md|txt)$'
    )

    __slots__ = 'path', '_title', '_metadata', '_published_at'

    def __init__(self, path: pathlib.Path):
        if not path.exists():
            raise FileNotFoundError('file not exists: ' + str(path))
        self.path = path
        self._title = None
        self._metadata = None
        self._published_at = None

    def build(self, format: Format=Format.html):
        cmd = list(PANDOC_OPTIONS)
        cmd.insert(0, '--to=' + format.value) 
        cmd.append(str(self.path))
        cmd.insert(0, 'pandoc')
        output = subprocess.check_output(cmd)
        output = output.decode('utf-8')
        if format is Format.ast:
            return json.loads(output)
        return output

    @property
    def title(self) -> str:
        quotes = {
            'SingleQuote': ('\u2018', '\u2019'),
            'DoubleQuote': ('\u201c', '\u201d'),
        }

        def flatten_nodes(nodes):
            for chunk in nodes:
                if chunk['t'] == 'Space':
                    yield ' '
                elif chunk['t'] == 'Str':
                    yield chunk['c']
                elif chunk['t'] == 'Link':
                    yield from flatten_nodes(chunk['c'][1])
                elif chunk['t'] == 'Quoted':
                    quote_type = chunk['c'][0]['t']
                    yield quotes[quote_type][0]
                    yield from flatten_nodes(chunk['c'][1])
                    yield quotes[quote_type][1]
                else:
                    raise ValueError('unexpected node: ' + repr(chunk))

        if self._title is not None:
            return self._title[0]
        tree = self.build(Format.ast)
        for nodes in tree[1:]:
            for node in nodes:
                if node.get('t') == 'Header' and node['c'][0] == 1:
                    title = ''.join(flatten_nodes(node['c'][2]))
                    self._title = title,
                    return title
        self._title = None,

    @property
    def metadata(self) -> typing.Tuple[datetime.date, str]:
        if self._metadata is not None:
            return self._metadata
        m = self.FILENAME_PATTERN.match(self.path.name)
        if not m:
            raise ValueError('invalid filename: ' + self.path.name)
        published_at = datetime.date(
            year=int(m.group('y')),
            month=int(m.group('m')),
            day=int(m.group('d'))
        )
        metadata = published_at, m.group('slug')
        self._metadata = metadata
        return metadata

    @property
    def published_at(self) -> datetime.date:
        if self._published_at is not None:
            return self._published_at
        cmd = ['git', 'log', '--follow', '--format=%aI', '--reverse', '--',
               str(self.path)]
        try:
            git_log = subprocess.check_output(cmd)
        except OSError:
            git_log = None
        else:
            git_log = git_log.lstrip().decode('utf-8')
            git_log = re.match(r'^[^\n]+', git_log).group(0)
        if git_log:
            dt = datetime.datetime.strptime(git_log[:19], '%Y-%m-%dT%H:%M:%S')
            offset = datetime.timedelta(hours=int(git_log[20:22]),
                                        minutes=int(git_log[23:25]))
            tz = datetime.timezone(offset)
            published_at = dt.replace(tzinfo=tz)
        else:
            published_at = self.metadata[0]
        self._published_at = published_at
        return published_at

    @property
    def slug(self) -> str:
        return self.metadata[1]

    def resolve_object_path(
        self,
        base: pathlib.Path=pathlib.Path('.')
    ) -> pathlib.Path:
        d = self.published_at.strftime
        return base / d('%Y') / d('%m') / d('%d') / self.slug / 'index.html'

    def resolve_object_url(self, base_url: str=None) -> str:
        object_path = pathlib.PurePosixPath(self.resolve_object_path())
        if base_url is None:
            return str(object_path)  # for local filesystem
        elif not base_url.startswith(('http://', 'https://')):
            # for local file system
            object_path = pathlib.PurePosixPath(base_url) / object_path
            return str(object_path)
        # for HTTP urls
        path = '{0!s}/'.format(object_path.parent)
        return urllib.parse.urljoin(base_url, path)

    def __str__(self) -> str:
        return '{!s} -> {!s}'.format(self.path, self.resolve_object_path())

    def __repr__(self) -> str:
        title = self.title
        title = '' if title is None else ' {!r}'.format(title)
        return '<Post {!s}{}>'.format(self.path, title)


class Blog:

    def __init__(self,
                 pool: multiprocessing.Pool,
                 post_files: typing.Iterable[pathlib.Path],
                 base_url: str=None):
        self.logger = logging.getLogger('Blog')
        self.pool = pool
        self.base_url = base_url
        self.logger.info('Loading posts...')
        self.posts = list(map(Post, post_files))
        # Loading published dates
        get_published_at = operator.attrgetter('published_at')
        list(pool.imap_unordered(get_published_at, self.posts))
        # Loading titles
        list(pool.imap_unordered(operator.attrgetter('title'), self.posts))
        self.posts.sort(key=get_published_at)
        self.logger.info('Total %d posts are loaded.', len(self.posts))
        self.current_base_path = './'
        self.jinja2_env = Environment(loader=FileSystemLoader('templates'),
                                      extensions=['jinja2.ext.with_'],
                                      autoescape=True)
        self.jinja2_env.globals.update(
            blog=self,
            href_for=self.resolve_relative_url,
        )

    def resolve_relative_url(self, relative_path: str) -> str:
        if relative_path.startswith('/'):
            raise ValueError('only accept relative path')
        if self.base_url is None:
            return self.current_base_path + relative_path
        if relative_path.endswith('/index.html'):
            relative_path = relative_path.rstrip('index.html')
        return urllib.parse.urljoin(self.base_url, relative_path)

    @contextlib.contextmanager
    def base_path_context(self, base_path: str):
        prev_base_path = self.current_base_path
        self.current_base_path = base_path
        yield
        self.current_base_path = prev_base_path

    @property
    def annual_archives(self) -> typing.Mapping[int, typing.Sequence[Post]]:
        return collections.OrderedDict(
            (k, list(v))
            for k, v in itertools.groupby(
                self.posts,
                key=lambda post: post.published_at.year
            )
        )

    def build(self, build_path: pathlib.Path):
        if not build_path.is_dir():
            build_path.mkdir()
        self.build_index(build_path)
        self.build_annual_archives(build_path)
        self.build_posts(build_path)

    def build_index(self, build_path: pathlib.Path):
        logger = self.logger.getChild('build_index')
        index_tpl = self.jinja2_env.get_template('index.html')
        posts = self.posts[:-6:-1]
        if not build_path.is_dir():
            build_path.mkdir()
        stream = index_tpl.stream(posts=posts)
        index_path = build_path / 'index.html'
        with index_path.open('wb') as f:
            stream.dump(f, encoding='utf-8')
        logger.info('%s', index_path) 

    def build_annual_archives(self, build_path: pathlib.Path):
        logger = self.logger.getChild('build_annual_archives')
        archive_tpl = self.jinja2_env.get_template('archive.html')
        with self.base_path_context('../'):
            for year, posts in self.annual_archives.items():
                stream = archive_tpl.stream(year=year, posts=posts)
                archive_dir_path = build_path / str(year)
                archive_dir_path.mkdir(parents=True, exist_ok=True)
                archive_path = archive_dir_path / 'index.html'
                with archive_path.open('wb') as f:
                    stream.dump(f, encoding='utf-8')
                logger.info('%s', archive_path)

    def build_posts(self, build_path: pathlib.Path):
        logger = self.logger.getChild('build_posts')
        posts = self.pool.imap_unordered(self._build_post_body, self.posts)
        post_tpl = self.jinja2_env.get_template('post.html')
        with self.base_path_context('../../../../'):
            for post, body in posts:
                object_path = post.resolve_object_path(build_path)
                object_path.parent.mkdir(parents=True, exist_ok=True)
                stream = post_tpl.stream(post=post, post_body=body)
                with object_path.open('wb') as f:
                    stream.dump(f, encoding='utf-8')
                logger.info('%s', object_path)

    @staticmethod
    def _build_post_body(post: Post):
        return post, Markup(post.build())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base-url', metavar='URL',
                        help='the base url.  if omitted, use relative paths')
    parser.add_argument('-j', '--jobs', metavar='N',
                        type=int, default=multiprocessing.cpu_count(),
                        help='the number of parallel processes [%(default)s]')
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='debug mode')
    parser.add_argument('dest', metavar='DIR', type=pathlib.Path,
                        help='destination directory path')
    parser.add_argument('files', metavar='FILE', type=pathlib.Path, nargs='+',
                        help='post files to generate')
    args = parser.parse_args()
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(levelname).1s | %(message)s'
    )
    pool = multiprocessing.Pool(args.jobs)
    blog = Blog(pool, args.files, base_url=args.base_url)
    blog.build(args.dest)


if __name__ == '__main__':
    main()
