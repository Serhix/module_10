from collections import UserDict


class AddressBook(UserDict):    # Наслідується від UserDict, словник з полями name, phone....
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_record_from_book(self, name):
        for record in self.data.values():
            if record.name.value.lower() == name.lower():
                return record
        return None
        
class Record:                   # Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name.
  
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)
                break

    def change_phone(self, phone, new_phone):
        for i in self.phones:
            if i.value == phone:
                i.value = new_phone
                break
    
    
    

class Field:                    # Батьківський для всіх полів, у ньому потім реалізуємо логіку, загальну для всіх полів.
    def __init__(self, value):
        self.value = value

class Name(Field):              # Обов'язкове поле з ім'ям
    pass
    


class Phone(Field):             # Необов'язкове поле з телефоном та таких один запис (Record) може містити кілька.
    pass
            

# блок функцій з модуля 9(змінено)


def input_error(func):
    
    def wrapper(*args):        
        try:
            return func(*args)
        except KeyError:
            return "KeyError, maybe contact list is empty"
        except (ValueError, IndexError, AttributeError):
            return "Enter the correct command!!!"

    return wrapper


def add(name, phone):                                    # додаємо новий номер до адресної книги(до існуючого або нового контакту)
    record = phone_dict.get_record_from_book(name)
    if not record:
        record = Record(name)
    record.add(phone)
    phone_dict.add_record(record)
    return 'Number added!'


def change(name, phone, new_phone):                     # міняємо номер phone на new_phone для контакту name
    record = phone_dict.get_record_from_book(name)
    if not record:
        return f'Contact with name {name} not found'
    record.change_phone(phone, new_phone)
    phone_dict.add_record(record)
    return f'The number {phone} has been changed to {new_phone} for contact {name}!'

def delete(name, phone):                                # видаляємо номер phone для контакту name
    record = phone_dict.get_record_from_book(name)
    if not record:
        return f'Contact with name {name} not found'
    record.delete_phone(phone)
    phone_dict.add_record(record)
    return f'The number {phone} has been delete for contact {name}!'

def show(name):                                # пошук по name
    record = phone_dict.get_record_from_book(name)
    # if not record:
    #     return f'Contact with name {name} not found'
    return f'The contact {name} has the following phone numbers {", ".join(j.value for j in record.phones)}!'

def show_all():                                 #вивід всієї книги
    if not phone_dict.data: 
        return 'Maybe namber list is empty!'
    else:
        print('Contact list:')
        result = []
        for i in phone_dict.data.values():
            result.append(f'name: {i.name.value}, phone: {", ".join(j.value for j in i.phones)}') 
        return '\n'.join(result)
        

def sanitize_phone(phone):
    new_phone = (
        phone.removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
    )
    return new_phone

@input_error
def choise_comand(request):

    request_split = request.split()
    if request_split[0] == 'hello':                                
        return 'How can I help you?'
    elif request_split[0] == 'show' and request_split[1] == 'all':  # виводить всю книгу    
        return show_all()
    elif request_split[0] == 'show': # пошук за номером
        return show(request_split[1])
    elif request_split[0] == 'add' and sanitize_phone(request_split[2]).isdigit():      
        return add(request_split[1], sanitize_phone(request_split[2]))
    elif request_split[0] == 'change' and sanitize_phone(request_split[2]).isdigit() and sanitize_phone(request_split[3]).isdigit(): 
        return change(request_split[1], sanitize_phone(request_split[2]), sanitize_phone(request_split[3]))
    elif request_split[0] == 'delete' and sanitize_phone(request_split[2]).isdigit(): #
        return delete(request_split[1], sanitize_phone(request_split[2]))
    elif request_split[0] == 'good' and request_split[0] == 'bye' or request_split[0] in ['close', 'exit']: #
        return 'Good bye!'
    else:
        return "Enter the correct command!!!" 


def main():
    while True:
        request = input('- ').lower()
        result = choise_comand(request)
        print(result)
        if result == 'Good bye!':
            break


if __name__ == '__main__':
    phone_dict = AddressBook()
    main()
