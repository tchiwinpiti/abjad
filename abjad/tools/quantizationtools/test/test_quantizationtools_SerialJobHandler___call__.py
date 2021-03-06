import abjad
from abjad.tools import quantizationtools


class Job(abjad.abctools.AbjadObject):

    ### INITIALIZER ###

    def __init__(self, number):
        self.number = number

    ### SPECIAL METHODS ###

    def __call__(self):
        self.result = [x for x in abjad.mathtools.yield_all_compositions_of_integer(self.number)]

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.number)


def test_quantizationtools_SerialJobHandler___call___01():

    jobs = [Job(x) for x in range(1, 11)]
    job_handler = quantizationtools.SerialJobHandler()
    finished_jobs = job_handler(jobs)
