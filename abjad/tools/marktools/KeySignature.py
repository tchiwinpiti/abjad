# -*- encoding: utf-8 -*-
from abjad.tools.marktools.ContextMark import ContextMark


class KeySignature(ContextMark):
    r'''A key signature contextualize or key signature change.

    ::

        >>> staff = Staff("e'8 fs'8 gs'8 a'8")
        >>> key_signature = marktools.KeySignature('e', 'major')
        >>> attach(key_signature, staff)
        KeySignature(NamedPitchClass('e'), Mode('major'))(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \key e \major
            e'8
            fs'8
            gs'8
            a'8
        }

    Key signature marks target staff context by default.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('c'),
        repr('major'),
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, tonic, mode, target_context=None):
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools import tonalanalysistools
        target_context = target_context or scoretools.Staff
        ContextMark.__init__(self, target_context=target_context)
        tonic = pitchtools.NamedPitchClass(tonic)
        mode = tonalanalysistools.Mode(mode)
        self._tonic = tonic
        self._mode = mode

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(self._tonic, self._mode,
            target_context = self._target_context)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.tonic == arg.tonic:
                if self.mode == arg.mode:
                    return True
        return False

    def __str__(self):
        return '%s-%s' % (self.tonic, self.mode)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return "%r, %r" % (self.tonic, self.mode)

    @property
    def _lilypond_format(self):
        return r'\key %s \%s' % (self.tonic, self.mode)

    ### PUBLIC PROPERTIES ###

    @apply
    def mode():
        def fget(self):
            r'''Get mode of key signature:

            ::

                >>> key_signature = marktools.KeySignature('e', 'major')
                >>> key_signature.mode
                Mode('major')

            Set mode of key signature:

            ::

                >>> key_signature.mode = 'minor'
                >>> key_signature.mode
                Mode('minor')

            Returns mode.
            '''
            return self._mode
        def fset(self, mode):
            from abjad.tools import tonalanalysistools
            mode = tonalanalysistools.Mode(mode)
            self._mode = mode
        return property(**locals())

    @property
    def name(self):
        r'''Name of key signature:

        ::

            >>> key_signature = marktools.KeySignature('e', 'major')
            >>> key_signature.name
            'E major'

        Returns string.
        '''
        if self.mode.mode_name == 'major':
            tonic = str(self.tonic).upper()
        else:
            tonic = str(self.tonic)
        return '%s %s' % (tonic, self.mode.mode_name)

    @apply
    def tonic():
        def fget(self):
            r'''Get tonic of key signature:

            ::

                >>> key_signature = marktools.KeySignature('e', 'major')
                >>> key_signature.tonic
                NamedPitchClass('e')

            Set tonic of key signature:

            ::

                >>> key_signature.tonic = 'd'
                >>> key_signature.tonic
                NamedPitchClass('d')

            Returns named pitch.
            '''
            return self._tonic
        def fset(self, tonic):
            from abjad.tools import pitchtools
            tonic = pitchtools.NamedPitchClass(tonic)
            self._tonic = tonic
        return property(**locals())
