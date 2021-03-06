from .Spanner import Spanner


class Slur(Spanner):
    r'''Slur.

    ..  container:: example

        Slurs four notes:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Slur(), staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                (
                d'4
                e'4
                f'4
                )
            }

    ..  container:: example

        Tweaks slur color:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> slur = abjad.Slur()
        >>> abjad.tweak(slur).color = 'red'
        >>> abjad.attach(slur, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                (
                d'4
                e'4
                f'4
                )
            }

    ..  container:: example

        Raises exception on fewer than two leaves:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Slur(), staff[:1])
        Traceback (most recent call last):
            ...
        Exception: Slur()._attachment_test_all():
          Requires at least two leaves.
          Not just Note("c'4").

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
        import abjad
        Spanner.__init__(self, overrides=overrides)
        direction = abjad.String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, component_expression):
        return self._at_least_two_leaves(component_expression)

    def _copy_keyword_args(self, new):
        new._direction = self.direction

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only_leaf(leaf):
            pass
        elif leaf is self[0]:
            if self.direction is not None:
                string = '{} ('.format(self.direction)
            else:
                string = '('
            bundle.right.spanner_starts.append(string)
        elif leaf is self[-1]:
            string = ')'
            bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Forces slur above staff:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur(direction=abjad.Up)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    ^ (
                    d'8
                    e'8
                    f'8
                    )
                }

        ..  container:: example

            Forces slur below staff:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur(direction=abjad.Down)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    _ (
                    d'8
                    e'8
                    f'8
                    )
                }

        ..  container:: example

            Positions slur according to LilyPond defaults:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur(direction=None)
            >>> abjad.attach(slur, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    d'8
                    e'8
                    f'8
                    )
                }

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction
