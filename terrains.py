from typing import Tuple
from shapely.geometry import Polygon, Point  # type: ignore


class Obstacle:
    """
    The Obstacle class represents an obstacle in a 2D space that can interact with walkers.

    An Obstacle is defined by its position (x, y) and its dimensions (width, height).
     The position represents the bottom-left corner of the obstacle.
     The dimensions represent the size of the obstacle in the x and y directions.

    Attributes:
        __x (float): The x-coordinate of the bottom-left corner of the obstacle.
        __y (float): The y-coordinate of the bottom-left corner of the obstacle.
        __width (float): The width of the obstacle.
        __height (float): The height of the obstacle.

    Methods:
        get_position() -> Tuple[float, float]: Returns the position of the obstacle as a tuple (x, y).
        get_dimensions() -> Tuple[float, float]: Returns the dimensions of the obstacle as a tuple (width, height).
        get_boundary() -> Polygon: Returns a Polygon object representing the boundary of the obstacle.
    """
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """
        Initializes an Obstacle object with the given position and dimensions.

        Args:
            x (float): The x-coordinate of the bottom-left corner of the obstacle.
            y (float): The y-coordinate of the bottom-left corner of the obstacle.
            width (float): The width of the obstacle.
            height (float): The height of the obstacle.
        """
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

    def get_position(self) -> Tuple[float, float]:
        """
        Returns the position of the obstacle.

        The position is represented as a tuple of two floats (x, y),
        where x is the x-coordinate of the bottom-left corner of the obstacle and y is
         the y-coordinate of the bottom-left corner of the obstacle.

        Returns:
            Tuple[float, float]: The position of the obstacle.
        """
        return self.__x, self.__y

    def get_dimensions(self) -> Tuple[float, float]:
        """
        Returns the dimensions of the obstacle.

        The dimensions are represented as a tuple of two floats (width, height),
         where width is the width of the obstacle and height is the height of the obstacle.

        Returns:
            Tuple[float, float]: The dimensions of the obstacle.
        """
        return self.__width, self.__height

    def get_boundary(self) -> Polygon:
        """
        Returns a Polygon object representing the boundary of the obstacle.

        The boundary is defined by the vertices of the obstacle,
         which are calculated based on the position and dimensions of the obstacle.

        Returns:
            Polygon: A Polygon object representing the boundary of the obstacle.
        """
        x, y = self.get_position()  # Get the position of the obstacle
        width, height = self.get_dimensions()  # Get the dimensions of the obstacle
        # Define the vertices of the obstacle's boundary
        vertices = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        # Create a Polygon from the vertices
        boundary = Polygon(vertices)
        return boundary  # Return the boundary of the obstacle


class EnchantedGate:
    """
    The EnchantedGate class represents a magical gate in a 2D space that can
     transport walkers from its entrance to its exit.

    An EnchantedGate is defined by its entrance and exit locations, and its dimensions (width, height).
    The entrance location represents the bottom-left corner of the entrance of the gate.
    The exit location represents the bottom-left corner of the exit of the gate.
    The dimensions represent the size of the gate in the x and y directions.

    Attributes:
        __entrance_location (Tuple[float, float]): The x and y coordinates of the entrance of the gate.
        __exit_location (Tuple[float, float]): The x and y coordinates of the exit of the gate.
        __width (float): The width of the entrance to the gate.
        __height (float): The height of the entrance to the gate.

    Methods:
        get_entrance_location() -> Tuple[float, float]: Returns the location of the entrance
         of the gate as a tuple (x, y).
        get_exit_location() -> Tuple[float, float]: Returns the location of the exit of the gate as a tuple (x, y).
        get_dimensions() -> Tuple[float, float]: Returns the dimensions of the entrance of
         the gate as a tuple (width, height).
        get_boundary() -> Polygon: Returns a Polygon object representing the boundary of the entrance of the gate.
    """
    def __init__(self, entrance_location: Tuple[float, float],
                 exit_location: Tuple[float, float], width: float, height: float) -> None:
        """
        Initializes an EnchantedGate object with the given entrance and exit locations, and dimensions.

        Args:
            entrance_location (Tuple[float, float]): The x and y coordinates of the entrance of the gate.
            exit_location (Tuple[float, float]): The x and y coordinates of the exit of the gate.
            width (float): The width of the entrance of the gate.
            height (float): The height of the entrance of the gate.
        """
        self.__entrance_location = entrance_location
        self.__exit_location = exit_location
        self.__width = width
        self.__height = height

    def get_entrance_location(self) -> Tuple[float, float]:
        """
        Retrieves the location of the entrance of the gate.

        Returns:
            Tuple[float, float]: A tuple containing the x and y coordinates of the entrance location.
        """

        return self.__entrance_location

    def get_exit_location(self) -> Tuple[float, float]:
        """
        Retrieves the location of the exit of the gate.

        Returns:
            Tuple[float, float]: A tuple containing the x and y coordinates of the exit location.
        """
        return self.__exit_location

    def get_dimensions(self) -> Tuple[float, float]:
        """
        Retrieves the dimensions of the gate.

        Returns:
            Tuple[float, float]: A tuple containing the width and height of the gate.
        """
        return self.__width, self.__height

    def get_boundary(self) -> Polygon:
        """
        Retrieves the boundary of the gate as a Polygon object. The boundary is defined by the vertices of the gate,
        which are calculated based on the entrance location and dimensions of the gate.

        Returns:
            Polygon: A Polygon object representing the boundary of the gate.
        """
        # Get the entrance location of the gate
        x, y = self.get_entrance_location()
        # Get the dimensions of the gate
        width, height = self.get_dimensions()
        # Define the vertices of the gate's boundary
        vertices = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        # Create a Polygon from the vertices
        boundary = Polygon(vertices)
        # Return the boundary of the gate
        return boundary


