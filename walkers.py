import math
import random
from typing import List, Tuple, Optional


class Walker:
    """
    Represents a basic random walker in a 2D space.

    This class provides the basic functionality for a random walker, including
    methods to get and set the walker's position, move back to the previous position,
    reset the position to the origin, and check if the walker has escaped a certain radius.

    Attributes:
    _x (float): The current x-coordinate of the walker.
    _y (float): The current y-coordinate of the walker.
    _prev_x (float): The previous x-coordinate of the walker.
    _prev_y (float): The previous y-coordinate of the walker.
    escaped (bool): Indicates whether the walker has escaped a radius of 10 from the origin.
    """

    def __init__(self):
        """
        Initialize the Walker object with initial position at the origin (0,0).
        """
        self._x = 0
        self._y = 0
        self._prev_x, self._prev_y = 0, 0
        self.escaped = False

    def get_location(self) -> Tuple[float, float]:
        """
        Get the current location of the walker.

        Returns:
            Tuple[float, float]: A tuple containing the current x and y coordinates.
        """
        return self._x, self._y

    def get_prev_location(self) -> Tuple[float, float]:
        """
        Get the previous location of the walker.

        Returns:
            Tuple[float, float]: A tuple containing the previous x and y coordinates.
        """
        return self._prev_x, self._prev_y

    def move_back(self) -> None:
        """
        Move the walker back to its previous position.

        This method is useful in situations where a move is made and then needs to be undone.
        """
        self._x, self._y = self._prev_x, self._prev_y

    def reset_walker(self) -> None:
        """
        Reset the position of the walker to the origin and reset y_crosses.
        """
        self._x, self._y = 0, 0
        self.escaped = False

    def escape_check(self) -> bool:
        """
        Check if the walker has escaped a radius 10 of the origin.

        This method is useful for determining if the walker has moved beyond a certain distance from the origin.

        Returns:
            bool: True if the walker has escaped, False otherwise.
        """
        if math.sqrt(self.get_location()[0] ** 2 + self.get_location()[1] ** 2) <= 10 and not self.escaped:
            return False
        self.escaped = True
        return True

    def set_position(self, position: Tuple[float, float]) -> None:
        """
        Set the position of the walker to the specified coordinates.

        Args:
            position (Tuple[float, float]): The new position of the walker.
        """
        self._x, self._y = position[0], position[1]

    def move(self) -> None:
        """
        Move the walker.

        This method should be implemented by subclasses to define the specific movement behavior of the walker.
        """
        pass


class UnitWalker(Walker):
    """
    The UnitWalker class represents a specific type of Walker that moves in unit distances in random directions.

    This class inherits from the Walker base class and overrides the move method
     to implement its unique movement behavior.

    Attributes:
    _x (float): The current x-coordinate of the walker.
    _y (float): The current y-coordinate of the walker.
    _prev_x (float): The previous x-coordinate of the walker.
    _prev_y (float): The previous y-coordinate of the walker.
    escaped (bool): Indicates whether the walker has escaped a radius of 10 from the origin.
    _y_crosses (int): The number of times the walker crosses the y-axis.
    """

    def move(self) -> None:
        """
        Overrides the move method of the Walker base class.

        This method moves the walker in a random direction by a unit distance.
        The direction is chosen uniformly at random from the interval [0, 2*pi],
        representing all possible directions in a 2D plane.
        The walker's current position is updated based on this direction.

        The method also updates the previous position of the walker before making the move.
         This is useful in case the move needs to be undone later.
        """
        # Generate a random direction in radians
        direction = random.uniform(0, 2 * math.pi)

        # Store the current position as the previous position
        self._prev_x, self._prev_y = self._x, self._y

        # Update the current position based on the direction
        self._x += math.cos(direction)
        self._y += math.sin(direction)


class RandomDistanceWalker(Walker):
    """
    The RandomDistanceWalker class represents a specific type of Walker that moves
     in random directions with random distances.

    This class inherits from the Walker base class and overrides the move
     method to implement its unique movement behavior.
     The distance of each move is chosen randomly from a uniform distribution between 0.5 and 1.5.

    Attributes:
    _x (float): The current x-coordinate of the walker.
    _y (float): The current y-coordinate of the walker.
    _prev_x (float): The previous x-coordinate of the walker.
    _prev_y (float): The previous y-coordinate of the walker.
    escaped (bool): Indicates whether the walker has escaped a radius of 10 from the origin.
    _y_crosses (int): The number of times the walker crosses the y-axis.
    """

    def move(self) -> None:
        """
        Overrides the move method of the Walker base class.

        This method moves the walker in a random direction by a random distance.
        The direction is chosen uniformly at random from the interval [0, 2*pi],
        representing all possible directions in a 2D plane.
        The distance is chosen uniformly at random from the interval [0.5, 1.5],
        representing all possible distances in the specified range.

        The walker's current position is updated based on this direction and distance.

        The method also updates the previous position of the walker before making the move.
         This is useful in case the move needs to be undone later.
        """
        # Generate a random direction in radians
        direction = random.uniform(0, 2 * math.pi)

        # Generate a random distance in the range [0.5, 1.5)
        distance = random.uniform(0.5, 1.5)

        # Store the current position as the previous position
        self._prev_x, self._prev_y = self._x, self._y

        # Update the current position based on the direction and distance
        self._x += distance * math.cos(direction)
        self._y += distance * math.sin(direction)


