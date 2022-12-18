class Help:
    __action_commands = ["help", "contact add", "contact del", "contact edit", "contact find", "contact show", "contact birthday", "note add", "note del", "note edit", \
        "note find", "note show", "note edit tag", "note show by tag", "note find by tag", "sort file"]
    __exit_commands = ["good bye", "close", "exit"]
    __commands_description = ["Returns the list of available CLI commands", "Adding the Contact to the AddressBook", \
        "Deleting the Contact", "Editing the Contact", "Finding the Contact", "Show all Contacts", "Returns the list of Contact with the birthdays within the requested period", \
            "Adding the Note to the Notebook", "Deleting the Note", "Editing the text of the Note", "Search for the Note", \
        "Displays all Notes", "Changing the Tag", "Returns the list of Notes by Tag", \
            "Searching the Note by Tag", "Sorting the files in a specified directory" , "Exits the program"]

    def __init__(self):
        self.__commands_desc = [f"<<{cmd}>> - {desc}" for cmd, desc in zip(self.__action_commands + [', '.join(self.__exit_commands)], self.__commands_description)]

    def show(self):
        result = ''
        for i in self.__commands_desc:
            result += i + '\n'
        return result

    'hello',
    'close',
    '',
    'exit',

    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',


    '',

    'contact find',
    'contact show',

    '',

    '',
