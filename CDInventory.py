#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with error handling and binary data.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
#JPadilla, 2022-Nov-20, Moved appropiate functions into classes
#JPadilla, 2022-Nov-20, Created add_data function under DataProcessor class w/ DocString
#JPadilla, 2022-Nov-20, Created delete_data function under DataProcessor class w/ DocString
#JPadilla, 2022-Nov-20, Added function calls to the main code (Lines 251-253, 255, 270)
#JPadilla, 2022-Nov-27, changed description title
#JPadilla, 2022-Nov-27, combined all input functions into one function (get_inputs())
#JPadilla, 2022-Nov-27, changed read_data, and write_data to binary files using pickle syntax 
#JPadilla, 2022-Nov-27, added error handling to functions and main body of script
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

intID = '' #user input ID number
strTitle = '' #user input CD title
stArtist = '' #user input artist name

# -- PROCESSING -- #
class DataProcessor:
    """Function to process/ save / delete any data entry made by user"""

    @staticmethod
    def add_data(ID, title, artist):
        """Function that adds user input of ID, CD Title, Artist Name to a dictionary and then adds to table


        Args:
            ID: identification number for entry
            Title: user inputted CD title
            Artist: user inputted artist name


        Returns:
            None
    """
        try:
            intID = int(strID)
            dicRow = {'ID': intID, 'Title': title, 'Artist': artist}
            lstTbl.append(dicRow)
        except ValueError as e:
            print('The ID entered is NOT an integer!. \nEntry not saved - Please enter ID as an integer! \n')
            print(type(e), e, e.__doc__, sep = '\n')

    @staticmethod
    def delete_data(ID):
        """Function that finds desired entry to delete based on ID number


        Args:
            ID: identification number for entry


        Returns:
            None
        """

        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == ID:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
            if blnCDRemoved:
                print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table: the table of data (ID, CD Title, Artist name) pulled from the file 
        """
        table.clear()  # this clears existing data and allows to load data from file
        with open(file_name, 'rb') as objFile:
            table = pickle.load(objFile)
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function that writes string data to file


        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime


        Returns:
            None
        """

        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def user_inputs():
        """Function that prompts user for ID number for entry, CD title, and Artist
        Args:
            None.


        Returns:
            strID: string ID entered by user
            strTitle: string CD title entered by user
            stArtist: string Artist name entered by user
        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, stArtist


# 1. When program starts, read in the currently saved Inventory
try:
    lstTbl = FileProcessor.read_file(strFileName, lstTbl)
except FileNotFoundError as e:
    print('File not found! File has now been created.')
    print(type(e), e, e.__doc__, sep = '\n')
    FileProcessor.write_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, stArtist = IO.user_inputs()
        # 3.3.2 Add item to the table
        DataProcessor.add_data(strID, strTitle, stArtist)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            # 3.5.2 search thru table and delete CD
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            DataProcessor.delete_data(intIDDel)
            IO.show_inventory(lstTbl)
        except ValueError as e:
            print('ID entered is not an integer. Please try again.')
            print(type(e), e, e.__doc__, sep = '\n')
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