class StraightWalker(Walker):
    """
    The StraightWalker class represents a specific type of Walker that moves in straight lines in random directions.

    This class inherits from the Walker base class and overrides the move method to implement
     its unique movement behavior. The direction of each move is chosen randomly from the
      four cardinal directions: up, down, left, and right.

    Attributes:
    _x (float): The current x-coordinate of the walker.
    _y (float): The current y-coordinate of the walker.
    _prev_x (float): The previous x-coordinate of the walker.
    _prev_y (float): The previous y-coordinate of the walker.
    escaped (bool): Indicates whether the walker has escaped a radius of 10 from the origin.
    _y_crosses (int): The number of times the walker crosses the y-axis.
    """

    def move(self) -> None:
        """
        Overrides the move method of the Walker base class.

        This method moves the walker in a straight line in a random direction.
        The direction is chosen randomly from the four cardinal directions: up, down, left, and right.

        The walker's current position is updated based on the chosen direction.

        The method also updates the previous position of the walker before making the move.
         This is useful in case the move needs to be undone later.
        """
        # Define the four possible directions: up, down, left, and right
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        # Choose a random direction
        direction = random.choice(directions)

        # Store the current position as the previous position
        self._prev_x, self._prev_y = self._x, self._y

        # Update the current position based on the chosen direction
        self._x += direction[0]
        self._y += direction[1]


class DirectionalBiasWalker(Walker):
    """
    The DirectionalBiasWalker class represents a specific type of Walker
     that moves in a direction based on a set of predefined probabilities.

    This class inherits from the Walker base class and overrides the move method
     to implement its unique movement behavior.
      The direction of each move is chosen based on the bias probabilities
       provided during the initialization of the object.

    Attributes:
    _x (float): The current x-coordinate of the walker.
    _y (float): The current y-coordinate of the walker.
    _prev_x (float): The previous x-coordinate of the walker.
    _prev_y (float): The previous y-coordinate of the walker.
    escaped (bool): Indicates whether the walker has escaped a radius of 10 from the origin.
    _y_crosses (int): The number of times the walker crosses the y-axis.
    _bias_probabilities (List[float]): A list containing the probabilities of choosing each direction.
    """

    def __init__(self, bias_probabilities: Optional[List[float]] = None) -> None:
        """
        Initialize the DirectionalBiasWalker object.

        Args:
            bias_probabilities (List[float]): A list containing the probabilities of choosing each direction.
             If not provided, equal probabilities are assumed for all directions.
        """
        super().__init__()
        if bias_probabilities is None:
            bias_probabilities = [1, 1, 1, 1, 1]
        self._bias_probabilities = self.normalize_weights(bias_probabilities)

    @staticmethod
    def normalize_weights(weights: List[float]) -> List[float]:
        """
        Normalize the weights to ensure they sum up to 1.

        This method takes a list of weights as input and returns a new list
         where each weight is divided by the total sum of the weights.
          This ensures that the sum of all weights in the returned list is 1.

        Args:
            weights (List[float]): A list of weights.

        Returns:
            List[float]: Normalized weights.
        """
        # Calculate the total sum of the weights
        total = sum(weights)

        # If the total sum is not 1, normalize the weights
        if total != 1:
            # Use list comprehension to create a new list where each weight is divided by the total sum
            return [w / total for w in weights]
        else:
            # If the total sum is already 1, return the original list
            return weights

    def angle_to_origin_distance_1(self) -> Optional[Tuple[float, float]]:
        """
        Calculate the angle to the origin.

        This method calculates the angle from the walker's current position to the origin (0,0).
        It returns the cosine and sine of the angle,
          which represent the direction of the origin from the walker's position.
        If the walker is already at the origin, it returns None.

        Returns:
            Tuple[float, float]: The cosine and sine of the angle to the origin, or None if the walker is at the origin.
        """
        # Calculate the y and x components of the vector from the walker's position to the origin
        y, x = -self._y, -self._x

        # Calculate the length of the vector using the Pythagorean theorem
        length = math.sqrt(x ** 2 + y ** 2)

        # If the length is not zero (i.e., the walker is not at the origin)
        if length != 0:
            # Return the cosine and sine of the angle to the origin
            return x / length, y / length

        # If the walker is at the origin, return None
        return None

    def move(self) -> None:
        """
        Move the walker according to its directional bias.
        This method overrides the move method of the Walker base class.
        It moves the walker in a direction based on the bias probabilities
         provided during the initialization of the object.
        The direction is chosen from a list of possible directions,
         which includes the four cardinal directions and the direction towards the origin.
        The direction towards the origin is calculated by the method angle_to_origin_distance_1.
        If the walker is already at the origin, this direction is not included in the list of possible directions.
        The chosen direction is then used to update the walker's current position.
        """

        # Define the possible directions: up, down, left, right, and towards the origin
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0), self.angle_to_origin_distance_1()]

        # Filter out the direction towards the origin if the walker is already at the origin
        relevant_directions = [direction for direction in directions if direction is not None]

        # Choose a direction based on the bias probabilities
        # The random.choices function is used to make a weighted random choice
        chosen_direction = random.choices(relevant_directions, self._bias_probabilities[:len(relevant_directions)])

        # Store the current position as the previous position
        self._prev_x, self._prev_y = self._x, self._y

        # Update the current position based on the chosen direction
        self._x += chosen_direction[0][0]
        self._y += chosen_direction[0][1]


