# -*- encoding: utf-8 -*-
from scoremanager.editors.InteractiveEditor import InteractiveEditor


class SpecifierEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        if self.target:
            return self.target._one_line_menuing_summary
