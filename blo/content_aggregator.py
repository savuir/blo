"""
Module for content aggregation to give data
"""
import collections


class ContentAggregator:
    def __init__(self, config):
        self.tags = collections.defaultdict(list)
        self.content = collections.defaultdict(dict)
        self.config = config

    def get_content_items(self, tag=None):
        pages_list = []
        for page_url, page_vars in self.content.iteritems():
            if tag and tag not in page_vars['page_tags']:
                continue
            page_vars['page_url'] = page_url
            pages_list.append(page_vars)
        return sorted(pages_list,
                      key=lambda x: x['page_date_time'],
                      reverse=True)

    def get_tags_list(self):
        return sorted([{"page_url": "/tag/{0}.html".format(tag),
                        "page_title": tag,
                        "page_brefing": len(items)}
                       for tag, items in self.tags.iteritems()],
                      key=lambda x: x['page_brefing'],
                      reverse=True)

    def get_latest_posts(self, number=None):
        if not number and self.config.get('items_per_page'):
            number = self.config.get('items_per_page')
        posts = sorted(self.content.items(),
                       key=lambda x: x[1]['page_date_time'],
                       reverse=True)[:number]
        return collections.OrderedDict(posts)

