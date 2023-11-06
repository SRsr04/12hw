from classes import AddressBook, Record

records = AddressBook()


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
    records.add_record(Record(contact_id, phone=contact_num))
    return f"Add record {contact_id = }, {contact_num = }"


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
def show_all(*args):
    return records

@user_error
def hello(*args):
    print("How can I help you?")

@user_error
def bye(*args):
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
        
        
if __name__ == '__main__':
    main()