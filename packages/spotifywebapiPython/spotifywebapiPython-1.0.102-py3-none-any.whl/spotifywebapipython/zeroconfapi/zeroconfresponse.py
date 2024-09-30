# external package imports.

# our package imports.
from ..sautils import export

@export
class ZeroconfResponse:
    """
    Spotify Zeroconf API basic response object.
    """

    def __init__(self, root:dict=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (dict):
                Spotify Web API JSON response in dictionary format, used to load object
                attributes; otherwise, None to not load attributes.
        """
        self._SpotifyError:int = None
        self._Status:int = None
        self._StatusString:str = None
        self._ResponseSource:str = None
        
        if (root is None):

            pass
        
        else:

            # some devices return the `status` and `spotifyError` values as string,
            # while others return them as numeric; use the property setters to
            # convert them to numeric if they are strings that contain a numeric value.
            self._ResponseSource = root.get('responseSource', None)
            self.SpotifyError = root.get('spotifyError', None)
            self.Status = root.get('status', None)
            self._StatusString = root.get('statusString', None)
            
    
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ResponseSource(self) -> str:
        """ 
        Response source string (e.g. "").
        """
        return self._ResponseSource


    @property
    def SpotifyError(self) -> int:
        """ 
        The last error code returned by a Spotify API call or the SpCallbackError() callback (e.g. 0, -119, etc).
        """
        return self._SpotifyError
    
    @SpotifyError.setter
    def SpotifyError(self, value:int):
        """ 
        Sets the SpotifyError property value.
        """
        if isinstance(value, int):
            self._SpotifyError = value
        elif isinstance(value, str):
            if value.isnumeric():
                self._SpotifyError = int(value)


    @property
    def Status(self) -> int:
        """ 
        A code indicating the result of the operation (e.g. 101, 402, etc).
        """
        return self._Status
    
    @Status.setter
    def Status(self, value:int):
        """ 
        Sets the Status property value.
        """
        if isinstance(value, int):
            self._Status = value
        elif isinstance(value, str):
            if value.isnumeric():
                self._Status = int(value)


    @property
    def StatusString(self) -> str:
        """ 
        The string describing the status code (e.g. "OK", "ERROR-SPOTIFY-ERROR", etc).
        """
        return self._StatusString
    
    @StatusString.setter
    def StatusString(self, value:str):
        """ 
        Sets the StatusString property value.
        """
        if isinstance(value, str):
            self._StatusString = value


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'SpotifyError': self._SpotifyError,
            'Status': self._Status,
            'StatusString': self._StatusString,
            'ResponseSource': self._ResponseSource,
        }
        return result
        

    def ToString(self, includeTitle:bool=True) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeTitle (str):
                True to include the class name title prefix.
        """
        msg:str = ''
        if includeTitle: 
            msg = 'ZeroconfResponse:'
        
        if self._SpotifyError is not None: msg = '%s\n SpotifyError="%s"' % (msg, str(self._SpotifyError))
        if self._Status is not None: msg = '%s\n Status="%s"' % (msg, str(self._Status))
        if self._StatusString is not None: msg = '%s\n StatusString="%s"' % (msg, str(self._StatusString))
        if self._ResponseSource is not None: msg = '%s\n ResponseSource="%s"' % (msg, str(self._ResponseSource))
        return msg 
