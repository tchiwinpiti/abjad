from experimental.tools import timespantools
from experimental.tools.requesttools.CommandRequest import CommandRequest


class DivisionCommandRequest(CommandRequest):
    '''Division command request.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name, offset, request_modifiers=None):
        CommandRequest.__init__(self, 'divisions', voice_name, offset,
            request_modifiers=request_modifiers)

    ### PUBLIC METHODS ###

    def get_payload(self, score_specification, voice_name):
        requested_segment_identifier = self.offset.start_segment_identifier
        requested_offset = self.offset._get_offset(score_specification, voice_name)
        timespan_inventory = timespantools.TimespanInventory()
        for division_region_command in score_specification.all_division_region_commands:
            if not division_region_command.request == self:
                timespan_inventory.append(division_region_command)
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=requested_offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = score_specification.get_start_segment_specification(requested_segment_identifier)
        # TODO: test from here down
        source_command = segment_specification.get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        absolute_request = source_command.request
        assert isinstance(absolute_request, requesttools.AbsoluteRequest), repr(absolute_request)
        divisions = absolute_request.payload
        return divisions
