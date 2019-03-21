import io
import os.path
import sys

import sphinx.cmd.build


HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PROJECT_PATH = os.path.join(HERE, 'test-project')
TEST_PROJECT_BUILD_PATH = os.path.join(TEST_PROJECT_PATH, '_build')


def compile_test_project():
    '''
    Compile the test project and return the literate programming output.
    '''
    exit_code = sphinx.cmd.build.main(argv=[
        '-b', 'litprog',
        TEST_PROJECT_PATH,
        TEST_PROJECT_BUILD_PATH,
    ])
    if exit_code != 0:
        raise RuntimeError(
            'sphinx-build returned exit code {}'.format(exit_code)
        )
    litprog_file = os.path.join(TEST_PROJECT_BUILD_PATH, 'litprog.py')
    with open(litprog_file, encoding='utf-8') as f:
        return f.read()


def test_sphinx_litprog():
    litprog_output = compile_test_project()
    assert litprog_output == '1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n'

