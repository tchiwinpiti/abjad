# -*- coding: utf-8 -*-
from abjad.tools.scoretools.Container import Container


class GraceContainer(Container):
    r'''Grace container.

    LilyPond positions grace notes immediately before main notes.

    LilyPond formats grace notes with neither a slashed nor a slur.

    .. container:: example

        Grace notes:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> grace_notes = [Note("c'16"), Note("d'16")]
            >>> grace_container = GraceContainer(grace_notes)
            >>> attach(grace_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  docs::

            >>> f(voice)
            \new Voice {
                c'4
                \grace {
                    c'16
                    d'16
                }
                d'4
                e'4
                f'4
            }

    Fill grace containers with notes, rests or chords.

    Attach grace containers to notes, rests or chords.

    ..  container:: example

        Detaches grace container:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> note = Note("cs'16")
            >>> grace_container = GraceContainer([note])
            >>> attach(grace_container, voice[1])
            >>> note = Note("ds'16")
            >>> after_grace_container = AfterGraceContainer([note])
            >>> attach(after_grace_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  docs::

            >>> f(voice)
            \new Voice {
                c'4
                \grace {
                    cs'16
                }
                \afterGrace
                d'4
                {
                    ds'16
                }
                e'4
                f'4
            }

        ::

            >>> detach(GraceContainer, voice[1])
            (GraceContainer(),)
            >>> show(voice) # doctest: +SKIP

        ..  docs::

            >>> f(voice)
            \new Voice {
                c'4
                \afterGrace
                d'4
                {
                    ds'16
                }
                e'4
                f'4
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_carrier',
        )

    ### INITIALIZER ###

    def __init__(self, music=None):
        self._carrier = None
        Container.__init__(self, music)

    ### PRIVATE METHODS ###

    def _attach(self, leaf):
        import abjad
        if not isinstance(leaf, abjad.Leaf):
            message = 'must attach to leaf: {!r}.'
            message = message.format(leaf)
            raise TypeError(message)
        leaf._grace_container = self
        self._carrier = leaf

    def _detach(self):
        if self._carrier is not None:
            carrier = self._carrier
            carrier._grace_container = None
            self._carrier = None
            self[:] = []
        return self

    def _format_open_brackets_slot(self, bundle):
        result = []
        result.append([('grace_brackets', 'open'), [r'\grace {']])
        return tuple(result)

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()
