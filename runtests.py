#!/usr/bin/env python
import os
import sys


os.environ['DJANGO_SETTINGS_MODULE'] = 'project_template.settings'
project_template_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'project_template')
sys.path.insert(0, project_template_dir)

from django.test.utils import get_runner
from django.conf import settings


def runtests(tests=('mezzanine_page_auth',)):
    """
    Takes a list as first argument, enumerating the apps and specific testcases
    that should be executed. The syntax is the same as for what you would pass
    to the ``django-admin.py test`` command.

    Examples::

        # run the default test suite
        runtests()

        # only run the tests from application ``mezzanine_page_auth``
        runtests(['mezzanine_page_auth'])

        # only run testcase class ``UnauthorizedListPagesPageAuthGroupTest``
        # from app ``mezzanine_page_auth``
        runtests(['mezzanine_page_auth.UnauthorizedListPagesPageAuthGroupTest'])

        # run all tests from application ``mezzanine_page_auth`` and the test
        # named ``test_register`` on the
        # ``mezzanine_page_auth.UnauthorizedListPagesPageAuthGroupTest``
        # testcase.
        runtests(['mezzanine_page_auth.UnauthorizedListPagesPageAuthGroupTest.
        test_unauthorized_list_pages_with_user_with_one_group''])
    """
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(tests)
    sys.exit(bool(failures))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        tests = sys.argv[1:]
        runtests(tests)
    else:
        runtests()