from docutils.parsers.rst import directives  # type: ignore
from docutils.parsers.rst import Directive  # type: ignore
from sphinx.util.nodes import set_source_info  # type: ignore


class ImportDirective(Directive):
    r'''An abjad-book import directive.

    Represents a class or function to be imported into an interactive session.

    Generates an ``abjad_import_block`` node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'hide': directives.flag,
        'reveal-label': str,
        }

    ### PUBLIC METHODS ###

    def run(self):
        r'''Executes the directive.
        '''
        import abjad.book
        path = self.arguments[0]
        block = abjad.book.abjad_import_block()
        block['path'] = path
        if 'hide' in self.options:
            block['hide'] = True
        if 'reveal-label' in self.options:
            block['reveal-label'] = self.options.get('reveal-label')
        set_source_info(self, block)
        return [block]
