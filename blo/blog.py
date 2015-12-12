import os
import sys
import json
import argparse
import shutil
from datetime import datetime
import logging

import SimpleHTTPServer
import BaseHTTPServer

from page_generator import PageGenerator


log = logging.getLogger(__name__)


class BlogAction:
    def __init__(self, config):
        self.config = config

    def serve(self):
        """ Run web-server to test static site """
        os.chdir(self.config["render_dir"])
        server_addr = ('localhost', 8000)
        request_handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = BaseHTTPServer.HTTPServer(server_addr, request_handler)
        log.info("Serving at http://{0}:{1}".format(*server_addr))
        httpd.serve_forever()

    def build(self):
        """ Generate finalized html. Also fill metadata for new drafts """
        page_generator = PageGenerator(self.config)
        page_generator.generate_all()

    def post(self, slug, draft_type):
        """ Make a new page draft with given slug """
        now = datetime.now()
        draft_path = os.path.join(self.config['pages_dir'], 
                                  now.strftime("%Y-%m-%d__") + slug + '.md')
        date_time = now.strftime(self.config['date_format'])
        with open(draft_path, 'w') as f:
            f.write(self.config['draft_templates'][draft_type]['content']
                    .format(slug=slug, date_time=date_time))
        log.info(draft_path)


def create_blog(blog_dir):
    blog_path = os.path.join(os.getcwd(), blog_dir, '_blog')
    pages_path = os.path.join(blog_path, 'pages')
    os.makedirs(pages_path)

    engine_path = os.path.dirname(os.path.realpath(__file__))
    shutil.copytree(os.path.join(engine_path, 'templates'), os.path.join(blog_path, 'templates'))
    shutil.copyfile(
        os.path.join(engine_path, 'default.json'),
         os.path.join(blog_path, 'default.json'))
    shutil.copyfile(
        os.path.join(engine_path, 'draft_templates.json'),
        os.path.join(blog_path, 'draft_templates.json'))
    log.info("Blog created. \ncd {0} && blo post hello-worlds".format(blog_dir))


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
            log.info("Add blog folder name")
            return 1
        blog_dir = unicode(opts.action[1], 'utf-8')
        create_blog(blog_dir)
        return 0

    config_path = os.path.join(os.getcwd(), '_blog', opts.config)
    config = json.load(open(config_path))
    draft_templates_path = os.path.join(os.getcwd(), '_blog', 'draft_templates.json')
    config['draft_templates'] = json.load(open(draft_templates_path))

    blog_action = BlogAction(config)
    if opts.action[0] == 'build':
        blog_action.build()
    if opts.action[0] == 'serve':
        blog_action.serve()
    elif opts.action[0] == 'post':
        slug = unicode(opts.action[1], 'utf-8')
        blog_action.post(slug, opts.type)


if __name__ == "__main__":
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.DEBUG)
    sys.exit(main())