# -*- encoding: utf-8 -*-

__all__ = [
    'validate_page',
]


def validate_page(text: str) -> bool:
    result = True

    preps = [
        text == '{"error":"Not Found"}',
        "<title>Группы Google</title>" in text,
        '<title>Git and Mercurial code management for teams</title>' in text,
        "- Google Project Hosting" in text,
    ]

    if any(preps):
        result = False
    return result
