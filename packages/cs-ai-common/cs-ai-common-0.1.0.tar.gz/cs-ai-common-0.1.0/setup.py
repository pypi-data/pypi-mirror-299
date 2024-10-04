# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cs_ai_common', 'cs_ai_common.typings']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cs-ai-common',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Adrian Gajewski',
    'author_email': 'adrian.gajewski001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.12,<4.0',
}


setup(**setup_kwargs)
