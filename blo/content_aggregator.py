"""
Module for content aggregation to give data
"""
from collections import defaultdict


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