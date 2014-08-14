# -*- encoding: utf-8 -*-


def selects_all_but_last_logical_tie_in_pitched_runs():
    r'''Selects all but last logical tie in pitched runs.

    ..  container:: example

        ::

            >>> selector = selectortools.selects_all_but_last_logical_tie_in_pitched_runs()
            >>> print(format(selector))
            selectortools.Selector(
                callbacks=(
                    selectortools.PrototypeSelectorCallback(
                        scoretools.Leaf
                        ),
                    selectortools.RunSelectorCallback(
                        (
                            scoretools.Note,
                            scoretools.Chord,
                            )
                        ),
                    selectortools.LogicalTieSelectorCallback(
                        flatten=False,
                        pitched=False,
                        trivial=True,
                        only_with_head=False,
                        only_with_tail=False,
                        ),
                    selectortools.SliceSelectorCallback(
                        argument=(None, -1),
                        apply_to_each=True,
                        ),
                    ),
                )

        ::

            >>> staff = Staff("c' d' ~ d' e' r f' g' r a' b' ~ b' c''")
            >>> tuplet = Tuplet((2, 3), staff[2:5])
            >>> tuplet = Tuplet((2, 3), staff[5:8])
            >>> print(format(staff))
            \new Staff {
                c'4
                d'4 ~
                \times 2/3 {
                    d'4
                    e'4
                    r4
                }
                f'4
                g'4
                \times 2/3 {
                    r4
                    a'4
                    b'4 ~
                }
                b'4
                c''4
            }

        ::

            >>> for x in selector(staff):
            ...     x
            ...
            Selection(LogicalTie(Note("c'4"),), LogicalTie(Note("d'4"), Note("d'4")))
            Selection(LogicalTie(Note("f'4"),),)
            Selection(LogicalTie(Note("a'4"),), LogicalTie(Note("b'4"), Note("b'4")))

    '''
    from experimental.tools import selectortools
    selector = selectortools.selects_pitched_runs()
    selector = selector.by_logical_tie(flatten=False)
    selector = selector[:-1]
    return selector