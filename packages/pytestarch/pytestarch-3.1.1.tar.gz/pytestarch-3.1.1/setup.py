# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytestarch',
 'pytestarch.diagram_extension',
 'pytestarch.eval_structure',
 'pytestarch.eval_structure_generation',
 'pytestarch.eval_structure_generation.file_import',
 'pytestarch.eval_structure_generation.graph_generation',
 'pytestarch.query_language',
 'pytestarch.rule_assessment',
 'pytestarch.rule_assessment.error_message',
 'pytestarch.rule_assessment.rule_check',
 'pytestarch.utils']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.2,<4.0']

extras_require = \
{'visualization': ['matplotlib>=3.9,<4.0']}

setup_kwargs = {
    'name': 'pytestarch',
    'version': '3.1.1',
    'description': 'Test framework for software architecture based on imports between modules',
    'long_description': '# Welcome to PyTestArch\n\nPyTestArch is an open source library that allows users to define architectural rules and test their code against them. It is \ngenerally inspired by [ArchUnit](https://www.archunit.org/).\n\n## Installation Guide\nPyTestArch is available via [PyPI](https://pypi.org/project/pytestarch/) and can be installed e.g. via pip: `pip install pytestarch`. To also install the\noptional dependency matplotlib, which is required to draw the created dependency graphs, install `pytestarch[visualization]`\n\n## Usage Guide\nThree steps are required to test an architectural rule:\n\n1) Create an evaluable representation of the source code you want to test\n\n```\nfrom pytestarch import get_evaluable_architecture\n\nevaluable = get_evaluable_architecture("/home/dummy/project", "/home/dummy/project/src")\n```\nThis will scan all python files under /home/dummy/project/src for imports and build an internal representation that can\nlater be queried. The first parameter /home/dummy/project helps PyTestArch to differentiate between internal and external \ndependencies. This evaluable can be used for multiple architectural rule checks; if you are using [pytest](https://docs.pytest.org/en/7.1.x/),\nyou could use a fixture for this evaluable object.\n\n2) Define an architectural rule\n```\nfrom pytestarch import Rule\n\nrule = (\n    Rule() \n    .modules_that() \n    .are_named("project.src.moduleB") \n    .should_not() \n    .be_imported_by_modules_that() \n    .are_sub_modules_of("project.src.moduleA") \n)\n```\n\nThis rule represents the architectural requirements that a module named "project.src.moduleB" should not be imported by any module\nthat is a submodule of "project.src.moduleA", excluding "project.src.moduleA" itself.\n\n3) Evaluate your code against this rule\n\n```\nrule.assert_applies(evaluable)\n```\nThat\'s it!\n',
    'author': 'zyskarch',
    'author_email': 'zyskarch@gmail.com',
    'maintainer': 'zyskarch',
    'maintainer_email': 'zyskarch@gmail.com',
    'url': 'https://github.com/zyskarch/pytestarch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