class Grass:
    """
    The Grass class represents a grass tile in a 2D terrain.

    Each grass tile is defined by its position (x, y) and its dimensions (width, height).
    The position represents the bottom-left corner of the grass tile.
    The dimensions represent the size of the grass tile in the x and y directions.

    Attributes:
        __x (float): The x-coordinate of the bottom-left corner of the grass tile.
        __y (float): The y-coordinate of the bottom-left corner of the grass tile.
        __width (float): The width of the grass tile.
        __height (float): The height of the grass tile.

    Methods:
        get_position() -> Tuple[float, float]: Returns the position of the grass tile as a tuple (x, y).
        get_dimensions() -> Tuple[float, float]: Returns the dimensions of the grass tile as a tuple (width, height).
        get_boundary() -> Polygon: Returns a Polygon object representing the boundary of the grass tile.
    """
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """
        Initializes a Grass object with the given position and dimensions.

        Args:
            x (float): The x-coordinate of the bottom-left corner of the grass tile.
            y (float): The y-coordinate of the bottom-left corner of the grass tile.
            width (float): The width of the grass tile.
            height (float): The height of the grass tile.
        """
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

    def get_position(self) -> Tuple[float, float]:
        """
        Returns the position of the grass tile.

        The position is represented as a tuple of two floats (x, y),
        where x is the x-coordinate of the bottom-left corner of the grass tile and y is
        the y-coordinate of the bottom-left corner of the grass tile.

        Returns:
            Tuple[float, float]: The position of the grass tile.
        """
        return self.__x, self.__y

    def get_dimensions(self) -> Tuple[float, float]:
        """
        Returns the dimensions of the grass tile.

        The dimensions are represented as a tuple of two floats (width, height),
        where width is the width of the grass tile and height is the height of the grass tile.

        Returns:
            Tuple[float, float]: The dimensions of the grass tile.
        """
        return self.__width, self.__height

    def get_boundary(self) -> Polygon:
        """
        Returns a Polygon object representing the boundary of the grass tile.

        The boundary is defined by the vertices of the grass tile,
        which are calculated based on the position and dimensions of the grass tile.

        Returns:
            Polygon: A Polygon object representing the boundary of the grass tile.
        """
        x, y = self.get_position()  # Get the position of the grass tile
        width, height = self.get_dimensions()  # Get the dimensions of the grass tile
        # Define the vertices of the grass tile's boundary
        vertices = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        # Create a Polygon from the vertices
        boundary = Polygon(vertices)
        return boundary  # Return the boundary of the grass tile


