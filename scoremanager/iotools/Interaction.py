# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class Interaction(ContextManager):
    r'''Interation context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_controller',
        '_display',
        '_dry_run',
        '_task',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        controller=None, 
        display=True, 
        dry_run=False,
        task=True,
        ):
        self._controller = controller
        self._display = display
        self._dry_run = dry_run
        self._task = task

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters interaction manager.

        Returns none.
        '''
        self._controller._session._interaction_depth += 1
        if self.task:
            self._controller._session._task_depth += 1

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits interaction manager.

        Returns none.
        '''
        self._controller._session._interaction_depth -= 1
        if self.task:
            self._controller._session._task_depth -= 1
        if self.display and not self.dry_run:
            self.controller._session._hide_next_redraw = False
            self.controller._io_manager._display('')
        self.controller._session._hide_next_redraw = True

    ### PUBLIC PROPERTIES ###

    @property
    def controller(self):
        r'''Gets controller of interaction.

        Returns controller.
        '''
        return self._controller

    @property
    def display(self):
        r'''Is true when blank line should display at end of interaction.
        Otherwise false.

        Returns boolean.
        '''
        return self._display

    @property
    def dry_run(self):
        r'''Is true when interaction is dry run. Otherwise false.

        Nothing will be displayed during dry run.

        Inputs and outputs will be returned from dry run.

        Returns boolean.
        '''
        return self._dry_run

    @property
    def task(self):
        r'''Is true when interaction is a task. Otherwise false.

        Main menus are not tasks; public methods are tasks.

        Tasks are not implemented around a while-true loop; main menus are
        implemented around a while-true loop.

        Returns boolean.
        '''
        return self._task