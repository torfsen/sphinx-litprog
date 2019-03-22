'''
A literate programming extension for Sphinx.
'''
import os.path

from docutils.parsers.rst import directives
from sphinx.builders import Builder
from sphinx.directives.code import CodeBlock
__version__ = '0.1.1'
class LitProgDirective(CodeBlock):
    '''
    Literate programming directive.

    Supports the same arguments/options as the ``code-block``
    directive.

    In addition, the ``:hidden:`` flag can be used to hide the
    content of the directive in the generated documentation (it will
    still be included in the exported literate programming source
    code).
    '''
    # In old Sphinx versions, the CodeBlock directive has a required
    # argument for specifying the programming language.
    required_arguments = 0

    option_spec = dict(CodeBlock.option_spec)
    option_spec['hidden'] = directives.flag

    def run(self):
        # Store content in environment for later export
        env = self.state.document.settings.env
        doc_snippets = _get_snippets(env).setdefault(env.docname, [])
        doc_snippets.extend(self.content)

        if 'hidden' in self.options:
            # Don't produce output in the documentation
            return []

        # Provide fake argument so that CodeBlock is happy in old
        # Sphinx versions
        self.arguments = ['python']

        # Delegate node creation to superclass
        return super().run()
def _get_snippets(env):
    '''
    Get the literate programming snippets from the environment.

    The snippets mapping is initialized if necessary.
    '''
    if not hasattr(env, 'litprog_snippets'):
        env.litprog_snippets = {}
    return env.litprog_snippets
class LitProgBuilder(Builder):
    name = 'litprog'

    def get_outdated_docs(self):
        return self.env.found_docs

    def get_target_uri(self, *args, **kwargs):
        return ''

    def prepare_writing(self, *args, **kwargs):
        return

    def write_doc(self, *args, **kwargs):
        return

    def finish(self):
        config = self.app.config
        env = self.app.env
        snippets = _get_snippets(env)
        filename = os.path.join(self.outdir, config.litprog_filename)
        with open(filename, 'w', encoding='utf-8') as f:
            for docname in _docnames_in_toc_order(env):
                doc_snippets = snippets.get(docname, [])
                if doc_snippets:
                    f.write('\n'.join(doc_snippets) + '\n')
def _docnames_in_toc_order(env):
    '''
    Yields all docnames in depth-first TOC order.
    '''
    includes = env.toctree_includes
    stack = [env.config.master_doc]
    while stack:
        docname = stack.pop()
        yield docname
        children = includes.get(docname, [])
        stack.extend(reversed(children))
def setup(app):
    app.add_builder(LitProgBuilder)
    app.add_directive('litprog', LitProgDirective)
    app.add_config_value('litprog_filename', 'litprog.py', '')
    app.connect('env-purge-doc', _purge_doc_snippets)
    return {
        'version': __version__,
        'env_version': 1,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
def _purge_doc_snippets(app, env, docname):
    _get_snippets(env).pop(docname, None)
