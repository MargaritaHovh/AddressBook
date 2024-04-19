import time
import json
import re

class ContactDescriptor:
    """Descriptor for managing contact attributes."""
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance , owner):
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            raise AttributeError(f"'{owner.__name__}' object has no attribute '{self.name}'")
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value



class Contact:
    """Class representing a contact."""


    name = ContactDescriptor()
    phone_number = ContactDescriptor()
    email = ContactDescriptor()
    birthday = ContactDescriptor()

    def __init__(self, name, phone_number, email, birthday ):
        """Initialize the contact with name, phone_number, email, and birthday."""
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.birthday = birthday
        self.contact_dict = {
            'name': name,
            'phone_number': phone_number,
            'email': email,
            'birthday': birthday
        }



class AddressBook:
    """Class representing an address book."""
    def __init__(self, name):
        """Initialize the address book with a name and an empty list of contacts."""
        self.name = name
        self.contacts = []
    
    def add(self):
        """Add a new contact to the address book."""
        while True:
            name = input("Enter the contact's name: ")
            try:
                # Perform name validation (basic empty/whitespace check)
                if not name.strip():
                    raise ValueError("Name cannot be empty or contain only whitespace")
                break
            except ValueError as e:
                print(f"Invalid name: {e}")

        while True:
            phone_number = input("Enter the contact's phone number: ")
            try:
                # Validate phone_number format (only digits and dashes allowed)
                if not re.match(r'^[\d-]+$', phone_number):
                    raise ValueError("Invalid phone number format")
                break
            except ValueError as e:
                print(f"Invalid phone number: {e}")

        while True:
            email = input("Enter the contact's email: ")
            try:
                # Validate email format
                if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
                    raise ValueError("Invalid email format")
                break
            except ValueError as e:
                print(f"Invalid email: {e}")

        while True:
            birthday = input("Enter the contact's birthday: ")
            try:
                # Validate birthday format (let's assume YYYY-MM-DD)
                time.strptime(birthday, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid birthday format, use YYYY-MM-DD")

        contact = Contact(name, phone_number, email, birthday)
        self.contacts.append(contact)

    def search(self, criteria):
        """Search for contacts that match the given criteria and print the results."""
        found_contacts = []
        for contact in self.contacts:
            for key, value in contact.contact_dict.items():
                if criteria.lower() in value.lower():
                    found_contacts.append(contact)
                    break
                    
        if found_contacts:
            print("Matching contacts:")
            for contact in found_contacts:
                print(f"Name: {contact.contact_dict['name']}, "
                  f"Phone: {contact.contact_dict['phone_number']}, "
                  f"Email: {contact.contact_dict['email']}, "
                  f"Birthday: {contact.contact_dict['birthday']}")
                
        else:
            print("No contacts found matching the criteria.")

    def update(self, contact_detail):
        """Update the value of the given contact detail for selected contacts."""
        updated_contacts = []
        matching_contacts = []         #We create this list because contacts can have the same name or birthday                
        

        for contact in self.contacts:
            for key, value in contact.contact_dict.items():
                if contact_detail.lower() == value.lower():
                    matching_contacts.append(contact)
                    break

        if matching_contacts:
            print("Matching contacts:")
            for index, contact in enumerate(matching_contacts, 1):  
                print(f"{index} - {contact.contact_dict}")
        else:
            print("No contacts found matching the criteria.")


        while True:
            choice = input("Please select the contact number whose detail you want to change ")
            if choice.isnumeric():
                choice = int(choice)
                if 1 <= choice <= len(matching_contacts):
                    selected_contact = matching_contacts[choice - 1]
                    new_detail = input(f"Now enter new value for contact detail: ")
                    answer = input(f"Are you sure you want to change the contact's value?\nPlease answer YES or NO: ")

                    if answer.upper() == "YES":
                        for key in selected_contact.contact_dict.keys():
                            if selected_contact.contact_dict[key].lower() == contact_detail.lower():
                                selected_contact.contact_dict[key] = new_detail
                                break
                        updated_contacts.append(selected_contact)
                        print(f"Contact's detail '{contact_detail}' updated successfully.")
                    elif answer.upper() == "NO":
                        print("We will not update your data")
                    else:
                        print("Invalid input, please try again")
                    break
                else:
                    print("Invalid value. Please try again.")
            else:
                print("Invalid input. Please enter a number.")


    def delete(self, contact_detail):
        """Delete contacts based on the given contact detail."""
        deleted_contacts = []
        matching_contacts = []

        for contact in self.contacts:
            for key, value in contact.contact_dict.items():
                if contact_detail.lower() == value.lower():
                    matching_contacts.append(contact)
                    break

        if matching_contacts:
            print("Matching contacts:")
            for index, contact in enumerate(matching_contacts, 1):  
                print(f"{index} - {contact.contact_dict}")
        
        else:
            print("No contacts found matching the criteria.")


        while True:
            choice = input("Please select the contact number whose you want to delete ")
            if choice.isnumeric():
                choice = int(choice)
                if 1 <= choice <= len(matching_contacts):
                    selected_contact = matching_contacts[choice - 1]
                    self.contacts.remove(selected_contact)
                    deleted_contacts.append(selected_contact)
                    print(f"Contact deleted successfully.")
                    break
                            
                else:
                    print("Invalid value. Please try again.")
            else:
                print("Invalid input. Please enter a number.")
        
    


def create_address_book():
    name = input("Enter the name for the new address book: ")
    address_book = AddressBook(name)
    address_books.append(address_book)
    print(f"Address book '{name}' created successfully!")


def choose_address_book():
    print("Choose an address book")
    for index, address_book in enumerate(address_books, 1):
        print(f"{index} - {address_book.name}")

    choice = input("Enter the number of the address book you want to use: ")
    try:
        choice = int(choice)
        if 1<= choice <=len(address_books):
            return address_books[choice - 1]
        else:
            print("Invalid choice. Using the first address book.")
            return address_books[0]
        
    except ValueError:
        print("Invalid input. Using the first address book.")
        return address_books[0]
    

def save_to_file(address_book, filename):
    data = {
        "Contacts": [contact.contact_dict for contact in address_book.contacts]
    }
    with open(filename, "w") as file:
        json.dump(data, file)
    print(f"Address book saved to {filename} successfully")


def load_from_file(address_book, filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            contacts_data = data.get("Contacts", [])
            address_book.contacts = [Contact(**contact_data) for contact_data in contacts_data]
            print("Address book loaded successfully.")
    except FileNotFoundError:
        print("File not found. Unable to load address book.")
    except Exception as e:
        print(f"Error occurred while loading the address book: {e}")
        

def start():
    global address_books
    address_books = []
    actions = ["1 - Create Address Book", "2 - Choose Address Book", "3 - Add contact", "4 - Search contact", "5 - Update contact", "6 - Delete contact", "7 - Save Address Book to file", "8 - Load Address Book from file", "9 - Exit"]
    
    while True:
        time.sleep(1)
        for action in actions:
            print(action)

        action = input("Choose the action you want: ")

        if action == "1":
            create_address_book()

        elif action == "2":
            address_book = choose_address_book()
            print(f"Using address book: {address_book.name}")

        elif action == "3":
            address_book.add()

        elif action == "4":
            criteria = input("Enter the search criteria: ")
            address_book.search(criteria)

        elif action == "5":
            contact_detail = input("Enter the detail's value you want to update:")
            address_book.update(contact_detail)

        elif action == "6":
            contact_detail = input("You can enter any contact detail and delete the contact according to that detail: ")
            address_book.delete(contact_detail)

        elif action == "7":
            filename = input("Enter file name for saving Address Book to file: ")
            save_to_file(address_book, filename)

        elif action == "8":
            filename = input("Enter file name for loading Address Book from file: ")
            load_from_file(address_book, filename)
        
        elif action == "9":
            break
            
        else:
            print("Invalid action. Please choose a vaild action")



if __name__ == "__main__":
    start()

