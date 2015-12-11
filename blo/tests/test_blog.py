import unittest
import os
import shutil
import sys
import subprocess
from datetime import datetime

import blog


class SandboxTestCase(unittest.TestCase):
    def make_sandbox(self):
        self.sandbox = '{0}/test-artifacts/'.format(
            os.getcwd(),
            self.__class__.__name__,
            self._testMethodName
        )
        try:
            shutil.rmtree(self.sandbox)
        except OSError:
            pass
        try:
            os.makedirs(self.sandbox)
        except OSError:
            pass

    def remove_sandbox(self):
        try:
            shutil.rmtree(self.sandbox)
        except IOError:
            pass


class TestCreateBlog(SandboxTestCase):
    def setUp(self):
        self.make_sandbox()

    def tearDown(self):
        self.remove_sandbox()

    def test_create_simple_blog(self):
        """ Check initially created blog """
        blog.create_blog(self.sandbox)
        real_list = [i[1:] for i in os.walk(self.sandbox)]
        expected_list = [
            (['_blog'], []),
            (['pages', 'templates'], ['draft_templates.json', 'default.json']),
            ([], []),
            ([], ['base.html', 'list.html', 'post.html', 'stat.html'])
        ]
        self.assertListEqual(real_list, expected_list)


class TestActionsBlog(SandboxTestCase):
    def setUp(self):
        self.make_sandbox()
        self.config = {
            'pages_dir': self.make_sandbox(),
            'date_format': "%Y-%m-%d %H:%M",
            'draft_templates': {
                "post": {
                    "content": "test note"
                }
            }
        }
        self.blog_action = blog.BlogAction(self.config)

    def tearDown(self):
        self.remove_sandbox()

    def test_post_draft(self):
        pass

    def test_build_pages(self):
        pass  # check that all generator and aggregator have run


class TestPageGenerator(SandboxTestCase):
    def setUp(self):
        self.make_sandbox()

    def tearDown(self):
        self.remove_sandbox()


class TestContentAggregator(SandboxTestCase):
    def setUp(self):
        self.make_sandbox()

    def tearDown(self):
        self.remove_sandbox()