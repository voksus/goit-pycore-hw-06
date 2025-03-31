import json
from collections import UserDict
from enum import Enum
import re

# ============================= ENUMS ТА КОНСТАНТИ =============================

class ModelError(Enum):
    INVALID_PHONE        = "INVALID_PHONE"
    INVALID_EMAIL        = "INVALID_EMAIL"
    INVALID_NAME         = "INVALID_NAME"
    CONTACT_EXISTS       = "CONTACT_EXISTS"
    CONTACT_NOT_FOUND    = "CONTACT_NOT_FOUND"
    DUPLICATE_PHONE      = "DUPLICATE_PHONE"
    DUPLICATE_EMAIL      = "DUPLICATE_EMAIL"
    PHONE_NOT_FOUND      = "PHONE_NOT_FOUND"
    EMAIL_NOT_FOUND      = "EMAIL_NOT_FOUND"
    EMPTY_CONTACTS       = "EMPTY_CONTACTS"
    INVALID_INDEX        = "INVALID_INDEX"
    EMPTY_CONTACT_FIELDS = "EMPTY_CONTACT_FIELDS"

MESSAGES = {
    # 🔴 Помилки валідації
    ModelError.INVALID_PHONE        : "Некоректний формат телефону {phone} (має бути 10 цифр).",
    ModelError.INVALID_EMAIL        : "Некоректний формат email-адреси {email}.",
    ModelError.INVALID_NAME         : "Некоректне ім’я {name}. Лише літери, апостроф та пробіли дозволено.",
    ModelError.CONTACT_EXISTS       : "Контакт з іменем {name} вже існує.",

    # 🟡 Помилки дублікатів
    ModelError.CONTACT_NOT_FOUND    : "Контакт з іменем {name} не знайдено.",
    ModelError.DUPLICATE_PHONE      : "Телефон {phone} вже існує у записі {name}.",
    ModelError.DUPLICATE_EMAIL      : "Email {email} вже існує у записі {name}.",

    # ⚠️ Помилки пошуку
    ModelError.PHONE_NOT_FOUND      : "Телефон з індексом {index} не знайдено у записі {name}.",
    ModelError.EMAIL_NOT_FOUND      : "Email з індексом {index} не знайдено у записі {name}.",
    ModelError.EMPTY_CONTACTS       : "У книзі контактів немає жодного запису.",
    ModelError.INVALID_INDEX        : "Вказано недійсний індекс: {index}.",
    ModelError.EMPTY_CONTACT_FIELDS : "Контакт {name} не має телефонів чи імейлів.",
}

# ============================= КЛАСИ ДАНИХ =============================

class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

class Name(Field):
    @staticmethod
    def validate(name: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-zА-Яа-яІіЇїЄєҐґ'-]{1,50}", name))

class Phone(Field):
    @staticmethod
    def validate(phone: str) -> bool:
        return bool(re.fullmatch(r"\d{10}", phone))

class Email(Field):
    @staticmethod
    def validate(email: str) -> bool:
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}$", email, re.I))

# ============================= ЗАПИС КОНТАКТУ =============================

class Record:
    def __init__(self, name: str) -> None:
        if not Name.validate(name):
            raise ValueError(MESSAGES[ModelError.INVALID_NAME].format(name=name))
        self.name: Name = Name(name)
        self.phones: dict[int, Phone] = {}
        self.emails: dict[int, Email] = {}

    def add_phone(self, phone: str) -> ModelError | None:
        if not Phone.validate(phone):
            return ModelError.INVALID_PHONE
        if any(p.value == phone for p in self.phones.values()):
            return ModelError.DUPLICATE_PHONE
        self.phones[len(self.phones)] = Phone(phone)

    def edit_phone(self, index: int, new_phone: str) -> ModelError | None:
        if index not in self.phones:
            return ModelError.INVALID_INDEX
        if not Phone.validate(new_phone):
            return ModelError.INVALID_PHONE
        self.phones[index] = Phone(new_phone)

    def remove_phone(self, index: int) -> ModelError | None:
        if index not in self.phones:
            return ModelError.INVALID_INDEX
        del self.phones[index]
        self.phones = {i: p for i, p in enumerate(self.phones.values())}

    def add_email(self, email: str) -> ModelError | None:
        if not Email.validate(email):
            return ModelError.INVALID_EMAIL
        if any(e.value == email for e in self.emails.values()):
            return ModelError.DUPLICATE_EMAIL
        self.emails[len(self.emails)] = Email(email)

    def edit_email(self, index: int, new_email: str) -> ModelError | None:
        if index not in self.emails:
            return ModelError.INVALID_INDEX
        if not Email.validate(new_email):
            return ModelError.INVALID_EMAIL
        self.emails[index] = Email(new_email)

    def remove_email(self, index: int) -> ModelError | None:
        if index not in self.emails:
            return ModelError.INVALID_INDEX
        del self.emails[index]
        self.emails = {i: e for i, e in enumerate(self.emails.values())}

# ============================= АДРЕСНА КНИГА =============================

class AddressBook(UserDict):
    def add_record(self, record: Record) -> ModelError | None:
        if record.name.value in self.data:
            return ModelError.CONTACT_EXISTS
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | ModelError:
        if name not in self.data:
            return ModelError.CONTACT_NOT_FOUND
        return self.data[name]

    def delete(self, name: str) -> ModelError | None:
        if name not in self.data:
            return ModelError.CONTACT_NOT_FOUND
        del self.data[name]

# ============================= СЕРІАЛІЗАЦІЯ =============================

def save_contacts(book: AddressBook, filename: str = "contacts.json") -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump({
            name: {
                "phones": [phone.value for phone in record.phones.values()],
                "emails": [email.value for email in record.emails.values()]
            }
            for name, record in book.data.items()
        }, file, indent=4, ensure_ascii=False)

def load_contacts(filename: str = "contacts.json") -> AddressBook:
    book = AddressBook()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            for name, entry in data.items():
                record = Record(name)
                for phone in entry.get("phones", []):
                    record.add_phone(phone)
                for email in entry.get("emails", []):
                    record.add_email(email)
                book.add_record(record)
    except FileNotFoundError:
        pass
    return book
