# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LogicalVoiceIndicator(AbjadObject):
    r'''Containment signature of Abjad component:

    ::

        >>> score = Score(r"""\context Staff = "CustomStaff" { """
        ...     r"""\context Voice = "CustomVoice" { c' d' e' f' } }""")
        >>> score.name = 'CustomScore'

    ..  doctest::

        >>> f(score)
        \context Score = "CustomScore" <<
            \context Staff = "CustomStaff" {
                \context Voice = "CustomVoice" {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }
        >>

    ::

        >>> parentage = more(score.select_leaves()[0]).select_parentage()
        >>> print parentage.logical_voice_indicator
            score: Score-'CustomScore'
            staff: Staff-...
            voice: Voice-'CustomVoice'

    Used for logical voice iteration behind the scenes.
    '''

    ### INITIALIZER ###

    def __init__(self):
        self._score = None
        self._staff = None
        self._staff_group = None
        self._voice = None

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if not isinstance(arg, LogicalVoiceIndicator):
            return False
        if not self._voice == arg._voice:
            return False
        if not self._staff == arg._staff:
            return False
        if not self._staff_group == arg._staff_group:
            return False
        if not self._score == arg._score:
            return False
        return True

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        values = [x[-1] for x in self._parts]
        values = ', '.join(values)
        return '{}({})'.format(self._class_name, values)

    def __str__(self):
        result = []
        for name, value in reversed(self._parts):
            result.append('%10s: %s' % (name, value))
        return '\n'.join(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _parts(self):
        result = []
        attrs = ('voice', 'staff', 'staff_group', 'score')
        for attr in attrs:
            if getattr(self, '_' + attr, None) is not None:
                result.append((attr, getattr(self, '_' + attr)))
        return result
