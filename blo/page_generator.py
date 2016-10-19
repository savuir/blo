"""
Module for html page generation using drafts.
"""
import codecs
import os
from datetime import datetime

import jinja2
import markdown
import PyRSS2Gen

from content_aggregator import ContentAggregator


def split_into_pages(items, per_page):
    return [items[i:i + per_page] for i in range(0, len(items), per_page)]


class PageGenerator:
    def __init__(self, config):
        self.config = config
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.config['template_dir']))
        self.md = markdown.Markdown(
            extensions=['markdown.extensions.meta',
                        'markdown.extensions.codehilite'])
        self.content_aggregator = ContentAggregator(config)

    def _generate_html(self, template_name, page_vars):
        template = self.jinja_env.get_template('{0}.html'.format(template_name))
        page_vars.update({"site_{0}".format(k): v
                          for k, v in self.config['site'].iteritems()})
        return template.render(page_vars)

    def _generate_xml_rss(self):
        posts = []
        for link, content in self.content_aggregator.get_latest_posts().iteritems():
            link = "{0}/{1}".format(self.config['site']['url'], link)
            posts.append(
                PyRSS2Gen.RSSItem(
                title=content['page_title'],
                link=link,
                description=content['page_briefing'],
                guid=PyRSS2Gen.Guid(link),
                pubDate=content['page_date_time'])
            )
        return PyRSS2Gen.RSS2(
            title=self.config['site']['title'],
            link=self.config['site']['url'],
            description=self.config['site']['briefing'],
            lastBuildDate=datetime.now(),
            items=posts
        )

    def _generate_html_tag_list(self):
        page_vars = {
            'page_title': "List of tags",
            'page_items': self.content_aggregator.get_tags_list()
        }
        return self._generate_html('stat', page_vars)

    def _generate_html_tag_pages(self, tag):
        items = self.content_aggregator.get_content_items(tag)
        pages = split_into_pages(items, self.config['items_per_page'])
        items_pages = []
        for page_number, item_set in enumerate(pages):
            page_vars = {
                'page_title': "Posts with tag '{0}'".format(tag),
                'tag': tag,
                'page_items': item_set,
                'page_number': page_number,
                'total_pages': len(pages)
            }
            items_pages.append(self._generate_html('list', page_vars))
        return items_pages

    def _generate_html_index(self):
        items = self.content_aggregator.get_content_items()
        pages = split_into_pages(items, self.config['items_per_page'])
        items_pages = []
        for page_number, item_set in enumerate(pages):
            page_vars = {
                'page_title': self.config['site']['title'],
                'page_briefing': self.config['site']['briefing'],
                'page_items': item_set,
                'page_number': page_number,
                'total_pages': len(pages)
            }
            items_pages.append(self._generate_html('list', page_vars))
        return items_pages

    def _generate_html_page_and_path(self, content):
        """
        Generate html content from markdown, form a relative path of page, aggregate data for lists
        :param content: content in markdown
        :return:
        """
        # collect page variables
        page_html = self.md.convert(content.decode('utf-8'))
        page_vars = {"page_{0}".format(k): v[0] for k, v in self.md.Meta.iteritems()}
        page_vars['page_content'] = page_html
        page_vars['page_author'] = self.config['site']['author']
        page_vars['page_date'] = page_vars.get('page_date_time', '').split(' ')[0]
        page_vars['page_tags'] = [tag for tag in page_vars['page_tags'].split(', ') if tag]
        if 'page_date_time' in page_vars:
            page_vars['page_date_time'] = \
                datetime.strptime(page_vars['page_date_time'],
                                  self.config['date_format'])
        page_type = page_vars.get('page_type', 'post')

        # generate relative path of page
        html_page_path = self.config['draft_templates'][page_type]['url'].format(**page_vars)
        page_vars['page_url'] = html_page_path

        # generate html page content
        html_page = self._generate_html(page_type, page_vars)

        # collect aggregations
        if page_vars['page_type'] == 'post':
            for tag in page_vars['page_tags']:
                self.content_aggregator.tags[tag].append(html_page_path)
            self.content_aggregator.content[html_page_path] = page_vars

        return html_page, html_page_path

    def _create_html_file(self, html_page, html_page_path):
        file_path = os.path.join(self.config["render_dir"], html_page_path)
        html_page_dir = os.path.dirname(os.path.realpath(file_path))
        if not os.path.exists(html_page_dir):
            os.makedirs(html_page_dir)
        with codecs.open(file_path, 'w', 'utf-8') as html_file:
            html_file.write(html_page)

    def _create_rss_file(self, rss_page, rss_file_path):
        file_path = os.path.join(self.config["render_dir"], rss_file_path)
        html_page_dir = os.path.dirname(os.path.realpath(file_path))
        if not os.path.exists(html_page_dir):
            os.makedirs(html_page_dir)
        with open(file_path, 'w') as rss_file:
            rss_page.write_xml(rss_file, encoding='utf-8')

    def generate_all(self):
        """
        index.html - main page (first page for all posts)
        page{page_number}.html  pages for all posts
        tags.html - list of tags
        tag/{tag_name}.html - first page for items of tag
        tag/{tag_name}/page{page_number}.html - pages for items of tag
        """
        # render page
        for draft in os.listdir(self.config['pages_dir']):
            with open(os.path.join(self.config['pages_dir'], draft)) as f:
                content = f.read()

            html_page, html_page_path = self._generate_html_page_and_path(content)
            self._create_html_file(html_page, html_page_path)

        # render index page
        html_pages = self._generate_html_index()
        for page_number, html_page in enumerate(html_pages):
            self._create_html_file(
                html_page, 'page{0}.html'.format(page_number))
        # shortcut for the first page
        self._create_html_file(html_pages[0], 'index.html')

        # render tags lists
        for tag, page_list in self.content_aggregator.tags.iteritems():
            html_pages = self._generate_html_tag_pages(tag)
            for page_number, html_page in enumerate(html_pages):
                self._create_html_file(html_page,
                    'tag/{0}/page{1}.html'.format(
                        tag.replace(' ', '-'), page_number))
            # shortcut for the first page
            self._create_html_file(html_pages[0],
                'tag/{0}.html'.format(tag.replace(' ', '-')))

        # render tags list page
        html_page = self._generate_html_tag_list()
        self._create_html_file(html_page, 'tags.html')

        # render rss
        xml_page = self._generate_xml_rss()
        self._create_rss_file(xml_page, 'rss.xml')