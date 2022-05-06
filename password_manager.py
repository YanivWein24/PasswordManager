import os
import pandas as pd
from time import sleep
from mp import get_mp
from art import logo

# select a location to store all the user data:
path = r"Enter_your_path_here/services.txt"
# Set your master password in 'mp.py'. The default password is: 1234
master_pass = get_mp()


class Service:
    def __init__(self, service="", user="", passw=""):
        # we can't know the values of the parameters we'll receive when writing the constructor, so we initialize the instant
        # with empty strings and change the strings when receiving data from the user.
        # if we wont initialize the object with empty strings, we will receive an error for not
        # sending arguments for "service", "user", "passw"
        self.service = service
        self.user = user
        self.passw = passw

    def create_service(self):
        """Create attributes for a new instance of the Service"""
        self.service = input("Please enter the name of the service: ").capitalize()
        self.user = input("Please enter UserName: ")
        self.passw = input("Please enter Password: ")

    def add_user(self, path):
        """Write the login information to a txt file to permanently store the data in ROM"""
        if os.path.isfile(path):
            fh = open(path, "a")  # append if file already exists
        else:
            # create a .txt file if the passwords were deleted or the file is not found
            fh = open(path, "w")
        mytuple = (self.service, self.user, self.passw)
        if (
            str(mytuple).isascii()
            and len(mytuple[0]) > 1
            and len(mytuple[1]) >= 4
            and len(mytuple[2]) >= 4
        ):
            # checks if one or more of the attributes contains none ASCII characters.
            # also checks if the name of the server is longer than 1 (nor an empty string), and the length of 'user' and 'passw' is at least 4 characters each.
            fh.write(str(mytuple))
            fh.write("\n")
            fh.close()
            print("Service Registered Successfully! \n")
            sleep(3)

        else:
            input(
                "\nProcess Failed!\n"
                "Please use at lest 2 characters on the first field, and at least 4 characters on the other fields \n"
                "Please Use Ascii Characters Only!\n"
                "\n* Press Enter to go back to main menu "
            )


def file_exist(file):
    """check if a .txt file exists"""
    return (
        True
        if os.path.isfile(file)
        else input(
            "There are no passwords registered!\n\n* press Enter to go back to main menu\n"
        )
    )


def service_exist(file, service):
    """search if service already exists, returns boolean value. required to be called *before* creating new service"""
    if os.path.isfile(
        file
    ):  # if not then the file was probably deleted, therefore the service is no longer registered
        with open(file) as fh:
            ServiceLines = fh.readlines()
        for line in ServiceLines:
            services = line.split(", ")
            if service in services[0] and len(service) > 1:
                return True


def search_services(file, service):
    """search for a specific service, returns the Username and Password"""
    flag = 0
    with open(file) as fh:
        ServiceLines = fh.readlines()
    for line in ServiceLines:
        services = line.split(", ")
        if service in services[0] and service != "":
            print(
                f"\nFound Service: {services[0][2:-1]}\n"
                f"Username: {services[1][1:-1]}\tPassword: {services[2][1:-3]}",
            )
            input(f"\n* press Enter to go back to main menu ")
            break
        else:
            flag += 1
        if flag == len(ServiceLines):
            print("\nService not registered")
            sleep(2)
            continue


def delete_services(file):
    """deletion menu. deletes the .txt file from the memory"""
    chances = 5
    while chances > 0:
        passw = input(
            "\nTo proceed, please type again the Master Password: "
        ).capitalize()
        if passw == master_pass:
            confirm = input(
                "\nAre you sure you want to delete all the passwords?\ntype [Y] to continue: "
            ).capitalize()
            if confirm == "Y":
                os.remove(file)
                print("\n* Passwords deleted successfully!")
                sleep(2)
                break
            else:
                print("\n\t* Process Aborted *\n")
                sleep(2)
                break
        elif passw == "Q":
            print("\n\t* Process Aborted *\n")
            sleep(2)
            break
        else:
            chances -= 1
            if chances == 0:
                print("\n\tYou have used 5/5 attempts!\n\t   Process aborted!")
                sleep(5)
            else:
                print(
                    "\nPasswords Incorrect.",
                    "\nPlease try again or type Q to quit the process",
                    f"\n\n* you have {chances} more attempts *",
                )
            continue


def view(file):
    """read the lists from the file and view as a table using pandas module"""
    services, usernames, passwords = [], [], []
    with open(file) as fh:
        lines = fh.readlines()
    for line in lines:
        account_list = line.split(",")  # object is now a list of strings
        # [2:-1] removes unwanted charts
        services.append(account_list[0][2:-1])
        usernames.append(account_list[1][2:-1])
        passwords.append(account_list[2][2:-3])

    table = pd.DataFrame(
        list(zip(services, usernames, passwords)),
        columns=["Service:", "UserName:", "Password:"],
    )
    print(table)
    input(f"\n* Press Enter to go back to main menu ")


def main():
    while True:
        os.system("cls")
        msg = (
            "\nWelcome! \n\n"
            "What do you want to do?\n\n"
            "[1] Add new user and password\n"
            "[2] Check if service exists\n"
            "[3] View existing services \n"
            "[4] Delete all registered services\n"
            "[5] End Program\n\n"
            "Choose a number [1-5]: "
        )
        try:
            choose = int(input(msg))
        except:  # pressing enter before typing a number can raise an exception
            print("\n* Please enter a valid number between 1-5 *")
            sleep(3)
        else:
            print("")
            match choose:
                case 1:
                    service = Service()
                    service.create_service()
                    if service_exist(path, service.service):
                        print("Service already registered!")
                        sleep(2)
                        continue
                    service.add_user(path)
                case 2:
                    if file_exist(path):
                        service_name = input(
                            "Enter a service name to check if it is available: "
                        ).capitalize()
                        search_services(path, service_name)
                case 3:
                    if file_exist(path):
                        view(path)
                case 4:
                    if file_exist(path):
                        delete_services(path)
                case 5:
                    print("\nGoodbye!")
                    sleep(1)
                    break
                case _:  # ? used as "else"
                    print("* Please enter a valid number between 1-4 *")
                    sleep(3)


if __name__ == "__main__":
    attempts = 5
    while attempts > 0:
        password = input("Enter Master password: ").capitalize()
        if password != master_pass and password != "Q":
            attempts -= 1
            if attempts == 0:
                print("\n\tYou have used 5/5 attempts!\n\t   Access Denied!")
                continue
            else:
                print(
                    "\nYouv'e entered invalid password! \n"
                    "Please try again or type Q to exit\n"
                    f"\nYou have {attempts} more attempts"
                )
                continue
        elif password == "Q":
            print("Goodbye!")
            break
        else:
            print(logo)
            sleep(3)
            main()
            break


"""
**************************************************************
Time complexity for this project: 

The Time Complexity for the search functions is: O(n),
because each function iterates over the number of existing services.
all the other functions have constant times, so their time complexity is O(1).
the overall time complexity of this project is O(n)

The Space Complexity for this project is also: O(n)

**************************************************************
"""
