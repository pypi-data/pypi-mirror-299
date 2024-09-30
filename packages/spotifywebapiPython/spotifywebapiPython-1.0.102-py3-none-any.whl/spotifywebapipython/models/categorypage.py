# external package imports.

# our package imports.
from ..sautils import export
from .pageobject import PageObject
from .category import Category

@export
class CategoryPage(PageObject):
    """
    Spotify Web API CategoryPage object.
    
    This allows for multiple pages of `Category` objects to be navigated.
    """

    def __init__(self, root:dict=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (dict):
                Spotify Web API JSON response in dictionary format, used to load object
                attributes; otherwise, None to not load attributes.
        """
        # initialize base class.
        super().__init__(root=root)
        
        # initialize storage.
        self._Items:list[Category] = []
        
        if (root is None):

            pass
        
        else:

            # process all collections and objects.
            items:list = root.get('items',None)
            if items is not None:
                for item in items:
                    if item is not None:
                        self._Items.append(Category(root=item))

        
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Items(self) -> list[Category]:
        """ 
        Array of `Category` objects.
        """
        return self._Items
    

    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include the Items collection of objects; otherwise, False
                to only return base properties.
        """
        return 'CategoryPage: %s' % super().ToString(includeItems)
