# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_open_lilypond_log_01():
    r'''In score.
    '''

    input_ = 'red~example~score g log q'
    score_manager._run(input_=input_)
    
    assert score_manager._session._attempted_to_open_file


def test_SegmentPackageWrangler_open_lilypond_log_02():
    r'''Out of score.
    '''

    input_ = 'g log q'
    score_manager._run(input_=input_)
    
    assert score_manager._session._attempted_to_open_file