# -*- encoding: utf-8 -*-


from .checkers import *
from .dev import *
from .helpers import *
from .io import *
from .prepare import *
from .site_checkers import *
from .site_extractors import *
from .validate import *

SITE_CHECKERS = {
    'pypi': check_pypi,
    'github': check_github,
}

SITE_EXTRACTORS = {
    'pypi': extract_pypi,
    'github': extract_github,
}
