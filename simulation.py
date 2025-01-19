import math
import random
from walkers import *
from terrains import *
from typing import Dict, List, Union, Optional
from shapely.geometry import LineString, Point  # type: ignore


class Simulation:
    """
    The Simulation class is responsible for simulating the movement of walkers through different
     terrains and enchanted gates.

    Methods:
        set_interaction(interaction: str) -> None: Sets the interaction type between walkers.
        add_walker(walker: Walker) -> None: Adds a walker to the simulation.
        add_grass(grass: Grass) -> None: Adds a grass terrain to the simulation.
        add_sand(sand: Sand) -> None: Adds a sand terrain to the simulation.
        add_water(water: Water) -> None: Adds a water terrain to the simulation.
        add_obstacle(obstacle: Obstacle) -> None: Adds an obstacle to the simulation.
        add_enchanted_gate(enchanted_gate: EnchantedGate) -> None: Adds an enchanted gate to the simulation.
        get_walkers() -> dict[str, Walker]: Returns the dictionary of walkers.
        get_escape_times() -> dict[str, int]: Returns the escape times of walkers.
        get_crosses_y() -> Dict[str, int]: Returns the number of times each walker crosses the y-axis.
        get_total_dict() -> Dict[str, Dict[int, Dict[str, Union[List[float], int, None]]]]:
            Returns the total results of the simulation.
        get_grasses() -> List[Grass]: Returns the list of grass terrains in the simulation.
        get_sands() -> List[Sand]: Returns the list of sand terrains in the simulation.
        get_waters() -> List[Water]: Returns the list of water terrains in the simulation.
        get_obstacles() -> List[Obstacle]: Returns the list of obstacles in the simulation.
        get_enchanted_gates() -> List[EnchantedGate]: Returns the list of enchanted gates in the simulation.
        locate_nearest_walker(walker: Walker) -> Walker: Locates the nearest walker to the given walker.
        choose_move(walker: Walker) -> None: Determines the next move for a walker.
        terrain_check(walker: Walker) -> str or bool: Checks if a walker is on a specific terrain.
        handle_terrain(walker: Walker, terrain: str) -> None: Handles the walker's movement based on the terrain.
        check_collision(walker: Walker) -> bool: Checks if a walker collides with any obstacles.
        gate_check(walker: Walker) -> None: Checks if a walker is at an enchanted gate entrance
            and moves it to the exit if so.
        cross_y_check(walker_name: str, walker: Walker) -> None: Checks if a walker crosses the y-axis
            and increments its counter if so.
        escape_check(walker_name: str, walker: Walker, i: int) -> None: Checks if a walker has escaped
            and updates its escape time if not.
        simulation_results_update(w alker_name: str, walker: Walker, i: int) -> None: Updates the simulation results.
        export_to_statistics(stat: Statistics, i: int) -> None: Exports simulation results to statistics.
        run_simulation() -> bool: Runs the simulation for the specified number of moves.
        reset() -> None: Resets the simulation to its initial state.
    """
    def __init__(self, num_moves: int):
        """
        Initializes a Simulation object with the specified number of moves.

        This method sets up the initial state of the simulation, including the number of moves,
        the walkers, obstacles, enchanted gates, escape times, y-axis crossings, and terrains.


        Attributes:
        __num_moves (int): The number of moves for the simulation.
        __walkers (dict): A dictionary of walkers participating in the simulation.
        __obstacles (list): A list of obstacles present in the simulation.
        __enchanted_gates (list): A list of enchanted gates present in the simulation.
        __escape_times (dict): A dictionary tracking the escape times for each walker.
        __crosses_y (dict): A dictionary tracking how many times each walker crosses the y-axis.
        __total_dict (dict): A dictionary to store the total results of the simulation.
        __sands (list): A list of sand terrains in the simulation.
        __waters (list): A list of water terrains in the simulation.
        __grasses (list): A list of grass terrains in the simulation.
        __walkers_interaction (str): The type of interaction between walkers ('attract' or 'repel').
        """
        self.__num_moves = num_moves
        self.__walkers: Dict[str, Walker] = {}
        self.__obstacles: List[Obstacle] = []
        self.__enchanted_gates: List[EnchantedGate] = []
        self.__escape_times: Dict[str, Optional[int]] = {}
        self.__crosses_y: Dict[str, int] = {}
        self.__total_dict: Dict[str, Dict[int, Dict[str, Union[List[float], int, None]]]] = {}
        self.__sands: List[Sand] = []
        self.__waters: List[Water] = []
        self.__grasses: List[Grass] = []
        self.__walkers_interaction: Optional[str] = None

    def set_interaction(self, interaction: str) -> None:
        """
        Sets the interaction type between walkers in the simulation.

        This method is used to define how walkers interact with each other during the simulation.
        The interaction type can be either 'attract' or 'repel'. If 'attract' is set, walkers will
        move towards each other. If 'repel' is set, walkers will move away from each other.

        Parameters:
        - interaction (str): The interaction type between walkers. This should be either 'attract' or 'repel'.

        Raises:
        - ValueError: If the provided interaction type exists, and it is not 'attract' or 'repel'.
        """
        if interaction and interaction not in ['attract', 'repel']:
            raise ValueError("Interaction type must be either 'attract' or 'repel'.")
        self.__walkers_interaction = interaction

    def add_walker(self, walker: Walker) -> None:
        """
        Adds a walker to the simulation.

        This method is used to add a new walker to the simulation. It generates a unique name for the walker
        based on its type and the existing walkers of the same type. It also initializes the escape time,
        y-axis crossing count, and simulation results for the new walker.

        Parameters:
        - walker (Walker): The Walker object to be added to the simulation.

        Raises:
        - TypeError: If the provided walker is not an instance of the Walker class.
        """
        if not isinstance(walker, Walker):
            raise TypeError("The walker must be an instance of the Walker class.")

        index = 1
        while type(walker).__name__ + str(index) in self.__walkers:
            index += 1
        walker_name = type(walker).__name__ + str(index)
        self.__walkers[walker_name] = walker
        self.__escape_times[walker_name] = None
        self.__crosses_y[walker_name] = -1
        self.__total_dict[walker_name] = {}

    def add_grass(self, grass: Grass) -> None:
        """
        Adds a grass terrain to the simulation.

        This method is used to add a new grass terrain to the simulation.
         The grass terrain is represented by an instance of the Grass class.
         The grass terrain will affect the movement of walkers during the simulation.

        Parameters:
        - grass (Grass): The Grass object to be added to the simulation.

        Raises:
        - TypeError: If the provided grass is not an instance of the Grass class.
        """
        if not isinstance(grass, Grass):
            raise TypeError("The grass must be an instance of the Grass class.")
        self.__grasses.append(grass)

    def add_sand(self, sand):
        """
        Adds a sand terrain to the simulation.

        This method is used to add a new sand terrain to the simulation.
         The sand terrain is represented by an instance of the Sand class.
         The sand terrain will affect the movement of walkers during the simulation.

        Parameters:
        - sand (Sand): The Sand object to be added to the simulation.

        Raises:
        - TypeError: If the provided sand is not an instance of the Sand class.
        """
        if not isinstance(sand, Sand):
            raise TypeError("The sand must be an instance of the Sand class.")
        self.__sands.append(sand)

    def add_water(self, water):
        """
        Adds a water terrain to the simulation.

        This method is used to add a new water terrain to the simulation.
         The water terrain is represented by an instance of the Water class.
         The water terrain will affect the movement of walkers during the simulation.

        Parameters:
        - water (Water): The Water object to be added to the simulation.

        Raises:
        - TypeError: If the provided water is not an instance of the Water class.
        """
        if not isinstance(water, Water):
            raise TypeError("The water must be an instance of the Water class.")
        self.__waters.append(water)

    def add_obstacle(self, obstacle) -> None:
        """
        Adds an obstacle to the simulation.

        This method is used to add a new obstacle to the simulation. Each obstacle is represented as an instance of the
        Obstacle class. The obstacles can affect the movement of walkers during the simulation by blocking their path.

        Parameters:
            obstacle (Obstacle): The Obstacle object to be added to the simulation. This object represents a physical
            barrier that walkers cannot pass through. The obstacle's position, size, and shape are defined when the
            Obstacle object is created.

        Raises:
            TypeError: If the provided obstacle is not an instance of the Obstacle class.
        """
        if not isinstance(obstacle, Obstacle):
            raise TypeError("The obstacle must be an instance of the Obstacle class.")
        self.__obstacles.append(obstacle)

    def add_enchanted_gate(self, enchanted_gate: EnchantedGate) -> None:
        """
        Adds an enchanted gate to the simulation.

        This method is used to add a new enchanted gate to the simulation.
        Each enchanted gate is represented as an instance of the EnchantedGate class.
        The enchanted gates can affect the movement of walkers during the simulation by
        teleporting them from the gate's entrance to its exit.

        Parameters:
            enchanted_gate (EnchantedGate): The EnchantedGate object to be added to the simulation.
            This object represents a magical gate that can teleport walkers from its entrance to its exit.
            The entrance and exit locations of the gate are defined when the EnchantedGate object is created.

        Raises:
            TypeError: If the provided enchanted gate is not an instance of the EnchantedGate class.
        """
        if not isinstance(enchanted_gate, EnchantedGate):
            raise TypeError("The enchanted gate must be an instance of the EnchantedGate class.")
        self.__enchanted_gates.append(enchanted_gate)

    def get_walkers(self) -> dict[str, Walker]:
        """
        Retrieves the dictionary of all walkers present in the simulation.

        This method is used to access the walkers that have been added to the simulation.
        Each walker is represented as an instance of the Walker class. The walkers are stored in a dictionary,
        where the keys are unique names generated for each walker and the values are the corresponding Walker objects.

        Returns:
            Dict[str, Walker]: A dictionary containing all the Walker objects that are currently in the simulation.
            The keys are the unique names of the walkers and the values are the corresponding Walker objects.
        """
        return self.__walkers

    def get_escape_times(self) -> dict[str, Optional[int]]:
        """
        Retrieves the escape times of all walkers in the simulation.

        This method is used to access the escape times of the walkers that have been added to the simulation.
        The escape time of a walker is the number of moves it took for the walker to escape from the origin.
        The escape times are stored in a dictionary, where the keys are the unique names of the walkers and
        the values are the corresponding escape times.

        Returns:
            Dict[str, int]: A dictionary containing the escape times of all the Walker objects that are currently
            in the simulation. The keys are the unique names of the walkers and the values are the corresponding
            escape times. If a walker has not yet escaped, its escape time is None.
        """
        return self.__escape_times

    def get_crosses_y(self) -> Dict[str, int]:
        """
        Retrieves the number of times each walker crosses the y-axis.

        This method is used to access the count of y-axis crossings for each walker in the simulation.
        A crossing is counted when a walker moves from one side of the y-axis to the other.
        The counts are stored in a dictionary, where the keys are the unique names of the walkers and
        the values are the corresponding counts of y-axis crossings.

        Returns:
            Dict[str, int]: A dictionary containing the counts of y-axis crossings for all the Walker objects
            that are currently in the simulation. The keys are the unique names of the walkers and the values
            are the corresponding counts of y-axis crossings.
        """
        return self.__crosses_y

    def get_total_dict(self) -> Dict[str, Dict[int, Dict[str, Union[List[float], int, None]]]]:
        """
        Retrieves the total results of the simulation.

        This method is used to access the total results of the simulation.
        The results include the location, escape time, number of y-axis crossings, distance from origin,
        distance from x and y axes for each walker at each move of the simulation.
        The results are stored in a nested dictionary, where the first level keys are the unique names of the walkers,
        the second level keys are the move numbers, and the third level keys are the result types
        ('locations', 'escape time', 'y crosses', 'distance from origin', 'distance from x', 'distance from y').

        Returns:
            Dict[str, Dict[int, Dict[str, Union[List[float], int, None]]]]:
            A nested dictionary containing the total results of the simulation for all the Walker objects.
            The first level keys are the unique names of the walkers, the second level keys are the move numbers,
            and the third level keys are the result types ('locations', 'escape time', 'y crosses',
            'distance from origin', 'distance from x', 'distance from y'). The third level values are the corresponding
            result values.
        """
        return self.__total_dict

    def get_grasses(self) -> List[Grass]:
        """
        Retrieves the list of all grass terrains present in the simulation.

        This method is used to access the grass terrains that have been added to the simulation.
        Each grass terrain is represented as an instance of the Grass class. The grass terrains
        can affect the movement of walkers during the simulation.

        Returns:
        List[Grass]: A list containing all the Grass objects that are currently in the simulation.
        If no grass terrains have been added, this method returns an empty list.
        """
        return self.__grasses

    def get_sands(self) -> List[Sand]:
        """
        Retrieves the list of all sand terrains present in the simulation.

        This method is used to access the sand terrains that have been added to the simulation.
        Each sand terrain is represented as an instance of the Sand class. The sand terrains
        can affect the movement of walkers during the simulation.

        Returns:
        List[Sand]: A list containing all the Sand objects that are currently in the simulation.
        If no sand terrains have been added, this method returns an empty list.
        """
        return self.__sands

    def get_waters(self) -> List[Water]:
        """
        Retrieves the list of all water terrains present in the simulation.

        This method is used to access the water terrains that have been added to the simulation.
        Each water terrain is represented as an instance of the Water class. The water terrains
        can affect the movement of walkers during the simulation.

        Returns:
        List[Water]: A list containing all the Water objects that are currently in the simulation.
        If no water terrains have been added, this method returns an empty list.
        """
        return self.__waters

    def get_obstacles(self) -> List[Obstacle]:
        """
        Retrieves the list of all obstacles present in the simulation.

        This method is used to access the obstacles that have been added to the simulation.
        Each obstacle is represented as an instance of the Obstacle class. The obstacles
        can affect the movement of walkers during the simulation by blocking their path.

        Returns:
            List[Obstacle]: A list containing all the Obstacle objects that are currently in the simulation.
            If no obstacles have been added, this method returns an empty list.
        """
        return self.__obstacles

    def get_enchanted_gates(self) -> List[EnchantedGate]:
        """
        Retrieves the list of all enchanted gates present in the simulation.

        This method is used to access the enchanted gates that have been added to the simulation.
        Each enchanted gate is represented as an instance of the EnchantedGate class. The enchanted gates
        can affect the movement of walkers during the simulation by
        teleporting them from the gate's entrance to its exit.

        Returns:
            List[EnchantedGate]: A list containing all the EnchantedGate objects that are currently in the simulation.
            If no enchanted gates have been added, this method returns an empty list.
        """
        return self.__enchanted_gates

    def locate_nearest_walker(self, walker: Walker) -> Walker:
        """
        Locates the nearest walker to the given walker.

        This method calculates the Euclidean distance between the given walker and all other walkers in the simulation.
        It then returns the walker that is closest to the given walker. If there are no other walkers in the simulation,
        this method returns None.

        Parameters:
            walker (Walker): The Walker object for which to find the nearest walker.

        Returns:
            Walker: The Walker object that is closest to the given walker.
             If there are no other walkers in the simulation, this method returns None.

        Raises:
            ValueError: If there are no other walkers in the simulation.
        """
        # Initialize the minimum distance to infinity
        min_distance = float('inf')
        nearest_walker = None

        # Iterate over all walkers in the simulation
        for walker_name in self.__walkers:
            other_walker = self.__walkers[walker_name]

            # Skip the given walker
            if other_walker != walker:
                # Calculate the Euclidean distance between the given walker and the current walker
                distance = ((other_walker.get_location()[0] - walker.get_location()[0]) ** 2 +
                            (other_walker.get_location()[1] - walker.get_location()[1]) ** 2) ** 0.5

                # If the current distance is less than the minimum distance,
                # update the minimum distance and the nearest walker
                if distance < min_distance:
                    min_distance = distance
                    nearest_walker = other_walker
        # If no other walker is found, raise an exception
        if nearest_walker is None:
            raise ValueError("No other walkers in the simulation.")

        # Return the nearest walker
        return nearest_walker

    def choose_move(self, walker: Walker) -> None:
        """
        Determines the next move for a walker.

        This method is responsible for deciding the next move of a given walker. The move is determined based on the
        interaction type set for the simulation. If the interaction type is 'attract',
         the walker will have 20% probability to move towards the nearest walker.
          If the interaction type is 'repel', the walker will have 20% probability to move away from the nearest walker.
           If the interaction type is not set, the walker will move randomly.

        Parameters:
            walker (Walker): The Walker object for which to determine the next move.
        """
        # If no interaction type is set, move the walker randomly
        if self.__walkers_interaction is None:
            walker.move()
            return

        # Locate the nearest walker
        nearest_walker = self.locate_nearest_walker(walker)

        # Generate a random probability
        prob = random.random()

        # Set the distance for the move
        distance: Union[float, int] = 1
        if isinstance(walker, RandomDistanceWalker):
            distance = random.uniform(0.5, 1.5)

        # If the probability is equal or less than 0.2, move the walker towards or away from the nearest walker
        if prob <= 0.2:
            # Calculate the direction vector towards the nearest walker
            direction_vector = math.atan2(nearest_walker.get_location()[1] - walker.get_location()[1],
                                          nearest_walker.get_location()[0] - walker.get_location()[0])
            if direction_vector < 0:
                direction_vector += 2 * math.pi

            # If the interaction type is 'attract', move the walker towards the nearest walker
            if self.__walkers_interaction == 'attract':

                # If the walker can only move in cardinal directions,
                # round the direction vector to the nearest multiple of pi/2
                if not isinstance(walker, UnitWalker) or isinstance(walker, RandomDistanceWalker):
                    direction_vector = round(direction_vector / (math.pi / 2)) * (math.pi / 2)
                walker.set_position((walker.get_location()[0] + math.cos(direction_vector) * distance,
                                     walker.get_location()[1] + math.sin(direction_vector) * distance))
                if isinstance(walker, MemoryWalker):
                    walker.update_memory()

            # If the interaction type is 'repel', move the walker away from the nearest walker
            elif self.__walkers_interaction == 'repel':

                # If the walker can only move in cardinal directions,
                # round the direction vector to the nearest multiple of pi/2
                if not isinstance(walker, UnitWalker) or isinstance(walker, RandomDistanceWalker):
                    direction_vector = round(direction_vector / (math.pi / 2)) * (math.pi / 2)
                walker.set_position((walker.get_location()[0] - math.cos(direction_vector) * distance,
                                     walker.get_location()[1] - math.sin(direction_vector) * distance))
                if isinstance(walker, MemoryWalker):
                    walker.update_memory()

        # If the probability is greater than 0.2, move the walker randomly
        else:
            walker.move()

    def terrain_check(self, walker: Walker) -> Union[str, bool]:
        """
        Checks if a walker is on a specific terrain.

        This method checks if the given walker is on any of the terrains (grass, sand, or water) in the simulation.
        It does this by checking if the walker's current position intersects with the boundary of any terrain.
        If the walker is on a terrain, the method returns the type of that terrain as a string.
        If the walker is not on any terrain, the method returns False.

        Parameters:
            walker (Walker): The Walker object for which to check the terrain.

        Returns:
            Union[str, bool]: The type of the terrain ('grass', 'sand', 'water') if the walker is on a terrain,
            False otherwise.
        """
        # Check if the walker is on any water terrain
        for water in self.__waters:
            # If the walker's position intersects with the water's boundary, return 'water'
            if Point(walker.get_location()).intersects(water.get_boundary()):
                return 'water'

        # Check if the walker is on any sand terrain
        for sand in self.__sands:
            # If the walker's position intersects with the sand's boundary, return 'sand'
            if Point(walker.get_location()).intersects(sand.get_boundary()):
                return 'sand'

        # Check if the walker is on any grass terrain
        for grass in self.__grasses:
            # If the walker's position intersects with the grass's boundary, return 'grass'
            if Point(walker.get_location()).intersects(grass.get_boundary()):
                return 'grass'

        # If the walker is not on any terrain, return False
        return False

    @staticmethod
    def handle_terrain(walker: Walker, terrain: str) -> None:
        """
        Adjusts the walker's position based on the terrain type.

        This method is responsible for adjusting the position of a given walker based on the type of terrain it is on.
        If the walker is on 'water', it is moved to the origin (0, 0).
        If the walker is on 'sand', it is moved to the midpoint between its current and previous positions.
        If the walker is on 'grass', it is moved twice as far in the direction it was already moving.

        Parameters:
            walker (Walker): The Walker object whose position needs to be adjusted.
            terrain (str): The type of terrain the walker is on. This should be 'water', 'sand', or 'grass'.
        """
        # If the walker is on water, move it to the origin
        if terrain == 'water':
            walker.set_position((0, 0))

        # If the walker is on sand, move it to the midpoint between its current and previous positions
        elif terrain == 'sand':
            walker.set_position(((walker.get_prev_location()[0] + walker.get_location()[0]) / 2,
                                 (walker.get_prev_location()[1] + walker.get_location()[1]) / 2))

        # If the walker is on grass, move it twice as far in the direction it was already moving
        elif terrain == 'grass':
            vector = (walker.get_location()[0] - walker.get_prev_location()[0],
                      walker.get_location()[1] - walker.get_prev_location()[1])
            vector = (vector[0] * 2, vector[1] * 2)
            walker.set_position((walker.get_location()[0] + vector[0], walker.get_location()[1] + vector[1]))

        # If the walker is a MemoryWalker, update its memory after moving
        if isinstance(walker, MemoryWalker):
            walker.update_memory()

    def check_collision(self, walker) -> bool:
        """
        Checks if a walker collides with any obstacles in the simulation.

        This method iterates over all the obstacles in the simulation and checks if the given walker's trajectory
        intersects with any of the obstacles' boundaries. The walker's trajectory is represented as a LineString object,
        and each obstacle's boundary is also represented as a LineString object. If the walker's trajectory intersects
        with an obstacle's boundary, it means the walker collides with the obstacle.

        Parameters:
            walker (Walker): The Walker object for which to check for collisions. This object represents a walker
            in the simulation, and its trajectory is used to check for collisions with obstacles.

        Returns:
            bool: True if the walker collides with any obstacle, False otherwise. A collision is determined by checking
            if the walker's trajectory intersects with an obstacle's boundary.
        """
        for obstacle in self.__obstacles:
            # Create LineString representing walker's trajectory
            walker_trajectory = LineString([(walker.get_prev_location()), (walker.get_location())])

            # Create LineString representing obstacle's boundary
            obstacle_boundary = obstacle.get_boundary()

            # Check for intersection
            if walker_trajectory.intersects(obstacle_boundary):
                return True

        return False

    def gate_check(self, walker) -> None:
        """
        Checks if a walker is at an enchanted gate entrance and teleports it to the exit if so.

        This method iterates over all the enchanted gates in the simulation and checks if the given walker's trajectory
        intersects with any of the gates' boundaries. The walker's trajectory is represented as a LineString object,
        and each gate's boundary is also represented as a LineString object. If the walker's trajectory intersects
        with a gate's boundary, it means the walker is at the gate's entrance,
        and it is then teleported to the gate's exit.

        Parameters:
            walker (Walker): The Walker object for which to check for enchanted gate entrances.
            This object represents a walker in the simulation, and its trajectory is used to check
            for intersections with enchanted gates.

        """
        for gate in self.__enchanted_gates:
            # Create LineString representing walker's trajectory
            walker_trajectory = LineString([(walker.get_prev_location()), (walker.get_location())])

            # Create LineString representing obstacle's boundary
            gate_boundary = gate.get_boundary()

            # Check for intersection
            if walker_trajectory.intersects(gate_boundary):
                walker.set_position(gate.get_exit_location())
                if isinstance(walker, MemoryWalker):
                    walker.update_memory()

    def cross_y_check(self, walker_name, walker) -> None:
        """
        Checks if a walker crosses the y-axis and increments its counter if so.

        This method checks if the given walker has crossed the y-axis during its movement. A crossing is counted when a
        walker moves from one side of the y-axis to the other or if a walker touches the y-axis.
        The counter starts from -1 so the first movement from (0,0) will not be considered as a cross.
        If a crossing is detected, the method increments the y-axis crossing count for the walker.

        Parameters:
            walker_name (str): The unique name of the Walker object for which to check for y-axis crossings. This name
            is used as a key to access the walker's y-axis crossing count in the __crosses_y dictionary.

            walker (Walker): The Walker object for which to check for y-axis crossings. This object represents a walker
            in the simulation, and its current and previous positions are used to check for y-axis crossings.
        """
        if (walker.get_location()[0] * walker.get_prev_location()[0] < 0 or
                (walker.get_prev_location()[0] == 0 and walker.get_location()[0] != 0)):
            self.__crosses_y[walker_name] += 1

    def escape_check(self, walker_name, walker, i) -> None:
        """
        Checks if a walker has escaped and updates its escape time if not.

        This method is responsible for checking if a given walker has escaped from the origin.
        A walker is considered to have escaped if it is more than a certain distance away from the origin.
        The distance is determined by the escape radius of the walker. If the walker has not escaped,
        the method updates the escape time for the walker. The escape time is the number of moves it took
        for the walker to escape from the origin.

        Parameters:
            walker_name (str): The unique name of the Walker object for which to check for escape.
            This name is used as a key to access the walker's escape time in the __escape_times dictionary.

            walker (Walker): The Walker object for which to check for escape. This object represents a walker
            in the simulation, and its current location and escape radius are used to check for escape.

            i (int): The current move number. This is used to update the escape time for the walker
            if it has not escaped.
        """
        if not walker.escape_check():  # Check if the walker has escaped
            self.__escape_times[walker_name] = i  # Update the escape time if the walker has not escaped

    def simulation_results_update(self, walker_name, walker, i) -> None:
        """
        Updates the simulation results for a specific walker at a specific move.

        This method is responsible for updating the simulation results for a given walker at a given move.
        The results include the walker's current location, escape time, number of y-axis crossings,
        distance from the origin, and distances from the x and y axes. These results are stored in the __total_dict
        attribute, which is a nested dictionary where the first level keys are the unique names of the walkers,
        the second level keys are the move numbers, and the third level keys are the result types.

        Parameters:
            walker_name (str): The unique name of the Walker object for which to update the simulation results.
            This name is used as a key to access the walker's results in the __total_dict dictionary.

            walker (Walker): The Walker object for which to update the simulation results.
            This object represents a walker in the simulation, and its current location, escape time,
            and number of y-axis crossings are used to update the simulation results.

            i (int): The current move number. This is used as a key to access the results for the specific move in the
            __total_dict dictionary.
        """

        self.__total_dict[walker_name][i] = {
            'locations': walker.get_location(),
            'escape time': self.get_escape_times()[walker_name] if walker.escape_check() else None,
            'y crosses': max(0, self.get_crosses_y()[walker_name]),
            'distance from origin': (walker.get_location()[0] ** 2 + walker.get_location()[1] ** 2) ** 0.5,
            'distance from x': abs(walker.get_location()[1]),
            'distance from y': abs(walker.get_location()[0]),
        }

    def export_to_statistics(self, stat, i):
        """
        Exports the simulation results to a Statistics object.

        This method is responsible for exporting the simulation results to a Statistics object for further analysis.
        The results include the walker's current location, escape time, number of y-axis crossings,
        distance from the origin, and distances from the x and y axes for each move of the simulation.
        These results are stored in the __total_dict attribute of the Simulation class and are loaded into
        the Statistics object.

        Parameters:
            stat (Statistics): The Statistics object to which the simulation results are to be exported.
            This object is used to store and analyze the simulation results.

            i (int): The current move number. This is used to specify which move's results are to be exported.
        """
        stat.load_to_dict(self.__total_dict, i)

    def run_simulation(self) -> bool:
        """
        Runs the simulation for the specified number of moves.

        This method is responsible for running the entire simulation. It iterates over the specified number of moves,
        and for each move, it iterates over all the walkers in the simulation. For each walker,
        it determines the next move, checks the terrain, handles the terrain, checks for collisions,
        checks for enchanted gates, checks for y-axis crossings, checks for escape, and updates the simulation results.
        If a walker collides with an obstacle, it attempts to move the walker until it no longer collides
        with the obstacle or until the maximum number of collision attempts is reached.
        If the maximum number of collision attempts is reached for any walker,
        the simulation is terminated and the method returns False. If the simulation completes successfully,
        the method returns True.

        Returns:
            bool: True if the simulation completes successfully, False if the simulation is terminated due to a walker
            colliding with an obstacle too many times.
        """
        for i in range(1, self.__num_moves + 1):  # Iterate over the specified number of moves
            for walker_name in self.__walkers:  # Iterate over all walkers in the simulation
                walker = self.__walkers[walker_name]  # Get the walker object
                self.choose_move(walker)  # Determine the next move for the walker
                terrain = self.terrain_check(walker)  # Check if the walker is on any terrain
                # If the walker is on a terrain, handle the terrain
                self.handle_terrain(walker, terrain)
                collision_attempts = 0  # Initialize the collision attempts counter
                max_collision_attempts = 1000  # Maximum number of collision attempts before terminating the simulation
                while self.check_collision(walker):  # Check if the walker collides with any obstacles

                    # Check if the maximum collision attempts are reached
                    if collision_attempts >= max_collision_attempts:
                        print(
                            f"Maximum collision attempts reached for {walker_name}. Terminating simulation.")
                        return False  # Simulation terminated
                    walker.move_back()  # Move the walker back to its previous position
                    self.choose_move(walker)  # Determine the next move for the walker
                    terrain = self.terrain_check(walker)  # Check if the walker is on any terrain
                    # If the walker is on a terrain, handle the terrain
                    if isinstance(terrain, str):
                        self.handle_terrain(walker, terrain)
                    collision_attempts += 1  # Increment the collision attempts counter
                if isinstance(walker, MemoryWalker):
                    walker.update_memory()  # If the walker is a MemoryWalker, update its memory
                self.gate_check(walker)  # Check if the walker is at an enchanted gate entrance
                self.escape_check(walker_name, walker, i)  # Check if the walker has escaped
                self.cross_y_check(walker_name, walker)  # Check if the walker crosses the y-axis
                self.simulation_results_update(walker_name, walker, i)  # Update the simulation results
        return True  # Simulation completed successfully

    def reset(self) -> None:
        """
        Resets the simulation to its initial state.

        This method is responsible for resetting the entire simulation to its initial state.
        It iterates over all the walkers in the simulation, resetting each walker's position and escape status.
        It also resets the escape times, y-axis crossing counts, and simulation results for all walkers.

        Specifically, the method performs the following operations:
        1. For each walker in the simulation, it resets the walker's position to its initial position and sets
        its escape status to False.
        2. It resets the escape times for all walkers to None, indicating that no walker has escaped yet.
        3. It resets the y-axis crossing counts for all walkers to -1, indicating that no walker
        has crossed the y-axis yet.
        4. It resets the simulation results for all walkers, clearing all previously stored results.

        This method is typically called at the beginning of a new simulation run to ensure that the simulation
        starts from a clean state.
        """
        for walker_name in self.__walkers:  # Iterate over all walkers in the simulation
            self.__walkers[walker_name].reset_walker()  # Reset the walker's position and escape status
        self.__escape_times = {walker_name: None for walker_name in self.__walkers}  # Reset the escape times
        self.__crosses_y = {walker_name: -1 for walker_name in self.__walkers}  # Reset the y-axis crossing counts
        self.__total_dict = {walker_name: {} for walker_name in self.__walkers}  # Reset the simulation results
