import abjad


def test_scoretools_VerticalMoment_next_vertical_moment_01():

    score = abjad.Score(r'''
        \new Staff {
            \times 4/3 {
                d''8
                c''8
                b'8
            }
        }
        \new PianoStaff <<
            \new Staff {
                a'4
                g'4
            }
            \new Staff {
                \clef "bass"
                f'8
                e'8
                d'8
                c'8
            }
        >>
        ''')

    vertical_moment = abjad.inspect(score).get_vertical_moment_at(abjad.Offset(0))
    assert vertical_moment.offset == abjad.Offset(0)

    vertical_moment = vertical_moment.next_vertical_moment
    assert vertical_moment.offset == abjad.Offset(1, 8)

    vertical_moment = vertical_moment.next_vertical_moment
    assert vertical_moment.offset == abjad.Offset(1, 6)

    vertical_moment = vertical_moment.next_vertical_moment
    assert vertical_moment.offset == abjad.Offset(1, 4)
