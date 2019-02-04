import abc
from DBInterface import *
from abc import ABC

# These Functions will be used automaticall by the server so all the code
# needed for a Function must be implemented here
# If the server has to send an answer, the functions needs to return 
# an array containing those Messages

# NEEDS TO BE FIRST FUNCTION!
class TCP_function(ABC):
    ident = ''                  # Entry in first Field used to identify Function
    fields = 0                  # Amount of Fields after first Field
    hostNeeded = False          # Only executable by Host
    DB = None

    def __init__(self, DB):             # Create DB Connection
        self.DB = DB

    @abc.abstractmethod
    def run(self,raw_data):          # initiate data handling
        pass

    def get_ident(self):            # return ident for comparison
        return self.ident

    def check_host(self):           # always activated, compares user to hostNeeded
        # DOTO: Check if User is Host
        return True

    


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ! ADD FUNCTIONS STARTING HERE !
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class TCP_HostAuthentication(TCP_function):
    ident = 'HA'
    answerIdent = 'AA'

    fields = 2                  # hostPW, MAC
    hostNeeded = False
    hostPW = '1231'
    
    def run(self,data):
        # More fields than necessary DOTO: handling
        if len(data) != self.fields:
            i = 1
        # Check if host pw correct
        if data[0] == self.hostPW:
            # Add Host
            Mac = data[1]
            ID = self.DB.new_user(Mac)
        else:
            ID = 0

        # Return Message
        MSG = '{}#{}'.format(self.answerIdent, ID)
        return MSG

class TCP_UserAuthentication(TCP_function):
    ident = 'UA'
    answerIdent = 'AA'

    fields = 1          # MAC
    hostNeeded = False

    def run(self,data):
        
        # More fields than necessary DOTO: handling
        if len(data) != self.fields:
            i = 1

        # Check if Host exists
        Host = self.DB.get_user(1)

        if Host == 1:
            # Add Host to Users
            ID = self.DB.new_user(data[0])
        else:
            # No Host, return Error
            ID = 0
        
        # Return Message
        MSG = '{}#{}'.format(self.answerIdent, ID)
        return MSG

class TCP_FetchPlaylist(TCP_function):
    ident = 'PR'
    answerIdentSignal = 'PS'
    answerIdentEntry = 'PE'

    fields = 1
    hostNeeded = False

    def run(self, data):
       # More fields than necessary DOTO: handling
        if len(data) != self.fields:
            i = 1
        MSG = []
        
        if data[0] == '1':
            Songs = self.DB.get_playlist()
            MSG.append(self.answerIdentSignal + '#1')

            # 0: ID
            # 1: CurPoints
            # 2: Name
            # 3: Interpret

            for s in Songs:
                MSG.append('{}#{}#{}#{}#{}'.format(self.answerIdentEntry, s['ID'], s['CurPoints'], s['Name'], s['Interpret']) + "\n")
            MSG.append(self.answerIdentSignal + '#0')

        return MSG

class TCP_SearchSong(TCP_function):
    ident = 'SS'
    answerIdentSignal = 'ST'
    answerIdentEntry = 'SE'
    fields = 2      #Name, Interpret
    hostNeeded = False


    def run(self, data):
        if len(data) != self.fields:
            i = 1

        Name = ""
        Interpret = ""

        if data[0] == "*":
            Name = ""
        elif data[0] == "_":
            Name = None
        else:
            Name = data[0]

        if data[1] == "*":
            Interpret = ""
        elif data[1] == "_":
            Interpret = None
        else:
            Interpret = data[1]
        
        Songs = self.DB.search_song(Name, Interpret)
        MSG = []
        MSG.append(self.answerIdentSignal + '#1')
        for s in Songs:
            # 0: ID
            # 1: Name
            # 2: Interpreter
            MSG.append('{}#{}#{}#{}'.format(self.answerIdentEntry, s['ID'], s['Name'], s['Interpret']) + "\n")
        MSG.append(self.answerIdentSignal + '#0')
        return MSG
