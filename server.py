from mcstatus import MinecraftServer

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

        Returns :
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

        Returns :
        ----------
        `int` : Number of players online
        """
        return self.server.status().players.online
    

    def get_player_names(self):
        """
        Method to get the names of the online players on the server.

        Returns :
        ----------
        `list` : List of player names
        """
        names = [user['name'] for user in self.server.status().raw['players']['sample']]
        return names
    
