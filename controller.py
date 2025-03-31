import view as v
import model as mdl
from functools import wraps
from model import MESSAGES, ModelError, AddressBook, Record

contacts: AddressBook = mdl.load_contacts()

def input_error(func):
    '''Декоратор для обробки помилок взаємодії з користувачем'''
    @wraps(func)
    def wrapper(*args, **kwargs: AddressBook | dict):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, ModelError):
                v.error(MESSAGES[result].format(**kwargs))
                return False
            return result
        except KeyError:
            v.error("Вказане ім’я не знайдено в списку контактів.")
        except ValueError as e:
            v.error(str(e))
        except IndexError:
            v.error("Команда введена без необхідних аргументів.")
        return False
    return wrapper

def parse_input(cmd: str) -> tuple[str, list[str]]:
    '''Розділяє введену команду на ключове слово і список аргументів'''
    parts = cmd.split()
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    return command, args

def get_cmd() -> str:
    '''Отримання команди через view'''
    return v.ask().strip()

def hello():
    '''Привітання користувача'''
    v.say_hello()

def quit(*_, kwargs):
    '''Завершення роботи програми'''
    v.info("GOODBYE_MESSAGE")
    exit(0)

@input_error
def add_contact(args: list[str], kwargs):
    '''Додавання нового контакту'''
    name, phone = args
    record = Record(name)
    error = record.add_phone(phone)
    if error:
        return error
    error = contacts.add_record(record)
    if error:
        return error
    v.contact_added(name, phone)
    mdl.save_contacts(contacts)
    return True

@input_error
def change_contact(args: list[str], kwargs):
    '''Зміна номера телефону контакту за індексом'''
    name, index, new_phone = args
    record = contacts.find(name)
    if isinstance(record, ModelError):
        return record
    idx = int(index.split(".")[1])
    error = record.edit_phone(idx, new_phone)
    if error:
        return error
    v.contact_changed(name, new_phone)
    mdl.save_contacts(contacts)
    return True

@input_error
def remove_contact(args: list[str], kwargs):
    '''Видалення контакту'''
    name = args[0]
    error = contacts.delete(name)
    if error:
        return error
    v.contact_deleted(name)
    mdl.save_contacts(contacts)
    return True

@input_error
def show_contact(args: list[str], kwargs):
    '''Показати контакт за ім'ям'''
    name = args[0]
    record = contacts.find(name)
    if isinstance(record, ModelError):
        return record
    v.contact_found(record)
    return True

def show_all_contacts():
    '''Показати всі контакти'''
    if not contacts.data:
        v.contacts_not_found()
        return False
    v.show_all_contacts(contacts)
    return True

def help():
    '''Показати довідку'''
    v.show_help()
    return False

def unknown_command(cmd: str):
    '''Обробка невідомої команди'''
    v.unknown_command(cmd)

COMMANDS = {
    'hi'     : hello,
    'hello'  : hello,
    'привіт' : hello,
    'quit'   : quit,
    'exit'   : quit,
    'close'  : quit,
    'add'    : add_contact,
    'change' : change_contact,
    'remove' : remove_contact,
    'phone'  : show_contact,
    'all'    : show_all_contacts,
    'clrscr' : v.clear_screen,
    '?'      : help
}

def execute(command: str, args: list[str], contacts: AddressBook):
    '''Виконання команди з аргументами'''
    handler = COMMANDS.get(command)
    if handler:
        was_changed = handler(args, kwargs=contacts)
        if command in ('add', 'change', 'remove') and was_changed:
            mdl.save_contacts(contacts)
    else:
        unknown_command(command)
