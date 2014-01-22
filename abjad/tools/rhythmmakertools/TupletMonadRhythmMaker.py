# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class TupletMonadRhythmMaker(RhythmMaker):
    r'''Tuplet monad rhythm-maker.

    ..  container:: example

        ::

            >>> maker = rhythmmakertools.TupletMonadRhythmMaker()

        ::

            >>> divisions = [(2, 5), (2, 5), (1, 4), (1, 5), (3, 4)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _class_name_abbreviation = 'TM'

    _human_readable_class_name = 'tuplet-monad rhythm-maker'

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls tuplet monad rhythm-maker on `divisions`.

        Returns list of tuplets.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats tuplet monad rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.TupletMonadRhythmMaker(
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    tie_across_divisions=False,
                    )

        Returns string.
        '''
        superclass = super(TupletMonadRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new tuplet monad rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker)

            ::

                >>> print format(new_maker)
                rhythmmakertools.TupletMonadRhythmMaker(
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    tie_across_divisions=False,
                    )

            ::

                >>> divisions = [(2, 5), (2, 5), (1, 4), (1, 5), (3, 4)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new tuplet monad rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _make_monad(self, division):
        numerator, talea_denominator = division
        power_of_two_denominator = \
            mathtools.greatest_power_of_two_less_equal(talea_denominator)
        duration = durationtools.Duration(abs(numerator), talea_denominator)
        power_of_two_duration = durationtools.Duration(
            abs(numerator), 
            power_of_two_denominator,
            )
        power_of_two_division = (numerator, power_of_two_denominator)
        tuplet_multiplier = duration / power_of_two_duration
        leaves = scoretools.make_leaves([0], [power_of_two_division])
        tuplet = scoretools.Tuplet(tuplet_multiplier, leaves)
        return tuplet

    def _make_music(self, duration_pairs, seeds):
        result = []
        for duration_pair in duration_pairs:
            monad = self._make_monad(duration_pair)
            result.append(monad)
        return result

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses tuplet monad rhythm-maker.

        ..  container:: example

            ::

                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.TupletMonadRhythmMaker(
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=False,
                    tie_across_divisions=False,
                    )

            ::

                >>> divisions = [(2, 5), (2, 5), (1, 4), (1, 5), (3, 4)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new tuplet monad rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
