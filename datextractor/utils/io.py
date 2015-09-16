# -*- encoding: utf-8 -*-

import yaml
import csv

__all__ = [
    'read_csv',
    'loadyaml',
    'get_date_tags',
]


def read_csv(filepath: str) -> list:
    with open(filepath, 'r') as fio:
        return [row for row in csv.reader(fio)]


def loadyaml(filepath: str) -> object:
    with open(filepath, 'r') as fio:
        return yaml.load(fio.read())


def get_date_tags() -> dict:
    return {
        "p": [
            {"class": "date"},
            {"class": "time"},
            {"class": "meta"},
            {"class": "blog-post-meta single"},
            {"class": "last-updated"},
            {"class": "post-meta"},
            {"class": "post-date"},
        ],
        "h2": [
            {"class": "date-header"},
        ],
        "h4": [
            {"class": "entry-meta"},
        ],
        "h6": [
            {"class": "post-meta"},
        ],
        "time": [
            {"class": "post-time"},
            {"itemprop": "datePublished"},
            {},
        ],
        "div": [
            {"class": "FeatureByline"},
            {"class": "post-meta"},
            {"class": "author_date"},
            {"class": "marg__b_mid text-muted"},
            {"class": "entry entry-1"},
            {"class": "published"},
            {"class": "post-info"},
            {"class": "blog_date"},
            {"class": "user-action-time"},
            {"class": "data-title"},
            {"class": "italics"},
            {"class": "tutorial-date"},
            {"class": "post-author"},
            {"class": "Byline"},
            {"class": "date"},
            {"class": "time"},
            {"id": "last_updated"},
            {"id": "blogpost-info"},
            {"id": "bio_date"},
            {"class": "infos"},
            {"class": "row withgap"},
            {"class": "submitted"},
        ],
        "span": [
            {"class": "postMetaInline postMetaInline--supplemental"},
            {"class": "meta"},
            {"class": "date"},
            {"class": "event-page-date"},
            {"class": "label label-default"},
            {"class": "entry-date"},
            {"itemprop": "datePublished"},
            {"class": "postAuthor hideOnIndex"},
            {"style": "cursor:help;border-bottom: 1px dotted;"},
            {"class": "timestamp"},
            {"class": "created-date"},
            {"class": "wi_date"},
            {"class": "post-date"}
        ],
        "td": [
            {"align": "left", "valign": "middle"},
        ],
        "table": [
            {"class": "list"},
        ],
        "small": [
            {"class": "commentmetadata"},
        ],
        "meta": [
            {"name": "publishedDate"},
            {"itemprop": "publishedDate"},
            {"itemprop": "datePublished"},
            {"property": "article:published_time"},
            {"property": "og:article:modified_time"},
        ],
        "abbr": [
            {"class": "published"},
        ],
        "ul": [
            {"class": "post-info"},
            {"class": "post-date"},
        ],
        "li": [
            {"class": "time"},
            {"class": "date"},
            {"class": "node_submitted first"},
        ],
        "header": [
            {},
        ]
    }
