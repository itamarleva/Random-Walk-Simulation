from typing import Dict, Any, Tuple, Union
import numpy as np


class Statistics:
    """
    A class used to perform statistical analysis on simulation data.

    Attributes
    ----------
    __total_dict : dict
        A dictionary to store all the simulation data.

    Methods
    -------
    load_to_dict(dicti: Dict[str, Dict[int, Dict[str, Any]]], i: int) -> None:
        Loads data from a dictionary into the total dictionary.

    get_total_dict() -> Dict[str, Dict[int, Dict[str, Any]]]:
        Returns the total dictionary containing all loaded data.

    average_escape_time() -> Dict[str, Tuple[Union[float, int], int]]:
        Calculates the average escape time from radius 10 of the origin for each walker type.

    _average_walker_distance(distance_key: str) -> dict:
        Helper method to calculate average walker distance for a given distance key.

    average_walker_distance_origin() -> dict:
        Calculates the average distance of walkers from the origin.

    average_walker_distance_x() -> dict:
        Calculates the average distance of walkers along the x-axis.

    average_walker_distance_y() -> dict:
        Calculates the average distance of walkers along the y-axis.

    avg_cross_y_axis() -> Dict[str, Dict[str, float]]:
        Calculates the average number of times walkers cross the y-axis.
    """

    def __init__(self):
        """
        Initializes the Statistics object with an empty total dictionary.
        """
        self.__total_dict = dict()

    def load_to_dict(self, dicti: Dict[str, Dict[int, Dict[str, Any]]], i: int) -> None:
        """
        Load data from a dictionary into the total dictionary.

        This method is used to load simulation data from an input dictionary into the total dictionary.
        The input dictionary is expected to contain simulation data for a specific walker type.
        The method iterates over the input dictionary, and for each walker type, it checks if the walker type
        already exists in the total dictionary. If it does, it adds the new simulation data to the existing data.
        If it doesn't, it creates a new entry in the total dictionary for the walker type and adds the simulation data.

        Args:
            dicti (Dict[str, Dict[int, Dict[str, Any]]]): Input dictionary containing simulation data.
                The dictionary is expected to be structured as follows:
                {
                    'walker_type1': {
                        'simulation_number1': {
                            'data_key1': 'data_value1',
                            'data_key2': 'data_value2',
                            ...
                        },
                        'simulation_number2': {
                            'data_key1': 'data_value1',
                            'data_key2': 'data_value2',
                            ...
                        },
                        ...
                    },
                    'walker_type2': {
                        'simulation_number1': {
                            'data_key1': 'data_value1',
                            'data_key2': 'data_value2',
                            ...
                        },
                        ...
                    },
                    ...
                }
            i (int): Index indicating the simulation number. This is used as a key in the total dictionary
                to store the simulation data from the input dictionary.
        """
        for walker_name, walker_data in dicti.items():  # Iterate over walker types in the input dictionary
            if walker_name not in self.__total_dict:  # Check if walker type already exists in the total dictionary
                # If it doesn't, create a new entry and add the simulation data
                self.__total_dict[walker_name] = {i: walker_data}

            else:  # If the walker type already exists in the total dictionary
                self.__total_dict[walker_name][i] = walker_data  # Add the simulation data to the existing entry

    def get_total_dict(self) -> Dict[str, Dict[int, Dict[str, Any]]]:
        """
        Returns the total dictionary containing all loaded data.

        This method is used to retrieve the total dictionary that contains all the simulation data loaded
        using the `load_to_dict` method.

        Each key in the outermost dictionary is a walker type. The value associated with each walker type
        is another dictionary, where each key is a simulation number and the value is a dictionary of
        simulation data for that simulation.

        Returns:
            Dict[str, Dict[int, Dict[str, Any]]]: Total dictionary containing all loaded data.
        """
        return self.__total_dict

    def average_escape_time(self) -> Dict[str, Tuple[Union[float, int], int]]:
        """
        Calculates the average escape time from radius 10 of the origin for each walker type.

        This method iterates over all walker types in the total dictionary. For each walker type, it iterates over all
        simulations. For each simulation, it iterates over all steps and collects the escape times. If no escape times
        are found for a simulation, it increments the unsuccessful count. If escape times are found, it calculates the
        average escape time for the simulation and adds it to the list of successful escapes. Finally, it calculates the
        average escape time across all successful escapes for the walker type. If no successful escapes are found, it
        sets the average escape time to 0.

        Returns:
            Dict[str, Tuple[Union[float, int], int]]: A dictionary where each key is a walker type and each value is a
            tuple containing the average escape time and the unsuccessful count for the walker type.
        """
        escape_data = {}  # Initialize dictionary to store average escape times and unsuccessful counts
        for walker_type, simulations in self.__total_dict.items():  # Iterate over walker types in the total dictionary
            successful_escapes = []  # Initialize list to store successful escape times
            unsuccessful_count = 0  # Initialize count for unsuccessful simulations
            for simulation in simulations.values():  # Iterate over simulations for the walker type
                escape_times = [step_data['escape time'] for step_data in simulation.values() if
                                step_data['escape time'] is not None]  # Collect escape times
                if not escape_times:  # Check if no escape times were found for the simulation
                    unsuccessful_count += 1  # Increment unsuccessful count
                else:  # If escape times were found
                    average_escape_time = sum(escape_times) / len(escape_times)  # Calculate average escape time
                    successful_escapes.append(average_escape_time)  # Add average escape time to the list
            if successful_escapes:  # Check if successful escapes were found
                average_escape_time = sum(successful_escapes) / len(successful_escapes)  # Calculate average escape time
            else:  # If no successful escapes were found
                average_escape_time = 0  # Set average escape time to 0
            escape_data[walker_type] = (average_escape_time, unsuccessful_count)  # Add data to the dictionary
        return escape_data  # Return the dictionary

    def average_walker_distance(self, distance_key: str) -> dict:
        """
        Helper method to calculate average walker distance for a given distance key.

        This method calculates the average distance of walkers for a given distance key. The distance key can be any key
        in the simulation data that represents a distance, such as 'distance from origin', 'distance from x', or
        'distance from y'. The method iterates over all walker types in the total dictionary. For each walker type,
        it iterates over all simulations. For each simulation, it iterates over all steps and collects the distances.
        It then calculates the average distance for each step across all simulations for the walker type.

        Args:
            distance_key (str): Key indicating the type of distance to calculate. This should be a key in the simulation
            data that represents a distance.

        Returns:
            dict: A dictionary where each key is a walker type and each value is another dictionary. In the inner
            dictionary, each key is a step number (as a string) and each value is the average distance for that step.
        """
        averages = {}  # Initialize dictionary to store average distances
        for walker, simulations in self.__total_dict.items():  # Iterate over walker types in the total dictionary
            distance_counts = np.zeros(
                len(next(iter(simulations.values()))))  # Initialize array to store distance counts for each step
            total_simulations = len(simulations)  # Get total number of simulations for the walker type

            for sim in simulations.values():  # Iterate over simulations for the walker type
                for step, step_data in sim.items():  # Iterate over steps in the simulation
                    distance = step_data[distance_key]  # Get the distance for the step
                    distance_counts[int(step) - 1] += distance  # Increment count for the corresponding step

            averages[walker] = {
                str(step): distance_counts[i] / total_simulations for i, step in
                enumerate(range(1, len(distance_counts) + 1))}  # Calculate average distance for each step
        return averages

    def average_walker_distance_origin(self) -> dict:
        """
        Calculates the average distance of walkers from the origin for each step.

        This method uses the helper method `average_walker_distance` with the distance key set to
        'distance from origin'.
        The 'distance from origin' key in the simulation data represents the distance of a walker from the origin.

        The method iterates over all walker types in the total dictionary. For each walker type, it iterates over all
        simulations. For each simulation, it iterates over all steps and collects the distances from the origin.
        It then calculates the average distance from the origin for each step across all simulations for
        the walker type.

        Returns:
            dict: A dictionary where each key is a walker type and each value is another dictionary. In the inner
            dictionary, each key is a step number (as a string) and each value is the average distance from the origin
            for that step.
        """
        return self.average_walker_distance('distance from origin')

    def average_walker_distance_x(self) -> dict:
        """
        Calculates the average distance of walkers along the x-axis for each step.

        This method uses the helper method `average_walker_distance` with the distance key set to 'distance from x'.
        The 'distance from x' key in the simulation data represents the distance of a walker from the x-axis.

        The method iterates over all walker types in the total dictionary. For each walker type, it iterates over all
        simulations. For each simulation, it iterates over all steps and collects the distances from the x-axis.
        It then calculates the average distance from the x-axis for each step across all simulations for
        the walker type.

        Returns:
            dict: A dictionary where each key is a walker type and each value is another dictionary. In the inner
            dictionary, each key is a step number (as a string) and each value is the average distance from the x-axis
            for that step.
        """
        return self.average_walker_distance('distance from x')

    def average_walker_distance_y(self) -> dict:
        """
        Calculates the average distance of walkers along the y-axis for each step.

        This method uses the helper method `average_walker_distance` with the distance key set to 'distance from y'.
        The 'distance from y' key in the simulation data represents the distance of a walker from the y-axis.

        The method iterates over all walker types in the total dictionary. For each walker type, it iterates over all
        simulations. For each simulation, it iterates over all steps and collects the distances from the y-axis.
        It then calculates the average distance from the y-axis for each step across all simulations for
        the walker type.

        Returns:
            dict: A dictionary where each key is a walker type and each value is another dictionary. In the inner
            dictionary, each key is a step number (as a string) and each value is the average distance from the y-axis
            for that step.
        """
        return self.average_walker_distance('distance from y')

    def avg_cross_y_axis(self) -> Dict[str, Dict[str, float]]:
        """
        Calculates the average number of times walkers cross the y-axis for each step.

        This method iterates over all walker types in the total dictionary. For each walker type, it iterates over all
        simulations. For each simulation, it iterates over all steps and collects the number of times the walker crosses
        the y-axis. It then calculates the average number of y-axis crossings for each step across all simulations for
        the walker type.

        The 'y crosses' key in the simulation data represents the number of times a walker crosses the y-axis.

        Returns:
            Dict[str, Dict[str, float]]: A dictionary where each key is a walker type and each value is
            another dictionary.
            In the inner dictionary, each key is a step number (as a string) and each value is the average number
            of times the walker crosses the y-axis for that step.
        """
        averages: Dict[str, Dict[str, float]] = {}  # Initialize dictionary to store average y-axis crossings
        for walker, simulations in self.__total_dict.items():  # Iterate over walker types in the total dictionary
            averages[walker] = {}  # Initialize dictionary to store average y-axis crossings for the walker type
            crossing_counts = np.zeros(
                len(next(iter(simulations.values()))))  # Initialize array to store crossing counts for each step
            total_simulations = len(simulations)  # Get total number of simulations for the walker type

            for sim in simulations.values():  # Iterate over simulations for the walker type
                for step, step_data in sim.items():  # Iterate over steps in the simulation
                    crossings = step_data['y crosses']  # Get the number of y-axis crossings for the step
                    crossing_counts[int(step) - 1] += crossings  # Increment count for the corresponding step

            averages[walker] = {
                str(step): crossing_counts[i] / total_simulations for i, step in
                enumerate(range(1, len(crossing_counts) + 1))}  # Calculate average y-axis crossings for each step
        return averages
