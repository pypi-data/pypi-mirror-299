# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyracf',
 'pyracf.access',
 'pyracf.common',
 'pyracf.connection',
 'pyracf.data_set',
 'pyracf.group',
 'pyracf.resource',
 'pyracf.scripts',
 'pyracf.setropts',
 'pyracf.user']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1']

setup_kwargs = {
    'name': 'pyracf',
    'version': '1.0b3',
    'description': 'Python interface to RACF using IRRSMO00 RACF Callable Service.',
    'long_description': '![pyRACF Logo](logo.png)\n\n![GitHub Actions Build Status](https://github.com/ambitus/pyracf/actions/workflows/.github-actions.yml/badge.svg?branch=dev)\n\nPython interface into the RACF management application programming interface.\n\n```python\n>>> from pyracf import UserAdmin\n>>> user_admin = UserAdmin()\n>>> user_admin.get_omvs_uid("squidwrd")\n2424\n>>> user_admin.set_omvs_uid("squidwrd", 1919)\n>>> user_admin.get_omvs_uid("squidwrd")\n1919\n```\n\n## Description\n\nAs automation becomes more and more prevalent, the need to manage the security environment programmatically increases. On z/OS that means managing a security product like the IBM Resource Access Control Facility (RACF). RACF is the primary facility for managing identity, authority, and access control for z/OS. There are more than 50 callable services with assembler interfaces that are part of the RACF API.\n\n[RACF callable services interfaces](http://publibz.boulder.ibm.com/epubs/pdf/ich2d112.pdf)\n\n While there are a number of languages that can be used to manage RACF, (from low level languages like Assembler to higher level languages like REXX), the need to have it in a language that is used to manage other platforms is paramount. The pyRACF project is focused on making the RACF management tasks available to Python programmers. This will make it easier to manage RACF from management tools like Ansible and Tekton.\n\n## Getting Started\n\n### Dependencies\n\n* z/OS 2.4 and higher.\n* R_SecMgtOper (IRRSMO00): Security Management Operations.\n* [The appropriate RACF authorizations](https://www.ibm.com/docs/en/zos/2.5.0?topic=operations-racf-authorization)\n\n### Installation\n\n:warning: _pyRACF will eventually be made available on [pypi.org](https://pypi.org/), but currently python wheel distributions for pyRACF are only available for manual download and installation via GitHub._\n\n* [Download & Install From GitHub](https://github.com/ambitus/pyracf/releases)\n\n### Usage\n\n* [pyRACF Documentation](https://ambitus.github.io/pyracf/)\n\n## Help\n\n* [Github Discussions](https://github.com/ambitus/pyracf/discussions)\n\n## Authors\n\n* Joe Bostian: jbostian@ibm.com\n* Frank De Gilio: degilio@us.ibm.com\n* Leonard Carcaramo: lcarcaramo@ibm.com\n* Elijah Swift: Elijah.Swift@ibm.com\n',
    'author': 'Joe Bostian',
    'author_email': 'jbostian@ibm.com',
    'maintainer': 'Leonard J. Carcaramo Jr',
    'maintainer_email': 'lcarcaramo@ibm.com',
    'url': 'https://github.com/ambitus/pyracf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}
from build_extension import *
build(setup_kwargs)

setup(**setup_kwargs)
