import math
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import marktools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from experimental.tools.handlertools.dynamics.DynamicHandler import DynamicHandler


class NoteAndChordSwellHandler(DynamicHandler):
    '''Note and chord swell handler.
    '''

    ### INITIALIZER ###

    def __init__(self, swell_dynamics=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        self.swell_dynamics = swell_dynamics

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        assert len(self.swell_dynamics) == 3, repr(self.swell_dynamics)
        start_dynamic, peak_dynamic, stop_dynamic = self.swell_dynamics
        leaves = list(iterationtools.iterate_leaves_in_expr(expr))
        leaves = leaftools.remove_outer_rests_from_sequence(leaves)
        assert 3 <= len(leaves)
        contexttools.DynamicMark(start_dynamic)(leaves[0])
        contexttools.DynamicMark(stop_dynamic)(leaves[-1])
        middle_index = int(math.ceil(len(leaves) / 2.0))
        middle_leaf = leaves[middle_index]
        contexttools.DynamicMark(peak_dynamic)(middle_leaf)
        return leaves

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def swell_dynamics():
        def fget(self):
            return self._swell_dynamics
        def fset(self, swell_dynamics):
            assert isinstance(swell_dynamics, (tuple, type(None))), repr(swell_dynamics)
            self._swell_dynamics = swell_dynamics
        return property(**locals())

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        new = type(self)(**kwargs)
        return new
