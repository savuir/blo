import unittest
import os
import shutil

from blog import BlogAction, create_blog


class TestFunctionalBuild(unittest.TestCase):
    def setUp(self):
        self.make_sandbox()

    def tearDown(self):
        try:
            shutil.rmtree(self.sandbox)
        except IOError:
            pass

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

    def test_build_simple_blog(self):
        """ Check initially created blog """
        create_blog(self.sandbox)
        real_list = [i[1:] for i in os.walk(self.sandbox)]
        expected_list = [
            (['_blog'], []),
            (['pages', 'templates'], ['default.json']),
            ([], []),
            ([], ['base.html', 'list.html', 'post.html', 'stat.html'])
        ]
        self.assertListEqual(real_list, expected_list)