class Water:
    """
    The Water class represents a water tile in a 2D terrain.

    Each water tile is defined by its position (x, y) and its dimensions (width, height).
    The position represents the bottom-left corner of the water tile.
    The dimensions represent the size of the water tile in the x and y directions.

    Attributes:
        __x (float): The x-coordinate of the bottom-left corner of the water tile.
        __y (float): The y-coordinate of the bottom-left corner of the water tile.
        __width (float): The width of the water tile.
        __height (float): The height of the water tile.

    Methods:
        get_position() -> Tuple[float, float]: Returns the position of the water tile as a tuple (x, y).
        get_dimensions() -> Tuple[float, float]: Returns the dimensions of the water tile as a tuple (width, height).
        get_boundary() -> Polygon: Returns a Polygon object representing the boundary of the water tile.
    """
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """
        Initializes a Water object with the given position and dimensions.

        Args:
            x (float): The x-coordinate of the bottom-left corner of the water tile.
            y (float): The y-coordinate of the bottom-left corner of the water tile.
            width (float): The width of the water tile.
            height (float): The height of the water tile.
        """
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

    def get_position(self) -> Tuple[float, float]:
        """
        Returns the position of the water tile.

        The position is represented as a tuple of two floats (x, y),
        where x is the x-coordinate of the bottom-left corner of the water tile and y is
        the y-coordinate of the bottom-left corner of the water tile.

        Returns:
            Tuple[float, float]: The position of the water tile.
        """
        return self.__x, self.__y

    def get_dimensions(self) -> Tuple[float, float]:
        """
        Returns the dimensions of the water tile.

        The dimensions are represented as a tuple of two floats (width, height),
        where width is the width of the water tile and height is the height of the water tile.

        Returns:
            Tuple[float, float]: The dimensions of the water tile.
        """
        return self.__width, self.__height

    def get_boundary(self) -> Polygon:
        """
        Returns a Polygon object representing the boundary of the water tile.

        The boundary is defined by the vertices of the water tile,
        which are calculated based on the position and dimensions of the water tile.

        Returns:
            Polygon: A Polygon object representing the boundary of the water tile.
        """
        x, y = self.get_position()  # Get the position of the water tile
        width, height = self.get_dimensions()  # Get the dimensions of the water tile
        # Define the vertices of the water tile's boundary
        vertices = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        # Create a Polygon from the vertices
        boundary = Polygon(vertices)
        return boundary  # Return the boundary of the water tile


class Sand:
    """
    The Sand class represents a sand tile in a 2D terrain.

    Each sand tile is defined by its position (x, y) and its dimensions (width, height).
    The position represents the bottom-left corner of the sand tile.
    The dimensions represent the size of the sand tile in the x and y directions.

    Attributes:
        __x (float): The x-coordinate of the bottom-left corner of the sand tile.
        __y (float): The y-coordinate of the bottom-left corner of the sand tile.
        __width (float): The width of the sand tile.
        __height (float): The height of the sand tile.

    Methods:
        get_position() -> Tuple[float, float]: Returns the position of the sand tile as a tuple (x, y).
        get_dimensions() -> Tuple[float, float]: Returns the dimensions of the sand tile as a tuple (width, height).
        get_boundary() -> Polygon: Returns a Polygon object representing the boundary of the sand tile.
    """
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """
        Initializes a Sand object with the given position and dimensions.

        Args:
            x (float): The x-coordinate of the bottom-left corner of the sand tile.
            y (float): The y-coordinate of the bottom-left corner of the sand tile.
            width (float): The width of the sand tile.
            height (float): The height of the sand tile.
        """
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

    def get_position(self) -> Tuple[float, float]:
        """
        Returns the position of the sand tile.

        The position is represented as a tuple of two floats (x, y),
        where x is the x-coordinate of the bottom-left corner of the sand tile and y is
        the y-coordinate of the bottom-left corner of the sand tile.

        Returns:
            Tuple[float, float]: The position of the sand tile.
        """
        return self.__x, self.__y

    def get_dimensions(self) -> Tuple[float, float]:
        """
        Returns the dimensions of the sand tile.

        The dimensions are represented as a tuple of two floats (width, height),
        where width is the width of the sand tile and height is the height of the sand tile.

        Returns:
            Tuple[float, float]: The dimensions of the sand tile.
        """
        return self.__width, self.__height

    def get_boundary(self) -> Polygon:
        """
        Returns a Polygon object representing the boundary of the sand tile.

        The boundary is defined by the vertices of the sand tile,
        which are calculated based on the position and dimensions of the sand tile.

        Returns:
            Polygon: A Polygon object representing the boundary of the sand tile.
        """
        x, y = self.get_position()  # Get the position of the sand tile
        width, height = self.get_dimensions()  # Get the dimensions of the sand tile
        # Define the vertices of the sand tile's boundary
        vertices = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        # Create a Polygon from the vertices
        boundary = Polygon(vertices)
        return boundary  # Return the boundary of the sand tile
