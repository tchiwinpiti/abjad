# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_write_stub_init_py_01():
    r'''Works when __init__.py doesn't already exist.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_01',
        '__init__.py',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score g A inpyws y q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(path)
        contents = score_manager._transcript.contents
        assert 'Will write stub to' in contents