from collections import UserDict
from datetime import datetime
import re
import pickle

records = {}


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Enter username"
        except KeyError:
            return "Contact not found"
    return inner



@user_error
def add_record(*args):
    contact_id = args[0]
    contact_num = args[1]
    records[contact_id] = contact_num
    return f"Add record {contact_id = }, {contact_id = }"


@user_error
def change_record(*args):
    contact_id = args[0]
    new_contact_id = args[1]
    rec = records[contact_id]
    if rec:
        records[contact_id] = new_contact_id
        return f"Change record {contact_id = }, {new_contact_id = }"

@user_error
def phone(contact_id):
    if contact_id in records:
        return f"{contact_id}'s phone number is {records[contact_id]}"

@user_error
def show_all():
    print(records)

@user_error
def hello():
    print("How can I help you?")

@user_error
def bye():
    return "Good bye!"

def unknown(*args):
    return "Unknown command. Try again."
        

COMMANDS = {add_record: "add record",
            change_record: "change record",
            phone: "phone",
            show_all: "show all",
            hello: "hello",
            bye: "bye",
            bye: "close",
            bye: "exit"
            }


def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown, []


def main():
    while True:
        user_input = input(">>>").lower()
        func, data = parser(user_input)
        result = (func(*data))
        print(result)
        if result == "Good bye!":
            break

filename = "Homework_12.bin"

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
        
class Birthday(Field):
    
    def __init__(self, value):
        self._value = None
        self.value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        # try:
        self._value = datetime.strptime(new_value, '%Y-%m-%d')
        # except ValueError:
        #     "wrong type of data, try like this '1990-10-26'"

    def __str__(self):
        return datetime.strftime(self.value, '%Y-%m-%d')

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return len(value) == 10 and value.isdigit()

    def __str__(self):
        return self.value

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
  
    def add_phone(self, phone):
        # if isinstance(phone, Phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                # if isinstance(new_phone, Phone):
                self.phones[i] = Phone(new_phone)
                return 
        raise ValueError("Phone number not found")  

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None 
    
    def days_to_birthday(birthday=None):
        current_date = datetime.now
        if birthday:
            period_to_birthday = birthday - current_date
        return period_to_birthday
    
    def birthday_input(birthday):
        try:
            birthday_format = "%d %m %Y" or "%d%m%Y"
            datetime.strptime(birthday, birthday_format)
            return True
        except ValueError:
            return "Not valid birth date"
    
    def phone_input(phone):
        phone_pattern = r'\d{3}\\d{3}-\d{4}'
        if re.match(phone_pattern, phone):
            return True
        else:
            return "Not valid number"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 10
        self.current_page = 1

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_page(self, page_number):
        start_index = (page_number - 1) * self.page_size
        end_index = page_number * self.page_size
        return list(self.data.values())[start_index:end_index]

    # def __iter__(self):
    #     self.current_page = 1
    #     return self

    # def __next__(self):
    #     if (self.current_page - 1) * self.page_size < len(self.data):
    #         page = self.get_page(self.current_page)
    #         self.current_page += 1
    #         return page
    #     raise StopIteration
    
    def save_addressbook(self):
        with open(self.file_name, "wb") as file:
            pickle.dump(self.data, file)
    
    def load_addressbook(self):
        try:
            with open(self.file_name, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.values())

def search_contacts(address_book, search_terms):
    match_contacts = []
    for record in address_book.values():
        if search_terms in record.name.value or any(search_terms in phone.value for phone in record.phone):
            match_contacts.append(record)
        return match_contacts

if __name__ == "__main__":
        # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")