class MemoryWalker(Walker):
    """
    The MemoryWalker class represents a specific type of Walker that remembers its previous moves.

    This class inherits from the Walker base class and overrides the move method to implement
    its unique movement behavior. The walker remembers its previous moves and avoids repeating them.
    The size of the walker's memory is defined by the `__memory_size` attribute.

    Attributes:
    _x (float): The current x-coordinate of the walker.
    _y (float): The current y-coordinate of the walker.
    _prev_x (float): The previous x-coordinate of the walker.
    _prev_y (float): The previous y-coordinate of the walker.
    escaped (bool): Indicates whether the walker has escaped a radius of 10 from the origin.
    _y_crosses (int): The number of times the walker crosses the y-axis.
    __memory_size (int): The size of the walker's memory.
    __memory (List[Tuple[int, int]]): The walker's memory of previous moves.
    """
    def __init__(self) -> None:
        """
        Initialize the MemoryWalker object with initial position at the origin (0,0) and an empty memory.
        """
        super().__init__()
        self.__memory_size = 1000  # Define the size of the walker's memory
        self.__memory: List[Tuple[int, int]] = []  # Initialize the walker's memory as an empty list

    def possible_moves(self) -> List[Tuple[int, int]]:
        """
        Get the possible moves for the walker.

        This method calculates the possible moves for the walker based on its current position.
        It excludes moves that are in the walker's memory.

        Returns:
            List[Tuple[int, int]]: A list of possible moves.
        """
        # Define the possible moves
        possible_moves = [(self._x, self._y - 1), (self._x, self._y + 1),
                          (self._x + 1, self._y), (self._x - 1, self._y)]
        # Exclude moves that are in the walker's memory
        return [move for move in possible_moves if move not in self.__memory]

    def move(self) -> None:
        """
        Move the walker according to its memory.

        This method overrides the move method of the Walker base class.
        It moves the walker to a position that is not in its memory.
        If all possible moves are in the memory, it chooses a random direction.
        """
        # If there are possible moves not in the memory
        if self.possible_moves():
            # Choose a random move from the possible moves
            direction = random.choice(self.possible_moves())
            # Store the current position as the previous position
            self._prev_x, self._prev_y = self._x, self._y
            # Update the current position based on the chosen direction
            self._x, self._y = direction[0], direction[1]
            # Add the new position to the memory
            self.__memory.append((self._x, self._y))
        else:
            # If all possible moves are in the memory, choose a random direction
            direction = random.choice([(0, -1), (0, 1), (1, 0), (-1, 0)])
            self._prev_x, self._prev_y = self._x, self._y
            self._x += direction[0]
            self._y += direction[1]

    def update_memory(self) -> None:
        """
        Update the memory with the current position.

        This method adds the current position to the walker's memory.
        If the memory is full, it removes the oldest position.
        """
        # Add the current position to the memory
        self.__memory.append((self._x, self._y))
        # If the memory is full, remove the oldest position
        if len(self.__memory) > self.__memory_size:
            self.__memory.pop(0)

    def reset_walker(self) -> None:
        """
        Reset the position of the walker to the origin and reset the memory.
        """
        super().reset_walker()  # Call the reset_walker method of the base class
        self.__memory = []  # Reset the walker's memory to an empty list
