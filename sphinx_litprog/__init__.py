'''
A literate programming extension for Sphinx.
'''

import os.path
import os

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx.directives.code import CodeBlock


__version__ = '0.1.0'


def _get_snippets(env):
    if not hasattr(env, 'litprog_snippets'):
        env.litprog_snippets = {}
    return env.litprog_snippets


class LitProg(CodeBlock):
    '''
    Literate programming directive.
    '''
    # In old Sphinx versions, the CodeBlock directive has a required argument
    required_arguments = 0

    option_spec = dict(CodeBlock.option_spec)
    option_spec['hidden'] = directives.flag

    def run(self):
        env = self.state.document.settings.env
        doc_snippets = _get_snippets(env).setdefault(env.docname, [])
        doc_snippets.extend(self.content)

        # Provide fake argument so that CodeBlock is happy in old
        # versions of Sphinx
        self.arguments = ['python']

        if 'hidden' in self.options:
            # Don't produce output in the documentation
            return []

        return super(LitProg, self).run()


def _purge_doc_snippets(app, env, docname):
    _get_snippets(env).pop(docname, None)


def _write_output(app, exception):
    if exception:
        return
    config = app.config
    env = app.env
    master_doc = config.master_doc
    includes = env.toctree_includes
    snippets = _get_snippets(env)

    filename = os.path.join(app.outdir, config.litprog_filename)
    print('Writing literate programming code to {}'.format(os.path.relpath(filename)))

    with open(filename, 'w', encoding='utf-8') as f:

        def visit(docname):
            doc_snippets = snippets.get(docname, [])
            if doc_snippets:
                f.write('\n'.join(doc_snippets) + '\n')
            for include in includes.get(docname, []):
                visit(include)

        visit(master_doc)


def setup(app):
    app.add_directive('litprog', LitProg)
    app.connect('env-purge-doc', _purge_doc_snippets)
    app.connect('build-finished', _write_output)
    app.add_config_value('litprog_filename', 'litprog.py', '')
    return {
        'version': __version__,
    }

