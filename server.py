from mcstatus import MinecraftServer
from os import path

class Server:
    """
    A class to handle a Minecraft server.

    Attributes
    ----------
    `ip` : str
        The IP of the Minecraft server.


    Methods
    ----------
    `check_status` : bool
        Pings the server to check if the server is online or offline.
    
    `get_players` : int
        Checks how many players are online on the server.

    `get_player_names` : str
        Returns the names of the players online.

    """
    def __init__(self, ip):
        self.ip = ip
        self.server = MinecraftServer.lookup(self.ip)
    

    def check_status(self):
        """
        Method to check if the server is online.

        Returns:
        ----------
        `bool` : True when ping was successful
        """
        try:
            self.server.ping()
            return True
        except Exception as e:
            return False


    def get_players(self):
        """
        Method to get the current number of online players on the server.

        Returns:
        ----------
        `int` : Number of players online
        """
        return self.server.status().players.online
    

    def get_player_names(self):
        """
        Method to get the names of the online players on the server.

        Returns:
        ----------
        `list` : List of player names
        """
        names = [user['name'] for user in self.server.status().raw['players']['sample']]
        return names
    

class World:
    """

    
    Methods
    ----------
    `save_coords` : None
        Saves coordinates and message to json file.

    """
    def __init__(self):
        self.coords_file = 'coordinates.json'


    def save_coordinates(self, coords):
        """
        Method to save world coordinates.

        Parameters:
        ------------
        `coords` : list
            List of xPos, yPos, zPos and description

        Returns:
        ----------
        True : True if coords were saved
        """
        pos = f'{coords[0]}, {coords[1]}, {coords[2]}'
        descr = str(" ".join(coords[3:]))

        if not self.check_coords_file():
            file = open(self.coords_file, 'x')
        
        if not self.__check_coordinates(pos):
            file = open(self.coords_file, 'a')
            file.write(f'{str(pos)} - {descr}\n')
            file.close()
            return True
        return False
        


    def load_coordinates(self):
        """
        Gets the saved coordinates from json file.

        Returns:
        ----------
        None : None if coordinates file does not exist
        `list` : list with coordinates ()
        """
        file = open(self.coords_file, 'r')
        return file.readlines()


    def check_coords_file(self):
        if path.exists(self.coords_file):
            return True
        return False


    def __check_coordinates(self, pos):
        file = open(self.coords_file, 'r')
        line = file.readline()
        
        while line:
            if str(pos) in line:
                return True
            line = file.readline()
        return False
