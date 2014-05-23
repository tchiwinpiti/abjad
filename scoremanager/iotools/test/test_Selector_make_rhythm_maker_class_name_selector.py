# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.core.Session(is_test=True)


def test_Selector_make_rhythm_maker_class_name_selector_01():

    selector = scoremanager.iotools.Selector(session=session)
    selector = selector.make_rhythm_maker_class_name_selector()
    selector._session._is_test = True

    input_ = 'note'
    result = selector._run(input_=input_)
    assert result == 'NoteRhythmMaker'