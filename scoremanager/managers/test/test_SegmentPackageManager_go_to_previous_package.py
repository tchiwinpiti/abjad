# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_go_to_previous_package_01():

    input_ = 'red~example~score g A < q'
    score_manager._run(input_=input_)
    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments - A',
        'Red Example Score (2013) - segments - C',
        ]
    assert score_manager._transcript.titles == titles