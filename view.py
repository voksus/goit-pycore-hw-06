import os
import random as rnd
from model import MESSAGES, ModelError, AddressBook, Record

# ============================ КОНСТАНТИ ТА СЛОВНИК ПОВІДОМЛЕНЬ ============================

class Colors:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    BLUE   = '\033[94m'
    BOLD   = '\033[1m'
    END    = '\033[0m'

MESSAGES = {
    # Помилки
    "INVALID_PHONE"      : f"{Colors.RED}Невірний формат номера: {{phone}}{Colors.RED}. Має бути 10 цифр.{Colors.END}",
    "INVALID_EMAIL"      : f"{Colors.RED}Невірний формат email: {{email}}{Colors.RED}.{Colors.END}",
    "INVALID_NAME"       : f"{Colors.RED}Некоректне ім’я {{name}}{Colors.RED}. Лише літери, апостроф, дефіс дозволено.",
    "CONTACT_EXISTS"     : f"{Colors.YELLOW}Контакт з іменем {{name}}{Colors.YELLOW} вже існує.{Colors.END}",
    "CONTACT_NOT_FOUND"  : f"{Colors.YELLOW}Контакт з іменем {{name}}{Colors.YELLOW} не знайдено.{Colors.END}",
    "PHONE_NOT_FOUND"    : f"{Colors.YELLOW}Номер {{phone}}{Colors.YELLOW} не знайдено у контакту {{name}}{Colors.YELLOW}.{Colors.END}",
    "EMAIL_NOT_FOUND"    : f"{Colors.YELLOW}Email {{email}}{Colors.YELLOW} не знайдено у контакту {{name}}{Colors.YELLOW}.{Colors.END}",
    "DUPLICATE_PHONE"    : f"{Colors.YELLOW}Номер {{phone}}{Colors.YELLOW} вже існує у контакту {{name}}{Colors.YELLOW}.{Colors.END}",
    "DUPLICATE_EMAIL"    : f"{Colors.YELLOW}Email {{email}}{Colors.YELLOW} вже існує у контакту {{name}}{Colors.YELLOW}.{Colors.END}",
    "EMPTY_CONTACTS"     : f"{Colors.BLUE}У книзі контактів немає жодного запису.{Colors.END}",
    "INVALID_INDEX"      : f"{Colors.RED}Вказано недійсний індекс: {{index}}{Colors.RED}.{Colors.END}",
    "EMPTY_RECORD"       : f"{Colors.BLUE}Контакт {{name}}{Colors.BLUE} не містить телефонів чи email.{Colors.END}",

    # 🟢 Інформаційні повідомлення
    "CONTACT_ADDED"      : f"{Colors.GREEN}Контакт {{name}}{Colors.GREEN} додано до адресної книги.",
    "CONTACT_CHANGED"    : f"{Colors.GREEN}Контакт {{name}}{Colors.GREEN} оновлено. Новий номер: {{phone}}{Colors.GREEN}.{Colors.END}",
    "CONTACT_DELETED"    : f"{Colors.GREEN}Контакт {{name}}{Colors.GREEN} успішно видалено.{Colors.END}",

    # ✅ Успішні операціїf
    "PHONE_ADDED"        : f"Номер {{phone}} додано до контакту {{name}}.",
    "EMAIL_ADDED"        : f"Email {{email}} додано до контакту {{name}}.",
    "PHONE_CHANGED"      : f"Номер під індексом {{index}} для контакту {{name}} замінено на {{phone}}.",
    "EMAIL_CHANGED"      : f"Email під індексом {{index}} для контакту {{name}} замінено на {{email}}.",
    "PHONE_DELETED"      : f"Номер під індексом {{index}} для контакту {{name}} видалено.",
    "EMAIL_DELETED"      : f"Email під індексом {{index}} для контакту {{name}} видалено.",

    # ℹ️ Системні
    "COMMAND_PROMPT"     : "Введіть команду: ",
    "UNKNOWN_COMMAND"    : f"{Colors.YELLOW}Невідома команда: {{cmd}}{Colors.YELLOW}. Спробуйте ще раз.{Colors.END}",
    "GOODBYE_MESSAGE"    : f"{Colors.GREEN}До побачення 👋{Colors.END}",
}
hello_options = (
        'Привіт! Чим можу допомогти?', 'Вітаю! Я тут, щоб допомогти.', 'Добрий день! Я до ваших послуг.',
        'Привіт, як справи?', 'Гей, як ся маєш?', 'Привіт-привіт! Що треба? 😉', 'Гей! Чекаю на твої команди.',
        'Йо! Що сьогодні робимо?', 'О, привітулі!', 'Слухаю уважно 🤖', 'Чим можу допомогти, друже?',
        'Вітаю! Як можу бути корисним?', 'Добрий день! Що вас цікавить?', 'Ласкаво прошу! Чим можу допомогти?',
        'Сервіс активовано. Що вам потрібно?', 'Біп-буп! Робобот до ваших послуг! 🤖',
        'Завантаження ввічливості... 100% – Привіт!', 'Хтось викликав штучний інтелект? 👀',
        'Привіт, людська істото! Що потрібно?', 'Хей! Давай працювати! 🚀', 'Здоровенькі були! Що треба?',
        'Поїхали! Я готовий до роботи!', 'Готовий до виклику! Що потрібно?', 'Я тут! Почнімо.',
        'Адресна книга відкрита! Що робимо?', 'Запити приймаються! Чим допомогти?',
        'Когось шукаємо? Я готовий!', 'Контакти? Команди? Що цікавить?', 'Починаємо роботу. Введіть команду.'
    )

