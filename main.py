#!/usr/bin/python3
import json
import os
import subprocess as sp
try:
    from colorama import Style, Fore
except ImportError:
    install_colorama = sp.run(['pip', 'install', 'colorama'], stdout=-3)
    if install_colorama.returncode == 0:
        from colorama import Style, Fore
    # print('Install Colorama package with `pip install colorama` and then re-run the app :(')
    # quit()


def clear_terminal(*args, **kwargs):
    os.system('clear')


class Main:
    def __init__(self, json_file_dir):
        '''default `json_file_dir`: `data.json`'''

        if json_file_dir == '':
            self._json_file_dir = f"{os.path.dirname(__file__)}/data.json"
        else:
            self._json_file_dir = f"{json_file_dir}"

        try:
            with open(self._json_file_dir) as test:
                json.load(test)
        except FileNotFoundError:
            print(
                Fore.RED, f'File Does not exist!\nI will create a file named: {self._json_file_dir} ', Style.RESET_ALL)
            with open(f'{self._json_file_dir}', 'w') as newFile:
                json.dump({}, newFile)
        except json.JSONDecodeError:
            print(Fore.RED, 'The Json file is either empty, broken or not Formatted in Json.\n Try checking or reformatting the json file!')
            quit()

    def get_json_data(self) -> dict:
        with open(self._json_file_dir) as json_file_read:
            json_data = json.load(json_file_read)
        return json_data

    def append_json(self, data: dict):
        copy = self.get_json_data()
        copy.update(data)
        with open(self._json_file_dir, 'w') as file_write:
            json.dump(copy, file_write, indent=2)

    def run(self):
        action_maps = {
            'add': self.add,
            'new': self.add,

            'find': self.find,
            'view': self.find,

            'edit': self.edit,
            'change': self.edit,
            'update': self.edit,

            'remove': self.remove,
            'delete': self.remove,

            'clear': clear_terminal,

            'exit': quit,
            'quit': quit,
            'done': quit,
        }

        while True:
            action = input(
                '\t(find, add, edit, remove)\n\t\t\t_>').strip().lower()

            if action in action_maps:
                func = action_maps[action]
                if func == self.find:
                    for item, data in func().items():
                        print(item)
                        for title, value in data.items():
                            print(title, '\b:', value)
                        print('\n\n')
                else:
                    func()
            elif action == '':
                continue
            else:
                print(Fore.RED, '\n\t\tinvalid input\n', Style.RESET_ALL)
                continue

    def find(self, target='NotPassed'):
        '''target is what we look for. if not passed, we get it from user'''
        items = {}
        if target == 'NotPassed':
            target = input('-->')
        if target == '':
            return items
        elif target in ('done', 'quit', 'back', 'exit'):
            return items
        for item, data in self.get_json_data().items():  # each item and it's value in the json file that matches the target, gets added to the items variable which the function finally returns
            if target in item.lower() and target != 'all':
                items.update({item: {}})
                for title, value in data.items():
                    items[item].update({title: value})
            elif target == 'all':
                items.update({f'{item}': {}})
                for title, value in data.items():
                    items[item].update({title: value})
        return items

    def add(self):
        new_item = {}
        item_titles = []
        for i in range(5):
            if i == 0:
                if input('want to proceed?  ').strip().lower() in ('no', 'n', 'false'):
                    return None
                item_name = input('Enter new item\'s Name:')
            elif input('want to add new title?  ').strip().lower() in ('no', 'n', 'false'):
                break
            new_title = input('title name:')
            new_value = input('value: ')
            item_titles.append({new_title: new_value})
        new_item.update({item_name: {}})
        for title in item_titles:
            new_item[item_name].update(title)
        self.append_json(new_item)

    def edit(self):
        inp = input('search: ')
        result = self.find(inp)
        items = list(result.keys())
        print('--------------')
        enum_items = dict(enumerate(items, 1))

        for i, item_name in enum_items.items():
            print(i, item_name, result[item_name])

        index = int(input())
        chosen_item_name = enum_items[index]
        chosen_item_data = result[chosen_item_name]  # title: value

        print(chosen_item_name, chosen_item_data)

        enum_chosen_item_titles = dict(enumerate(chosen_item_data, 1))
        [print(i, title) for i, title in enum_chosen_item_titles.items()]

        title_index = int(input())
        chosen_title = enum_chosen_item_titles[title_index]
        chosen_value = result[chosen_item_name][chosen_title]
        print('value:', chosen_value)

        replace_with = input('replace with: ')
        result[chosen_item_name][chosen_title] = replace_with

        current_database = self.get_json_data()
        current_database.update(result)
        self.append_json(result)

    def remove(self):
        target = input('what do you want to remove? ')
        found = self.find(target)
        if len(found) == 0:
            print('Nothing Was Found')
            return
        enum_found = dict(enumerate(found, start=1))
        for index, item in enum_found.items():
            print(index, item)

        repeat = True
        while repeat:
            try:
                chosen_index = int(input('choose one:  '))
                if chosen_index not in enum_found:
                    raise ValueError
                repeat = False
            except ValueError:
                print(Fore.RED, 'Invalid Input', Style.RESET_ALL)

        print(Fore.GREEN)
        print('\n\n', enum_found[chosen_index], '\n')
        for title, value in found[enum_found[chosen_index]].items():
            print(title, '\b:', value)
            print()
        print(Style.RESET_ALL)

        print(Fore.BLUE)
        if input('DO YOU REALLY WANT TO REMOVE IT ? THIS ACTION CANNOT BE UNDONE !!!\n[y]') in ('y', ''):
            if input('write CONFIRM: ') == 'CONFIRM':
                copy = self.get_json_data()
                copy.pop(enum_found[chosen_index])
                with open(self._json_file_dir, 'w') as file_write:
                    json.dump(copy, file_write, indent=2)
                print(Fore.GREEN, 'THE ITEM GOT DELETED SUCCESSFULLY !')
            else:
                print(Fore.GREEN, 'CANCELLED !')
        else:
            print(Fore.GREEN, 'CANCELLED !')
        print(Style.RESET_ALL)


if __name__ == '__main__':
    file_path = input(
        'Enter json file\'s path: (default name : data.json)\n ==>')
    main = Main(file_path)
    main.run()
