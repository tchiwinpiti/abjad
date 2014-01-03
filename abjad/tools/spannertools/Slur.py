# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner


class Slur(Spanner):
    r'''A slur.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> slur = spannertools.Slur()
            >>> attach(slur, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff {
                c'8 (
                d'8
                e'8
                f'8 )
            }
            
    Formats LilyPond ``(`` command on first leaf in spanner.

    Formats LilyPond ``)`` command on last leaf in spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        direction = stringtools.arg_to_tridirectional_lilypond_symbol(
            direction)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._direction = self.direction

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            direction = self.direction
            if direction is not None:
                string = '{} ('.format(self.direction)
                result.append(string)
            else:
                result.append('(')
        if self._is_my_last_leaf(leaf):
            result.append(')')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction of slur.

        ..  container:: example

            Forces slur above staff:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> slur = spannertools.Slur(direction=Up)
                >>> attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8 ^ (
                    d'8
                    e'8
                    f'8 )
                    }

        ..  container:: example

            Forces slur below staff:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> slur = spannertools.Slur(direction=Down)
                >>> attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8 _ (
                    d'8
                    e'8
                    f'8 )
                }

        ..  container:: example

            Positions slur according to LilyPond defaults:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> slur = spannertools.Slur(direction=None)
                >>> attach(slur, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8 (
                    d'8
                    e'8
                    f'8 )
                }

        Returns up, down or none.
        '''
        return self._direction
