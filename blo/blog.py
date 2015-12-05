import os
import sys
import json
import argparse
import jinja2
import codecs
import markdown
import shutil
from datetime import datetime
from collections import defaultdict

import SimpleHTTPServer
import BaseHTTPServer


PREVIEW_FIELDS = ['page_title', 'page_tags', 'page_briefing', 'page_date_time']


class ContentAggregator:
    def __init__(self):
        self.tags = defaultdict(list)
        self.content = defaultdict(dict)

    def get_content_items(self, tag=None):
        pages_list = []
        for page_url, page_vars in self.content.iteritems():
            if tag and tag not in page_vars['page_tags']:
                continue
            page_vars['page_url'] = page_url
            pages_list.append(page_vars)
        return sorted(pages_list, key=lambda x: x['page_date_time'])

    def get_tags_list(self):
        return sorted([{"page_url": "/tag/{0}.html".format(tag),
                        "page_title": tag,
                        "page_brefing": len(items)}
                       for tag, items in self.tags.iteritems()])


class BlogAction:
    def __init__(self, config):
        self.config = config
        self.jinja_env = None
        self.md = None
        self.content_aggregator = ContentAggregator()

    def serve(self):
        """ Run web-server to test static site """
        os.chdir(self.config["render_dir"])
        server_addr = ('localhost', 8000)
        request_handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = BaseHTTPServer.HTTPServer(server_addr, request_handler)
        httpd.serve_forever()

    def _generate_html(self, template_name, page_vars):
        template = self.jinja_env.get_template('{0}.html'.format(template_name))
        page_vars.update({"site_{0}".format(k): v for k, v in self.config['site'].iteritems()})
        return template.render(page_vars)

    def _generate_html_tag_list(self):
        page_vars = {
            'page_title': "List of tags",
            'page_items': self.content_aggregator.get_tags_list()
        }
        return self._generate_html('stat', page_vars)

    def _generate_html_tag(self, tag):
        page_vars = {
            'page_title': "Posts with tag '{0}'".format(tag),
            'page_items': self.content_aggregator.get_content_items(tag)
        }
        return self._generate_html('list', page_vars)

    def _generate_html_index(self):
        page_vars = {
            'page_title': self.config['site']['title'],
            'page_briefing': self.config['site']['briefing'],
            'page_items': self.content_aggregator.get_content_items()
        }
        return self._generate_html('list', page_vars)

    def _generate_html_page_and_path(self, content):
        """
        Generate html content from markdown, form a relative path of page, aggregate data for lists
        :param content: content in markdown
        :return:
        """
        # collect page variables
        page_html = self.md.convert(content)
        page_vars = {"page_{0}".format(k): v[0] for k, v in self.md.Meta.iteritems()}
        page_vars['page_content'] = page_html
        page_vars['page_date'] = page_vars['page_date_time'].split(' ')[0]
        page_vars['page_tags'] = page_vars['page_tags'].split(', ')
        page_vars['page_date_time'] = datetime.strptime(page_vars['page_date_time'], self.config['date_format'])

        # generate html page content
        html_page = self._generate_html(page_vars['page_type'], page_vars)

        # generate relative path of page
        html_page_path = self.config['draft_templates'][page_vars['page_type']]['url'].format(**page_vars)

        # collect aggregations
        if page_vars['page_type'] == 'post':
            for tag in page_vars['page_tags']:
                self.content_aggregator.tags[tag].append(html_page_path)
            self.content_aggregator.content[html_page_path] = \
                {k: v for k, v in page_vars.iteritems() if k in PREVIEW_FIELDS}

        return html_page, html_page_path

    def _create_html_file(self, html_page, html_page_path):
        file_path = os.path.join(self.config["render_dir"], html_page_path)
        html_page_dir = os.path.dirname(os.path.realpath(file_path))
        if not os.path.exists(html_page_dir):
            os.makedirs(html_page_dir)
        with codecs.open(file_path, 'w', 'utf-8') as html_file:
            html_file.write(html_page)

    def build(self):
        """ Generate finalized html. Also fill metadata for new drafts """
        
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.config['template_dir']))
        self.md = markdown.Markdown(extensions=['markdown.extensions.meta',
                                                'markdown.extensions.codehilite'])
        # render page
        for draft in os.listdir(self.config['pages_dir']):
            with open(os.path.join(self.config['pages_dir'], draft)) as f:
                content = f.read()

            html_page, html_page_path = self._generate_html_page_and_path(content)
            self._create_html_file(html_page, html_page_path)

        # render index page
        html_page = self._generate_html_index()
        self._create_html_file(html_page, 'index.html')

        # render tags lists
        for tag, page_list in self.content_aggregator.tags.iteritems():
            html_page = self._generate_html_tag(tag)
            self._create_html_file(html_page, 'tag/{0}.html'.format(tag.replace(' ','-')))
        # render tags list page
        html_page = self._generate_html_tag_list()
        self._create_html_file(html_page, 'tags.html')

    def post(self, slug, draft_type):
        """ Make a new page draft with given slug """
        now = datetime.now()
        draft_path = os.path.join(self.config['pages_dir'], 
                                  now.strftime("%Y-%m-%d__") + slug + '.md')
        date_time = now.strftime(self.config['date_format'])
        with open(draft_path, 'w') as f:
            f.write(self.config['draft_templates'][draft_type]['content']
                    .format(slug=slug, date_time=date_time))
        print("subl {0}".format(draft_path))


def create_blog(blog_dir):
    blog_path = os.path.join(os.getcwd(), blog_dir, '_blog')
    pages_path = os.path.join(blog_path, 'pages')
    os.makedirs(pages_path)

    engine_path = os.path.dirname(os.path.realpath(__file__))
    shutil.copytree(os.path.join(engine_path, 'templates'), os.path.join(blog_path, 'templates'))
    shutil.copyfile(os.path.join(engine_path, 'default.json'), os.path.join(blog_path, 'default.json'))
    print("Blog created. cd {0} && blo post hello-worlds".format(blog_dir))


def parse_args():
    """
    How to use blog:
     - build  --  generate htmls in 'render_dir'
     - serve  --  run webserver for testing in 'render_dir'
     - post "slug"  --  greate new page with given title
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='+')
    parser.add_argument('--config', default='default.json')
    parser.add_argument('--type', default='post')
    return parser.parse_args()


def main():
    opts = parse_args()
    if opts.action[0] == 'create':
        if len(opts.action) == 1:
            print("Add blog folder name")
            sys.exit(1)
        blog_dir = unicode(opts.action[1], 'utf-8')
        create_blog(blog_dir)
        sys.exit()

    config_path = os.path.join(os.getcwd(), '_blog', opts.config)
    config = json.load(open(config_path))
    blog_action = BlogAction(config)
    if opts.action[0] == 'build':
        blog_action.build()
    if opts.action[0] == 'serve':
        blog_action.serve()
    elif opts.action[0] == 'post':
        slug = unicode(opts.action[1], 'utf-8')
        blog_action.post(slug, opts.type)


if __name__ == "__main__":
    main()