# -*- encoding: utf-8 -*-
import abc
import copy
import os
import subprocess
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.Controller import Controller


class Wrangler(Controller):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_abjad_storehouse_path',
        '_forbidden_directory_entries',
        '_main_menu',
        '_manager_class',
        '_score_storehouse_path_infix_parts',
        '_user_storehouse_path',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        assert session is not None
        Controller.__init__(self, session=session)
        self._abjad_storehouse_path = None
        self._forbidden_directory_entries = ()
        self._score_storehouse_path_infix_parts = ()
        self._user_storehouse_path = None

    ### PRIVATE PROPERTIES ###

    @property
    def _current_package_manager(self):
        path = self._get_current_directory_path()
        if path is None:
            return
        return self._io_manager.make_package_manager(path)

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory_path)
            parts.extend(self._score_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self._abjad_storehouse_path

    @property
    def _initializer_file_path(self):
        path = self._get_current_directory_path()
        if path:
            return os.path.join(path, '__init__.py')

    @property
    def _user_input_to_action(self):
        superclass = super(Wrangler, self)
        result = superclass._user_input_to_action
        result = copy.deepcopy(result)
        result.update({
            'pyt': self.pytest,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'rrv': self.revert_to_repository,
            'rst': self.repository_status,
            'rup': self.update_from_repository,
            'va': self.apply_view,
            'vls': self.list_views,
            'vnew': self.make_view,
            'vren': self.rename_view,
            'vrm': self.remove_view,
            'vmrm': self.remove_views_module,
            'vmro': self.view_views_module,
            'V': self.clear_view,
            })
        return result

    @property
    @systemtools.Memoize
    def _views_directory_manager(self):
        path = self._configuration.user_library_views_directory_path
        return self._io_manager.make_directory_manager(path)

    @property
    @systemtools.Memoize
    def _views_module_manager(self):
        return self._io_manager.make_file_manager(self._views_module_path)

    @property
    def _views_module_path(self):
        if self._session.is_in_score:
            directory = self._get_current_directory_path()
            return os.path.join(directory, '__views__.py')
        else:
            directory = self._configuration.user_library_views_directory_path
            class_name = type(self).__name__
            file_name = '__{}_views__.py'.format(class_name)
            return os.path.join(directory, file_name)

    ### PRIVATE METHODS ###

    def _enter_run(self):
        pass

    def _extract_common_parent_directories(self, paths):
        parent_directories = []
        user_score_packages_directory_path = \
            self._configuration.user_score_packages_directory_path
        for path in paths:
            parent_directory = os.path.dirname(path)
            if parent_directory == user_score_packages_directory_path:
                parent_directories.append(path)
            elif parent_directory not in parent_directories:
                parent_directories.append(parent_directory)
        return parent_directories

    def _find_git_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=True,
            repository='git',
            )
        return manager

    def _find_svn_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=False,
            repository='svn',
            )
        return manager

    def _find_up_to_date_manager(
        self,
        inside_score=True,
        must_have_file=False,
        system=True,
        repository='git',
        ):
        import scoremanager
        abjad_library = False
        example_score_packages = False
        user_library = False
        user_score_packages = False
        if system and inside_score:
            example_score_packages = True
        elif system and not inside_score:
            abjad_library = True
        elif not system and inside_score:
            user_score_packages = True
        elif not system and not inside_score:
            user_library = True
        else:
            Exception
        asset_paths = self._list_asset_paths(
            abjad_library=abjad_library,
            example_score_packages=example_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        session = scoremanager.core.Session()
        for asset_path in asset_paths:
            manager = self._manager_class(
                path=asset_path,
                session=session,
                )
            if (repository == 'git' and
                manager._is_git_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager
            elif (repository == 'svn' and
                manager._is_svn_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager

    def _get_available_path(
        self,
        prompt_string=None,
        storehouse_path=None,
        ):
        storehouse_path = storehouse_path or self._current_storehouse_path
        while True:
            prompt_string = prompt_string or 'enter package name'
            getter = self._io_manager.make_getter()
            getter.append_space_delimited_lowercase_string(prompt_string)
            name = getter._run()
            if self._should_backtrack():
                return
            name = stringtools.to_accent_free_snake_case(name)
            path = os.path.join(storehouse_path, name)
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager.display([line, ''])
            else:
                return path

    def _get_current_directory_path(self):
        score_directory_path = self._session.current_score_directory_path
        if score_directory_path is not None:
            parts = (score_directory_path,)
            parts += self._score_storehouse_path_infix_parts
            directory_path = os.path.join(*parts)
            assert '.' not in directory_path, repr(directory_path)
            return directory_path

    def _get_file_path_ending_with(self, string):
        path = self._get_current_directory_path()
        for file_name in self._list():
            if file_name.endswith(string):
                file_path = os.path.join(path, file_name)
                return file_path

    def _get_manager(self, path):
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        return manager

    def _get_next_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory_path
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[0]
        if last_path not in paths:
            return paths[0]
        index = paths.index(last_path)
        next_index = (index + 1) % len(paths)
        next_path = paths[next_index]
        return next_path

    def _get_previous_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory_path
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[-1]
        if last_path not in paths:
            return paths[-1]
        index = paths.index(last_path)
        previous_index = (index - 1) % len(paths)
        previous_path = paths[previous_index]
        return previous_path

    def _get_sibling_asset_path(self):
        if self._session.is_navigating_to_next_asset:
            return self._get_next_asset_path()
        if self._session.is_navigating_to_previous_asset:
            return self._get_previous_asset_path()

    def _get_visible_asset_path(self, item_identifier='asset'):
        getter = self._io_manager.make_getter()
        prompt_string = 'enter {} to rename'
        prompt_string = prompt_string.format(item_identifier)
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        getter.append_menu_section_item(
            prompt_string, 
            asset_section,
            )
        numbers = getter._run()
        if self._should_backtrack():
            return
        if not len(numbers) == 1:
            return
        number = numbers[0]
        index = number - 1
        paths = [_.return_value for _ in asset_section.menu_entries]
        path = paths[index]
        return path

    def _get_visible_asset_paths(self, item_identifier='asset'):
        getter = self._io_manager.make_getter()
        plural_identifier = stringtools.pluralize(item_identifier)
        prompt_string = 'enter {} to remove'
        prompt_string = prompt_string.format(plural_identifier)
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        getter.append_menu_section_range(
            prompt_string, 
            asset_section,
            )
        numbers = getter._run()
        if self._should_backtrack():
            return
        indices = [_ - 1 for _ in numbers]
        paths = [_.return_value for _ in asset_section.menu_entries]
        paths = sequencetools.retain_elements(paths, indices)
        return paths

    def _get_visible_storehouses(self):
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        storehouses = set()
        for menu_entry in asset_section:
            path = menu_entry.return_value
            storehouse = self._configuration._path_to_storehouse(path)
            storehouses.add(storehouse)
        storehouses = list(sorted(storehouses))
        return storehouses

    def _initialize_manager(self, path):
        assert os.path.sep in path, repr(path)
        return self._manager_class(
            path=path,
            session=self._session,
            )

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry not in self._forbidden_directory_entries:
            if directory_entry[0].isalpha():
                return True
        return False

    def _list(self, public_entries_only=False):
        result = []
        path = self._get_current_directory_path()
        if not os.path.exists(path):
            return result
        if public_entries_only:
            for directory_entry in sorted(os.listdir(path)):
                if directory_entry[0].isalpha():
                    if not directory_entry.endswith('.pyc'):
                        if not directory_entry in ('test',):
                            result.append(directory_entry)
        else:
            for directory_entry in sorted(os.listdir(path)):
                if not directory_entry.startswith('.'):
                    if not directory_entry.endswith('.pyc'):
                        result.append(directory_entry)
        return result

    def _list_asset_paths(
        self,
        abjad_library=True,
        example_score_packages=True,
        user_library=True,
        user_score_packages=True,
        ):
        result = []
        directory_paths = self._list_storehouse_paths(
            abjad_library=abjad_library,
            example_score_packages=example_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        for directory_path in directory_paths:
            if not directory_path:
                continue
            if not os.path.exists(directory_path):
                continue
            directory_entries =  sorted(os.listdir(directory_path))
            for directory_entry in directory_entries:
                if not self._is_valid_directory_entry(directory_entry):
                    continue
                path = os.path.join(directory_path, directory_entry)
                result.append(path)
        return result

    def _list_storehouse_paths(
        self,
        abjad_library=True,
        example_score_packages=True,
        user_library=True,
        user_score_packages=True,
        ):
        result = []
        if (abjad_library and
            self._abjad_storehouse_path is not None):
            result.append(self._abjad_storehouse_path)
        if user_library and self._user_storehouse_path is not None:
            result.append(self._user_storehouse_path)
        if (example_score_packages and
            self._score_storehouse_path_infix_parts):
            for score_directory_path in \
                self._configuration.list_score_directory_paths(abjad=True):
                parts = [score_directory_path]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                storehouse_path = os.path.join(*parts)
                result.append(storehouse_path)
        if user_score_packages and self._score_storehouse_path_infix_parts:
            for directory_path in \
                self._configuration.list_score_directory_paths(user=True):
                parts = [directory_path]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                path = os.path.join(*parts)
                result.append(path)
        return result

    def _list_visible_asset_paths(
        self,
        abjad_library=True,
        example_score_packages=True,
        user_library=True,
        user_score_packages=True,
        ):
        visible_paths = []
        paths = self._list_asset_paths(
            abjad_library=abjad_library,
            example_score_packages=example_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        current_path = self._get_current_directory_path()
        for path in paths:
            if current_path is None or path.startswith(current_path):
                visible_paths.append(path)
        return visible_paths

    def _make_asset(self, asset_name):
        if os.path.sep in asset_name:
            asset_name = os.path.basename(asset_name)
        assert stringtools.is_snake_case(asset_name)
        path = os.path.join(
            self._current_storehouse_path,
            asset_name,
            )
        manager = self._initialize_manager(path)
        if hasattr(manager, '_write_stub'):
            manager._write_stub()
        elif hasattr(manager, 'fix'):
            manager.fix(prompt=False)

    def _make_asset_selection_breadcrumb(
        self,
        human_readable_target_name=None,
        infinitival_phrase=None,
        is_storehouse=False,
        ):
        if human_readable_target_name is None:
            name = self._manager_class.__name__
            name = stringtools.upper_camel_case_to_space_delimited_lowercase(
                name)
            human_readable_target_name = name
        if infinitival_phrase:
            return 'select {} {}:'.format(
                human_readable_target_name,
                infinitival_phrase,
                )
        elif is_storehouse:
            return 'select storehouse'
        else:
            return 'select {}:'.format(human_readable_target_name)

    def _make_asset_selection_menu(self, packages_instead_of_paths=False):
        menu = self._io_manager.make_menu(name='asset selection')
        include_extensions = getattr(self, '_include_extensions', False)
        menu_entries = self._make_asset_menu_entries(
            include_extensions=include_extensions,
            packages_instead_of_paths=packages_instead_of_paths,
            )
        menu.make_asset_section(
            menu_entries=menu_entries,
            )
        return menu

    def _make_file(
        self, 
        extension='', 
        file_name_callback=None,
        force_lowercase=True,
        prompt_string='file name', 
        ):
        from scoremanager import managers
        if self._session.is_in_score:
            path = self._get_current_directory_path()
        else:
            path = self._select_storehouse_path()
            if self._should_backtrack():
                return
            if not path:
                return
        getter = self._io_manager.make_getter()
        getter.append_string(prompt_string)
        name = getter._run()
        if self._should_backtrack():
            return
        if not name:
            return
        name = stringtools.strip_diacritics(name)
        if file_name_callback:
            name = file_name_callback(name)
        name = name.replace(' ', '_')
        if force_lowercase:
            name = name.lower()
        if not name.endswith(extension):
            name = name + extension
        path = os.path.join(path, name)
        manager = self._initialize_manager(path=path)
        manager._make_empty_asset()
        manager.edit()

    def _make_main_menu(self, name=None):
        menu = self._io_manager.make_menu(name=name)
        self._main_menu = menu
        self._make_asset_menu_section(menu)
        self._make_views_menu_section(menu)
        self._make_views_module_menu_section(menu)
        self._make_go_wrangler_menu_section(menu)
        return menu

    def _make_storehouse_menu_entries(
        self,
        abjad_library=True,
        example_score_packages=True,
        user_library=True,
        user_score_packages=True,
        ):
        from scoremanager import wranglers
        display_strings, keys = [], []
        keys.append(self._user_storehouse_path)
        display_strings.append('My {}'.format(self._breadcrumb))
        wrangler = wranglers.ScorePackageWrangler(session=self._session)
        paths = wrangler._list_asset_paths(
            abjad_library=abjad_library,
            example_score_packages=example_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        for path in paths:
            manager = wrangler._initialize_manager(path)
            display_strings.append(manager._get_title())
            path_parts = (manager._path,)
            path_parts = path_parts + self._score_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

    def _make_go_wrangler_menu_section(self, menu):
        commands = []
        commands.append(('go - clear view', 'V'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='go wrangler',
            )

    def _navigate_to_next_asset(self):
        pass

    def _navigate_to_previous_asset(self):
        pass

    def _read_view(self):
        view_name = self._read_view_name()
        if not view_name:
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    def _read_view_inventory(self):
        if self._views_module_path is None:
            return
        result = self._views_module_manager._execute(
            attribute_names=('view_inventory',),
            )
        if result == 'corrupt':
            message = 'views module is corrupt.'
            self._io_manager.display([message, ''])
            return
        if not result:
            return
        assert len(result) == 1
        view_inventory = result[0]
        return view_inventory

    def _read_view_name(self):
        if self._session.is_test:
            return
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_directory_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        if not manager:
            return
        return manager._get_metadatum(metadatum_name)

    def _remove_asset(self, item_identifier='asset', prompt=True):
        paths = self._get_visible_asset_paths(item_identifier=item_identifier)
        self._io_manager.display('')
        if not paths:
            return
        count = len(paths)
        if count == 1:
            confirmation_string = 'remove'
        else:
            confirmation_string = 'remove {}'
            confirmation_string = confirmation_string.format(count)
        prompt_string = "type {!r} to proceed"
        prompt_string = prompt_string.format(confirmation_string)
        if prompt:
            getter = self._io_manager.make_getter()
            getter.append_string(prompt_string)
            result = getter._run()
            if self._should_backtrack():
                return
            if not result == confirmation_string:
                return
        for path in paths:
            manager = self._initialize_manager(path)
            manager._remove()

    def _rename_asset(self, item_identifier='asset'):
        path = self._get_visible_asset_path(item_identifier=item_identifier)
        if not path:
            return
        self._io_manager.display('')
        manager = self._initialize_manager(path)
        manager.rename()

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context = iotools.ControllerContext(
            self,
            on_enter_callbacks=(self._enter_run,),
            )
        with context:
            while True:
                result = self._get_sibling_asset_path()
                if not result:
                    menu = self._make_main_menu()
                    result = menu._run()
                if self._should_backtrack():
                    return
                if result:
                    self._handle_main_menu_result(result)
                    if self._should_backtrack():
                        return

    def _select_asset_path(self):
        menu = self._make_asset_selection_menu()
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb()
            result = menu._run()
            if self._should_backtrack():
                return
            elif not result:
                continue
            elif result == 'user entered lone return':
                return
            else:
                break
        return result

    def _select_storehouse_path(self):
        from scoremanager import iotools
        menu_entries = self._make_storehouse_menu_entries(
            abjad_library=False,
            example_score_packages=False,
            user_library=True,
            user_score_packages=False,
            )
        selector = iotools.Selector(
            breadcrumb='storehouse',
            menu_entries=menu_entries,
            session=self._session,
            )
        result = selector._run()
        if self._should_backtrack():
            return
        return result

    def _select_view(self, infinitive_phrase=None, is_ranged=False):
        from scoremanager import managers
        view_inventory = self._read_view_inventory()
        if view_inventory is None:
            message = 'no views found.'
            self._io_manager.proceed(message)
            return
        lines = []
        view_names = view_inventory.keys()
        if is_ranged:
            breadcrumb = 'view(s)'
        else:
            breadcrumb = 'view'
        if infinitive_phrase:
            breadcrumb = '{} {}'.format(breadcrumb, infinitive_phrase)
        selector = self._io_manager.make_selector(
            breadcrumb=breadcrumb,
            is_ranged=is_ranged,
            items=view_names,
            )
        result = selector._run()
        if self._should_backtrack():
            return
        return result

    def _set_is_navigating_to_sibling_asset(self):
        message = 'implement on concrete wrangler classes.'
        raise Exception(message)

    def _write_view_inventory(self, view_inventory, prompt=True):
        lines = []
        lines.append(self._unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('from scoremanager import iotools')
        lines.append('')
        lines.append('')
        view_inventory = self._sort_ordered_dictionary(view_inventory)
        line = 'view_inventory={}'.format(format(view_inventory))
        lines.append(line)
        contents = '\n'.join(lines)
        manager = self._views_module_manager
        manager._write(contents)
        message = 'view inventory written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    ### PUBLIC METHODS ###

    def add_to_repository(self, prompt=True):
        r'''Adds assets to repository.

        Returns none.
        '''
        self._session._attempted_to_add_to_repository = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_manager(path)
            manager.add_to_repository(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def apply_view(self):
        r'''Applies view.

        Writes view name to metadata module.

        Returns none.
        '''
        infinitive_phrase = 'to apply'
        view_name = self._select_view(infinitive_phrase=infinitive_phrase)
        if self._should_backtrack():
            return
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_directory_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(metadatum_name, view_name)

    def clear_view(self):
        r'''Clears view.

        Set 'view_name' to none in metadata module.

        Returns none.
        '''
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_directory_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(metadatum_name, None)

    def commit_to_repository(self, prompt=True):
        r'''Commits assets to repository.

        Returns none.
        '''
        self._session._attempted_to_commit_to_repository = True
        if self._session.is_repository_test:
            return
        getter = self._io_manager.make_getter()
        getter.append_string('commit message')
        commit_message = getter._run()
        if self._should_backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self._io_manager.display(line)
        if not self._io_manager.confirm():
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_manager(path)
            manager.commit_to_repository(
                commit_message=commit_message,
                prompt=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def doctest(self, prompt=True):
        r'''Runs doctest.

        Returns none.
        '''
        self._current_package_manager.doctest(prompt=prompt)

    def list_views(self):
        r'''List views in views module.

        Returns none.
        '''
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            message = 'no views found.'
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True
            return
        lines = []
        names = view_inventory.keys()
        view_count = len(view_inventory)
        view_string = 'view'
        if view_count != 1:
            view_string = stringtools.pluralize(view_string)
        message = '{} {} found:'
        message = message.format(view_count, view_string)
        lines.append(message)
        lines.extend(names)
        lines.append('')
        self._io_manager.display(lines, capitalize=False)
        self._session._hide_next_redraw = True

    def make_view(self):
        r'''Makes view.

        Returns none.
        '''
        from scoremanager import iotools
        getter = self._io_manager.make_getter()
        getter.append_string('view name')
        view_name = getter._run()
        if self._should_backtrack():
            return
        menu_entries = self._make_asset_menu_entries(apply_view=False)
        display_strings = [_[0] for _ in menu_entries]
        view = iotools.View(
            items=display_strings,
            )
        breadcrumb = 'views - {} view - edit:'
        breadcrumb = breadcrumb.format(view_name)
        editor = self._io_manager.make_editor(
            breadcrumb=breadcrumb,
            target=view,
            )
        editor._run()
        if self._should_backtrack():
            return
        self._io_manager.display('')
        view = editor.target
        view_inventory = self._read_view_inventory()
        if view_inventory is None:
            view_inventory = datastructuretools.TypedOrderedDict(
                item_class=iotools.View,
                )
        view_inventory[view_name] = view
        self._write_view_inventory(view_inventory)

    def pytest(self, prompt=True):
        r'''Run pytest on visible storehouses.

        Returns none.
        '''
        assets = []
        paths = self._list_visible_asset_paths()
        for path in paths:
            if os.path.isdir(path):
                assets.append(path)
            elif os.path.isfile(path) and path.endswith('.py'):
                assets.append(path)
        if not assets:
            message = 'no testable assets found.'
            self._io_manager.display([message, ''])
        else:
            message = '{} testable assets found ...'
            message = message.format(len(assets))
            self._io_manager.display([message, ''])
            assets = ' '.join(assets)
            command = 'py.test -rf {}'.format(assets)
            self._io_manager.run_command(command)
        self._session._hide_next_redraw = True

    def remove_view(self):
        r'''Removes view from views module.

        Returns none.
        '''
        infinitive_phrase = 'to remove'
        view_names = self._select_view(
            infinitive_phrase=infinitive_phrase,
            is_ranged=True,
            )
        if self._should_backtrack():
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        for view_name in view_names:
            if view_name in view_inventory:
                del(view_inventory[view_name])
        self._write_view_inventory(view_inventory)

    def remove_views_module(self):
        r'''Removes views module.

        Returns none.
        '''
        self._current_package_manager.remove_views_module()

    def rename_view(self):
        r'''Renames view.

        Returns none.
        '''
        infinitive_phrase = 'to rename'
        old_view_name = self._select_view(infinitive_phrase=infinitive_phrase)
        if self._should_backtrack():
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        view = view_inventory.get(old_view_name)
        if not view:
            return
        getter = self._io_manager.make_getter()
        getter.append_string('view name')
        new_view_name = getter._run()
        if self._should_backtrack():
            return
        del(view_inventory[old_view_name])
        view_inventory[new_view_name] = view
        self._write_view_inventory(view_inventory)

    def repository_status(self, prompt=True):
        r'''Display asset status in repository.

        Returns none.
        '''
        self._session._attempted_repository_status = True
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        for path in paths:
            manager = self._io_manager.make_directory_manager(path)
            manager.repository_status(prompt=False)
        self._session._hide_next_redraw = True

    def revert_to_repository(self, prompt=True):
        r'''Reverts assets from repository.

        Returns none.
        '''
        self._session._attempted_to_revert_to_repository = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        for path in paths:
            manager = self._io_manager.make_directory_manager(path)
            manager.revert_to_repository(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def update_from_repository(self, prompt=True):
        r'''Updates assets from repository.

        Returns none.
        '''
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_manager(path)
            manager.update_from_repository(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def view_views_module(self):
        r'''Views views module.

        Returns none.
        '''
        self._views_module_manager.view()