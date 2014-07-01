# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_edit_every_output_py_01():

    input_ = 'red~example~score m oe* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert ide._session._attempted_to_open_file

    package_names = (
        'instrumentation',
        'magic_numbers',
        'pitch_range_inventory',
        'tempo_inventory',
        )

    paths = []
    for package_name in package_names:
        path = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            package_name,
            'output.py',
            )

    lines = []
    lines.append('Will open ...')
    lines.extend(paths)

    for line in lines:
        assert line in contents