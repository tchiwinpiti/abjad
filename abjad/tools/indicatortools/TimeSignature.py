import collections
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class TimeSignature(AbjadValueObject):
    r'''Time signature.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \time 3/8
                c'8
                d'8
                e'8
            }

    ..  container:: example

        Create score-contexted time signatures like this:

        >>> staff = abjad.Staff("c'8 d'8 e'8 c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0], context='Score')

        Score-contexted time signatures format behind comments when no Abjad
        score container is found:

        >>> abjad.f(staff)
        \new Staff
        {
            %%% \time 3/8 %%%
            c'8
            d'8
            e'8
            c'8
            d'8
            e'8
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Score-contexted time signatures format normally when an Abjad score
        container is found:

        >>> score = abjad.Score([staff])
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                \time 3/8
                c'8
                d'8
                e'8
                c'8
                d'8
                e'8
            }
        >>

        >>> abjad.show(score) # doctest: +SKIP

    ..  container:: example

        Time signatures can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0], context='Score', tag='RED')
        >>> score = abjad.Score([staff])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                \time 3/8 %! RED
                c'8
                d'8
                e'8
                c'8
                d'8
                e'8
            }
        >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_denominator',
        '_has_non_power_of_two_denominator',
        '_hide',
        '_multiplier',
        '_numerator',
        '_partial',
        '_partial_repr_string',
        )

    _context = 'Staff'

    _format_slot = 'opening'

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        pair=(4, 4),
        partial=None,
        hide=None,
        ):
        import abjad
        pair = getattr(pair, 'pair', pair)
        assert isinstance(pair, collections.Iterable), repr(pair)
        assert len(pair) == 2, repr(pair)
        numerator, denominator = pair
        assert isinstance(numerator, int), repr(numerator)
        assert isinstance(denominator, int), repr(denominator)
        self._numerator = numerator
        self._denominator = denominator
        if partial is not None:
            partial = abjad.Duration(partial)
        self._partial = partial
        if partial is not None:
            self._partial_repr_string = ', partial=%r' % self._partial
        else:
            self._partial_repr_string = ''
        assert isinstance(hide, (bool, type(None))), repr(hide)
        self._hide = hide
        self._multiplier = self.implied_prolation
        self._has_non_power_of_two_denominator = \
            not abjad.mathtools.is_nonnegative_integer_power_of_two(
                self.denominator)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds time signature to `argument`.

        ..  container:: example

            Adds two time signatures with the same denominator:

            >>> abjad.TimeSignature((3, 4)) + abjad.TimeSignature((3, 4))
            TimeSignature((6, 4))

        ..  container:: example

            Adds two time signatures with different denominators:

            >>> abjad.TimeSignature((3, 4)) + abjad.TimeSignature((6, 8))
            TimeSignature((12, 8))

            Returns new time signature in terms of greatest denominator.

        Returns new time signature.
        '''
        import abjad
        if not isinstance(argument, type(self)):
            message = 'must be time signature: {!r}.'
            message = message.format(argument)
            raise Exception(message)
        nonreduced_1 = abjad.NonreducedFraction(
            self.numerator,
            self.denominator,
            )
        nonreduced_2 = abjad.NonreducedFraction(
            argument.numerator,
            argument.denominator,
            )
        result = nonreduced_1 + nonreduced_2
        result = type(self)((
            result.numerator,
            result.denominator,
            ))
        return result

    def __copy__(self, *arguments):
        r'''Copies time signature.

        Returns new time signature.
        '''
        return type(self)(
            (self.numerator, self.denominator),
            partial=self.partial,
            )

    def __eq__(self, argument):
        r'''Is true when `argument` is a time signature with numerator and
        denominator equal to this time signature. Also true when `argument` is
        a tuple with first and second elements equal to numerator and
        denominator of this time signature. Otherwise false.

        Returns true or false.
        '''
        # custom definition retained only bc tests currently break with super()
        if isinstance(argument, type(self)):
            return (self.numerator == argument.numerator and
                self.denominator == argument.denominator)
        elif isinstance(argument, tuple):
            return self.numerator == argument[0] and self.denominator == argument[1]
        else:
            return False

    def __format__(self, format_specification=''):
        r'''Formats time signature.

        ..  container:: example

            >>> print(format(abjad.TimeSignature((3, 8))))
            abjad.TimeSignature((3, 8))

        Returns string.
        '''
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._get_lilypond_format()
        return str(self)

    def __ge__(self, argument):
        r'''Is true when duration of time signature is greater than or equal to
        duration of `argument`. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            return self.duration >= argument.duration
        else:
            raise TypeError(argument)

    def __gt__(self, argument):
        r'''Is true when duration of time signature is greater than duration of
        `argument`. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            return self.duration > argument.duration
        else:
            raise TypeError(argument)

    def __hash__(self):
        r'''Hashes time signature.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(TimeSignature, self).__hash__()

    def __le__(self, argument):
        r'''Is true when duration of time signature is less than duration of
        `argument`. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            return self.duration <= argument.duration
        else:
            raise TypeError(argument)

    def __lt__(self, argument):
        r'''Is true when duration of time signature is less than duration of
        `argument`. Otherwise false.

        Returns booelan.
        '''
        if isinstance(argument, type(self)):
            return self.duration < argument.duration
        else:
            raise TypeError(argument)

    def __radd__(self, argument):
        r'''Adds `argument` to time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)) + abjad.TimeSignature((4, 4))
            TimeSignature((11, 8))

        Returns new time signature.
        '''
        return self.__add__(argument)

    def __str__(self):
        r'''Gets string representation of time signature.

        ..  container:: example

            >>> str(abjad.TimeSignature((3, 8)))
            '3/8'

        Returns string.
        '''
        return '{}/{}'.format(self.numerator, self.denominator)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return '{}/{}'.format(self.numerator, self.denominator)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        storage_format_is_indented = False
        if self.partial is not None or self.hide is not None:
            storage_format_is_indented = True
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.pair],
            storage_format_kwargs_names=['partial', 'hide'],
            storage_format_is_indented=storage_format_is_indented,
            )

    def _get_lilypond_format(self):
        if self.hide:
            return []
        elif self.partial is None:
            return r'\time {}/{}'.format(
                int(self.numerator),
                int(self.denominator),
                )
        else:
            result = []
            duration_string = self.partial.lilypond_duration_string
            partial_directive = r'\partial {}'.format(duration_string)
            result.append(partial_directive)
            string = r'\time {}/{}'.format(
                int(self.numerator),
                int(self.denominator),
                )
            result.append(string)
            return result

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets (historically conventional) context.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).context
            'Staff'

        Returns ``'Staff'``.

        ..  todo:: Should return ``'Score'``.

        Override with ``abjad.attach(..., context='...')``.
        '''
        return self._context

    @property
    def denominator(self):
        r'''Gets denominator of time signature:

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).denominator
            8

        Set to positive integer.

        Returns positive integer.
        '''
        return self._denominator

    @property
    def duration(self):
        r'''Gets duration of time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).duration
            Duration(3, 8)

        Returns duration.
        '''
        import abjad
        return abjad.Duration(self.numerator, self.denominator)

    @property
    def has_non_power_of_two_denominator(self):
        r'''Is true when time signature has non-power-of-two denominator.
        Otherwise false.

        ..  container:: example

            With non-power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((7, 12))
            >>> time_signature.has_non_power_of_two_denominator
            True

        ..  container:: example

            With power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((3, 8))
            >>> time_signature.has_non_power_of_two_denominator
            False

        Returns true or false.
        '''
        return self._has_non_power_of_two_denominator

    @property
    def hide(self):
        r'''Is true when time signature should not appear in output (but should
        still determine effective time signature).

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> time_signature = abjad.TimeSignature((4, 4))
            >>> abjad.attach(time_signature, staff[0]) 
            >>> time_signature = abjad.TimeSignature((2, 4), hide=True)
            >>> abjad.attach(time_signature, staff[2]) 
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            {
                \time 4/4
                c'4
                d'4
                e'4
                f'4
            }

            >>> for leaf in abjad.iterate(staff).leaves():
            ...     prototype = abjad.TimeSignature 
            ...     leaf, abjad.inspect(leaf).get_effective(prototype)
            ...
            (Note("c'4"), TimeSignature((4, 4)))
            (Note("d'4"), TimeSignature((4, 4)))
            (Note("e'4"), TimeSignature((2, 4), hide=True))
            (Note("f'4"), TimeSignature((2, 4), hide=True))

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._hide

    @property
    def implied_prolation(self):
        '''Gets implied prolation of time signature.

        ..  container:: example

            Implied prolation of time signature with power-of-two denominator:

            >>> abjad.TimeSignature((3, 8)).implied_prolation
            Multiplier(1, 1)

        ..  container:: example

            Implied prolation of time signature with non-power-of-two
            denominator:

            >>> abjad.TimeSignature((7, 12)).implied_prolation
            Multiplier(2, 3)

        Returns multiplier.
        '''
        import abjad
        dummy_duration = abjad.Duration(1, self.denominator)
        return dummy_duration.implied_prolation

    @property
    def numerator(self):
        r'''Gets numerator of time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).numerator
            3

        Set to positive integer.

        Returns positive integer.
        '''
        return self._numerator

    @property
    def pair(self):
        '''Gets numerator / denominator pair corresponding to time siganture.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).pair
            (3, 8)

        Returns pair.
        '''
        return (self.numerator, self.denominator)

    @property
    def partial(self):
        r'''Gets duration of pick-up to time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).partial is None
            True

        Set to duration or none.

        Defaults to none.

        Returns duration or none.
        '''
        return self._partial

    @property
    def persistent(self):
        r'''Is true.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).persistent
            True

        Returns true.
        '''
        return self._persistent

    ### PUBLIC METHODS ###

    @staticmethod
    def from_string(string):
        r'''Makes new time signature from fraction `string`.

        ..  container:: example

            >>> abjad.TimeSignature.from_string('6/8')
            TimeSignature((6, 8))

        Returns new time signature.
        '''
        assert isinstance(string, str), repr(string)
        parts = string.split('/')
        assert len(parts) == 2, repr(parts)
        parts = [int(_) for _ in parts]
        numerator, denominator = parts
        return TimeSignature((numerator, denominator))

    def with_power_of_two_denominator(self, contents_multiplier=1):
        r'''Makes new time signature equivalent to current
        time signature with power-of-two denominator.

        ..  container:: example

            Non-power-of-two denominator with power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((3, 12))
            >>> time_signature.with_power_of_two_denominator()
            TimeSignature((2, 8))

        Returns new time signature.
        '''
        import abjad
        contents_multiplier = abjad.Multiplier(contents_multiplier)
        contents_multiplier = abjad.Multiplier(contents_multiplier)
        non_power_of_two_denominator = self.denominator
        if contents_multiplier == abjad.Multiplier(1):
            power_of_two_denominator = \
                abjad.mathtools.greatest_power_of_two_less_equal(
                    non_power_of_two_denominator)
        else:
            power_of_two_denominator = \
                abjad.mathtools.greatest_power_of_two_less_equal(
                    non_power_of_two_denominator, 1)
        non_power_of_two_pair = abjad.NonreducedFraction(self.pair)
        power_of_two_fraction = non_power_of_two_pair.with_denominator(
            power_of_two_denominator)
        power_of_two_pair = power_of_two_fraction.pair
        return type(self)(power_of_two_pair)
