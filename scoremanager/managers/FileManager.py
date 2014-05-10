# -*- encoding: utf-8 -*-
import os
import shutil
import traceback
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.managers.Manager import Manager


class FileManager(Manager):
    r'''File manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(FileManager, self)
        superclass.__init__(path=path, session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_action(self):
        superlcass = super(FileManager, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'cp': self.copy,
            'e': self.edit,
            'o': self.open,
            'ren': self.rename,
            })
        return result

    ### PRIVATE METHODS ###

    def _execute(self, path=None, attribute_names=None):
        assert isinstance(attribute_names, tuple)
        path = path or self._path
        if not os.path.isfile(path):
            return
        file_pointer = open(path, 'r')
        file_contents_string = file_pointer.read()
        file_pointer.close()
        try:
            exec(file_contents_string)
        except:
            traceback.print_exc()
            self._io_manager.display('')
            return 'corrupt'
        result = []
        for name in attribute_names:
            if name in locals():
                result.append(locals()[name])
            else:
                result.append(None)
        result = tuple(result)
        return result

    def _get_space_delimited_lowercase_name(self):
        if self._path:
            base_name = os.path.basename(self._path)
            name = base_name.strip('.py')
            name = stringtools.to_space_delimited_lowercase(name)
            return name

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            self.edit()

    def _is_editable(self):
        if self._path.endswith(('.tex', '.py')):
            return True
        return False

    def _make_empty_asset(self, prompt=False):
        if not os.path.exists(self._path):
            with file(self._path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.proceed(prompt=prompt)

    def _make_file_menu_section(self, menu):
        commands = []
        if self._is_editable():
            commands.append(('file - edit', 'e'))
        else:
            commands.append(('file - open', 'o'))
        commands.append(('file - rename', 'ren'))
        commands.append(('file - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            )

    def _make_main_menu(self, name='file manager'):
        menu = self._io_manager.make_menu(name=name)
        self._main_menu = menu
        self._make_file_menu_section(self, menu)
        return menu

    def _read_lines(self):
        result = []
        if self._path:
            if os.path.exists(self._path):
                with file(self._path) as file_pointer:
                    result.extend(file_pointer.readlines())
        return result
    
    def _write(self, contents):
        with file(self._path, 'w') as file_pointer:
            file_pointer.write(contents)

    def _write_stub(self):
        self._write(self._unicode_directive)

    ### PUBLIC METHODS ###

    def copy(
        self, 
        extension=None, 
        file_name_callback=None,
        force_lowercase=True,
        ):
        r'''Copies file.

        Returns none.
        '''
        getter = self._initialize_file_name_getter()
        name = getter._run()
        if self._should_backtrack():
            return
        name = stringtools.strip_diacritics(name)
        if file_name_callback:
            name = file_name_callback(name)
        name = name.replace(' ', '_')
        if force_lowercase:
            name = name.lower()
        if extension and not name.endswith(extension):
            name = name + extension
        parent_directory_path = os.path.dirname(self._path)
        new_path = os.path.join(parent_directory_path, name)
        message = 'new path will be {}'
        message = message.format(new_path)
        self._io_manager.display(message)
        result = self._io_manager.confirm()
        if self._should_backtrack():
            return
        if not result:
            return
        shutil.copyfile(self._path, new_path)
        message = 'copied {}.'.format(self._path)
        self._io_manager.proceed(message)

    def edit(self, line_number=None):
        r'''Edits file.

        Returns none.
        '''
        self._io_manager.edit(
            self._path,
            line_number=line_number,
            )

    def interpret(self, prompt=True):
        r'''Calls Python on file.

        Returns integer success code.
        '''
        _, extension = os.path.splitext(self._path)
        if extension == '.py':
            command = 'python {}'.format(self._path)
        elif extension == '.ly':
            command = 'lilypond {}'.format(self._path)
        else:
            message = 'can not interpret {}.'.format(self._path)
            raise Exception(message)
        directory = os.path.dirname(self._path)
        context = systemtools.TemporaryDirectoryChange(directory)
        with context:
            result = self._io_manager.spawn_subprocess(command)
        if result != 0:
            self._io_manager.display('')
        elif prompt:
            message = 'interpreted {}.'.format(self._path)
            self._io_manager.display([message])
        return result

    def open(self):
        r'''Opens file.

        Returns none.
        '''
        if os.path.isfile(self._path):
            self._io_manager.open_file(self._path)
        else:
            message = 'Can not find {}.'.format(self._path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True

    def rename(
        self, 
        extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        r'''Renames file.

        Returns none.
        '''
        self._rename_interactively(
            extension=extension,
            file_name_callback=file_name_callback,
            force_lowercase=force_lowercase,
            )