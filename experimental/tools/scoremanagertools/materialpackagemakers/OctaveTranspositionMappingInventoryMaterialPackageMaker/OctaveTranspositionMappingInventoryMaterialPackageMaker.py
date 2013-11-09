# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools.scoremanagertools.materialpackagemakers.InventoryMaterialPackageMaker \
    import InventoryMaterialPackageMaker
from experimental.tools.scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor \
    import OctaveTranspositionMappingInventoryEditor


class OctaveTranspositionMappingInventoryMaterialPackageMaker(
    InventoryMaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'octave transposition mapping inventory'

    output_material_checker = staticmethod(lambda x: isinstance(x,
        pitchtools.OctaveTranspositionMappingInventory))

    output_material_editor = OctaveTranspositionMappingInventoryEditor

    output_material_maker = pitchtools.OctaveTranspositionMappingInventory

    output_material_module_import_statements = [
        'from abjad.tools import pitchtools',
        ]

    ### PUBLIC METHODS ###

    @staticmethod
    def illustration_builder(
        octave_transposition_mapping_inventory, **kwargs):
        notes = []
        for octave_transposition_mapping in \
            octave_transposition_mapping_inventory:
            note = Note("c'4")
            notes.append(note)
        staff = scoretools.RhythmicStaff(notes)
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        illustration.paper_block.top_system_spacing = \
            layouttools.make_spacing_vector(0, 0, 6, 0)
        override(score).note_head.transparent = True
        override(score).bar_line.transparent = True
        override(score).clef.transparent = True
        override(score).span_bar.transparent = True
        override(score).staff_symbol.transparent = True
        override(score).stem.transparent = True
        override(score).time_signature.stencil = False
        contextualize(score).proportional_notation_duration = \
            schemetools.SchemeMoment(1, 24)
        return illustration