# ============================ БАЗОВІ МЕТОДИ ============================

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def say_hello():
    print(hello_options[rnd.randint(0, len(hello_options) - 1)])

# ============================ МЕТОДИ ВЗАЄМОДІЇ ============================

def ask() -> str:
    return input(MESSAGES["COMMAND_PROMPT"])

def info(key: str, **kwargs) -> None:
    print(MESSAGES[key].format(**kwargs))

def success(key: str, **kwargs) -> None:
    print(MESSAGES[key].format(**kwargs))

def warn(key: str, **kwargs) -> None:
    print(MESSAGES[key].format(**kwargs))

def error(key: str, **kwargs) -> None:
    print(MESSAGES[key].format(**kwargs))

# ============================ СПЕЦИФІЧНІ МЕТОДИ ВІДОБРАЖЕННЯ ============================

def contact_added(name: str, phone: str) -> None:
    success("CONTACT_ADDED", name=name)

def contact_changed(name: str, phone: str) -> None:
    success("CONTACT_CHANGED", name=name, phone=phone)

def contact_deleted(name: str) -> None:
    success("CONTACT_DELETED", name=name)

def contact_found(record: Record) -> None:
    phones = "; ".join(f"[{idx}] {p.value}" for idx, p in record.phones.items())
    emails = "; ".join(f"[{idx}] {e.value}" for idx, e in record.emails.items())
    if not phones and not emails:
        info("EMPTY_RECORD", name=record.name.value)
        return
    print(f"Інформація про контакт {Colors.BOLD}{record.name.value}:{Colors.END}")
    if phones:
        print(f" Телефони: {phones}")
    if emails:
        print(f" Email: {emails}")

def contacts_not_found() -> None:
    warn("EMPTY_CONTACTS")

def show_all_contacts(book: AddressBook) -> None:
    print("Усі збережені контакти:")
    contacts = book.data.values()
    for record in contacts:
        contact_found(record)
    print(f"Кількість осіб в контактах: {str(len(contacts))}")

def unknown_command(cmd: str) -> None:
    warn("UNKNOWN_COMMAND", cmd=cmd)

def show_help() -> None:
    print(f"{Colors.BOLD}Список команд:{Colors.END}")
    print("  add <name> <phone>          - Додати новий контакт.")
    print("  change <name> p.<i> <phone> - Змінити номер контакту за індексом.")
    print("  change <name> e.<i> <phone> - Змінити emial контакту за індексом.")
    print("  remove <name>               - Видалити контакт.")
    print("  phone <name>                - Показати дані контакту за ім'ям.")
    print("  all                         - Показати всі контакти.")
    print("  clrscr                      - Очистити екран.")
    print("  ?                           - Показати цю довідку.")
