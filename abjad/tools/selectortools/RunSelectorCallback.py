# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject
from abjad.tools import selectiontools
from abjad.tools.topleveltools import iterate


class RunSelectorCallback(AbjadValueObject):
    r'''Run selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_prototype',
        )

    ### INITIALIZER ###

    def __init__(self, prototype=None):
        prototype = prototype or ()
        if isinstance(prototype, collections.Sequence):
            prototype = tuple(prototype)
            assert all(isinstance(x, type) for x in prototype)
        assert isinstance(prototype, (tuple, type))
        self._prototype = prototype

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Iterates tuple `argument`.

        Returns tuple of selections.
        '''
        assert isinstance(argument, tuple), repr(argument)
        result = []
        prototype = self.prototype
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        for subexpr in argument:
            for run in iterate(subexpr).by_run(prototype):
                run = selectiontools.Selection(run)
                result.append(run)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def prototype(self):
        r'''Gets run selector callback prototype.

        Return tuple of classes.
        '''
        return self._prototype
