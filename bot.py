from classes import AddressBook, Record


address_book = AddressBook()
filename = "Homework_12.bin"


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
    contact_name = args[0]
    contact_num = args[1]
    record = Record(contact_name)
    record.add_phone(contact_num)
    address_book.add_record(record)
    return f"Додано запис {contact_name}, {contact_num}"


@user_error
def change_record(*args):
    contact_name = args[0]
    new_contact_name = args[1]
    record = address_book.find(contact_name)
    if record:
        record.name.value = new_contact_name
        return f"Змінено запис {contact_name}, {new_contact_name}"


@user_error
def phone(contact_name):
    record = address_book.find(contact_name)
    if record:
        return f"Номер телефону {contact_name}: {', '.join(p.value for p in record.phones)}"


@user_error
def show_all():
    for record in address_book.data.values():
        print(record)


def unknown(*args):
    return "Unknown command"


# Define a dictionary of commands and their corresponding functions
COMMANDS = {
    add_record: "додати запис",
    change_record: "змінити запис",
    phone: "телефон",
    show_all: "показати всі"
    }


def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown, []


def main():
    address_book.load_addressbook(filename)
    while True:
        user_input = input(">>>").lower()
        func, data = parser(user_input)
        result = func(*data)
        print(result)
        if result == "Прощавай!":
            address_book.save_addressbook(filename)
            break


if __name__ == '__main__':
    main()
    