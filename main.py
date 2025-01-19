import random
from simulation import *
from plot import *
from terrains import *
import json
import argparse
import os
from statistics import *
from typing import Any, List, Tuple, Optional
from walkers import *
from shapely.geometry import Point  # type: ignore


def load_config(config_file: str) -> dict:
    """
    Load configuration from a JSON file.

    This function reads a JSON file and returns its content as a dictionary. The JSON file should contain the
    configuration data for the simulation. If the file is not found or the JSON is not valid, the function will
    print an error message and terminate the program.

    Args:
        config_file (str): The path to the JSON file that contains the configuration data.

    Returns:
        dict: A dictionary that contains the configuration data. The keys and values in the dictionary depend on
        the structure of the JSON file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file does not contain valid JSON.
        PermissionError: If the file cannot be opened due to insufficient permissions.

    Example:
        config_data = load_config("config.json")
    """
    try:  # Try to open the file and load the JSON data
        with open(config_file, 'r') as f:  # Open the file in read mode
            config_data = json.load(f)  # Load the JSON data from the file
        return config_data  # Return the JSON data as a dictionary
    except FileNotFoundError:  # If the file is not found
        print(f"Error: Config file '{config_file}' not found.")  # Print an error message
        exit(1)  # Terminate the program
    except json.JSONDecodeError:  # If the JSON is not valid
        print(f"Error: Unable to parse JSON file '{config_file}'.")  # Print an error message
        exit(1)  # Terminate the program
    except PermissionError:  # If the file cannot be opened due to insufficient permissions
        print(f"Error: Permission denied when trying to open '{config_file}'. Check if you accidentally entered "
              f"a folder path instead of the full path to the JSON config file.")
        exit(1)  # Terminate the program


def get_walkers_from_json(data_dict: dict) -> List[Any]:
    """
    Get walker objects from JSON data.

    This function reads a dictionary that represents JSON data and creates walker objects based on the 'walker_types'
    field in the dictionary. The 'walker_types' field should be a list of dictionaries, where each dictionary
    represents a walker and has a 'name' field that specifies the type of the walker.

    If the walker type is "DirectionalBiasWalker", the function also calls the `get_probabilities` function to get
    the probabilities for the walker.

    If the walker type is not found in the global scope, the function prints an error message and terminates the
    program.

    If the 'walker_types' field is not found in the dictionary, the function prints an error message and terminates
    the program.

    Args:
        data_dict (dict): A dictionary that represents JSON data. The dictionary should have a 'walker_types' field
        that is a list of dictionaries.

    Returns:
        List[Any]: A list of walker objects. The type of the objects depends on the 'name' field in the 'walker_types'
        dictionaries.

    Raises:
        KeyError: If the 'walker_types' field is not found in the dictionary.

    Example:
        walkers = get_walkers_from_json(data_dict)
    """
    try:  # Try to get the walker types from the JSON data
        walkers_list = []  # Create an empty list to store the walker objects
        walker_names = [walker['name'] for walker in data_dict['walker_types']]  # Get the walker names from the data
        for walker in walker_names:  # Iterate over the walker names
            if walker == "DirectionalBiasWalker":  # If the walker type is DirectionalBiasWalker
                cls = globals()[walker]  # Get the class from the global scope
                instance = cls(get_probabilities())  # Create an instance of the walker with probabilities
                walkers_list.append(instance)  # Add the walker instance to the list
            else:  # If the walker type is not DirectionalBiasWalker
                cls = globals()[walker]  # Get the class from the global scope
                if cls:  # If the class is found
                    instance = cls()  # Create an instance of the walker
                    walkers_list.append(instance)  # Add the walker instance to the list
                else:  # If the class is not found
                    print(f"Error: Walker type '{walker}' not found.")  # Print an error message
                    exit(1)  # Terminate the program
        if not walkers_list:  # If no walkers were found
            print("Error: No walkers found in config file.")  # Print an error message
            exit(1)  # Terminate the program
        return walkers_list  # Return the list of walker objects
    except KeyError:  # If the 'walker_types' field is not found
        print("Error: Invalid JSON format for 'walker_types' in config file.")  # Print an error message
        exit(1)  # Terminate the program


def get_obstacles_from_json(data_dict: dict) -> Optional[List[Obstacle]]:
    """
    Get obstacle objects from JSON data.

    This function reads a dictionary that represents JSON data and creates obstacle objects based on the 'obstacles'
    field in the dictionary. The 'obstacles' field should be a list of dictionaries, where each dictionary
    represents an obstacle and has 'x', 'y', 'width', and 'height' fields that specify the properties of the obstacle.

    If the 'obstacles' field is not found in the dictionary, the function returns None.

    Args:
        data_dict (dict): A dictionary that represents JSON data. The dictionary should have an 'obstacles' field
        that is a list of dictionaries.

    Returns:
        List[Obstacle]: A list of obstacle objects. The properties of the objects depend on the 'x', 'y', 'width',
        and 'height' fields in the 'obstacles' dictionaries.
        None: If the 'obstacles' field is not found in the dictionary.

    Raises:
        KeyError: If the 'obstacles' field is not in a correct format the dictionary.

    Example:
        obstacles = get_obstacles_from_json(data_dict)
    """
    if 'obstacles' not in data_dict:  # If the 'obstacles' field is not found in the dictionary
        return None
    try:  # Try to get the obstacles from the JSON data
        obstacles_list = []  # Create an empty list to store the obstacle objects
        for obstacle in data_dict['obstacles']:  # Iterate over the obstacles in the data
            if (obstacle['x'] <= 0 <= obstacle['x'] + obstacle['width'] and
                    obstacle['y'] <= 0 <= obstacle['y'] + obstacle['height']):  # Check if the obstacle is at (0, 0)
                print("Error: Obstacle cannot be placed at (0, 0).")  # Print an error message
                exit(1)  # Terminate the program
            else:  # If the obstacle is not at (0, 0)

                # Create an obstacle object with the properties from the data and add it to the list
                obs = Obstacle(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
                obstacles_list.append(obs)
        return obstacles_list  # Return the list of obstacle objects
    except KeyError:  # If the JSON format is invalid
        print("Error: Invalid JSON format for 'obstacles' in config file.")  # Print an error message
        return None


def get_terrains_from_json(data_dict: dict) -> Tuple[List[Water], List[Sand], List[Grass]]:
    """
    Get terrain objects from JSON data.

    This function reads a dictionary that represents JSON data and creates terrain objects based on the 'waters',
    'sands', and 'grasses' fields in the dictionary. Each of these fields should be a list of dictionaries, where each
    dictionary represents a terrain and has 'x', 'y', 'width', and 'height' fields that specify the properties
    of the terrain.

    If any of the 'waters', 'sands', or 'grasses' fields are not found in the dictionary, the function returns None
    for that terrain type.

    Args:
        data_dict (dict): A dictionary that represents JSON data. The dictionary should have 'waters', 'sands',
        and 'grasses' fields that are lists of dictionaries.

    Returns:
        Tuple[List[Water], List[Sand], List[Grass]]: A tuple of lists of terrain objects. The properties of the
        objects depend on the 'x', 'y', 'width', and 'height' fields in the corresponding dictionaries.

    Raises:
        KeyError: If the 'waters', 'sands', or 'grasses' field is not in a correct format in the dictionary.
    Example:
        waters, sands, grasses = get_terrains_from_json(data_dict)
    """
    waters_list = sands_list = grasses_list = None  # Initialize the lists to None
    if 'waters' in data_dict:  # If the 'waters' field is found in the dictionary
        try:  # Try to get the waters from the JSON data
            waters_list = []  # Create an empty list to store the water objects
            for water in data_dict['waters']:  # Iterate over the waters in the data
                if (water['x'] <= 0 <= water['x'] + water['width'] and
                        water['y'] <= 0 <= water['y'] + water['height']):  # Check if the water is at (0, 0)
                    print("Error: Water cannot be placed at (0, 0).")  # Print an error message
                    exit(1)  # Terminate the program
            for water in data_dict['waters']:  # Iterate over the waters in the data
                wat = Water(water['x'], water['y'], water['width'], water['height'])  # Create a water object
                waters_list.append(wat)  # Add the water object to the list
        except KeyError:  # If the JSON format is invalid
            print("Error: Invalid JSON format for 'waters' in config file.")  # Print an error message
            exit(1)  # Terminate the program
    if 'sands' in data_dict:  # If the 'sands' field is found in the dictionary
        try:  # Try to get the sands from the JSON data
            sands_list = []  # Create an empty list to store the sand objects
            for sand in data_dict['sands']:  # Iterate over the sands in the data
                san = Sand(sand['x'], sand['y'], sand['width'], sand['height'])  # Create a sand object
                sands_list.append(san)  # Add the sand object to the list
        except KeyError:  # If the JSON format is invalid
            print("Error: Invalid JSON format for 'sands' in config file.")  # Print an error message
            exit(1)  # Terminate the program
    if 'grasses' in data_dict:  # If the 'grasses' field is found in the dictionary
        try:  # Try to get the grasses from the JSON data
            grasses_list = []  # Create an empty list to store the grass objects
            for grass in data_dict['grasses']:  # Iterate over the grasses in the data
                gra = Grass(grass['x'], grass['y'], grass['width'], grass['height'])  # Create a grass object
                grasses_list.append(gra)  # Add the grass object to the list
        except KeyError:  # If the JSON format is invalid
            print("Error: Invalid JSON format for 'grasses' in config file.")  # Print an error message
            exit(1)  # Terminate the program
    return waters_list, sands_list, grasses_list  # Return the lists of terrain objects


def get_gates_from_json(data_dict: dict) -> Optional[List[EnchantedGate]]:
    """
    Get enchanted gate objects from JSON data.

    This function reads a dictionary that represents JSON data and creates enchanted gate objects based on the
    'enchanted_gates' field in the dictionary. The 'enchanted_gates' field should be a list of dictionaries,
    where each dictionary represents an enchanted gate and has 'entrance_location', 'exit_location',
    'entrance_width', and 'entrance_height' fields that specify the properties of the enchanted gate.

    If the 'enchanted_gates' field is not found in the dictionary, the function returns None

    Args:
        data_dict (dict): A dictionary that represents JSON data. The dictionary should have an 'enchanted_gates'
        field that is a list of dictionaries.

    Returns:
        List[EnchantedGate]: A list of enchanted gate objects. The properties of the objects depend on the
        'entrance_location', 'exit_location', 'entrance_width', and 'entrance_height' fields in the
        'enchanted_gates' dictionaries.
        None: If the 'enchanted_gates' field is not found in the dictionary.

    Raises:
        KeyError: If the 'enchanted_gates' field is not in a correct format in the dictionary.

    Example:
        gates = get_gates_from_json(data_dict)
    """
    if 'enchanted_gates' not in data_dict:  # If the 'enchanted_gates' field is not found in the dictionary
        return None
    try:  # Try to get the enchanted gates from the JSON data
        gates_list = []  # Create an empty list to store the enchanted gate objects
        for enchanted_gate in data_dict['enchanted_gates']:  # Iterate over the enchanted gates in the data
            # Create an enchanted gate object with the properties from the data and add it to the list
            entrance_x = enchanted_gate['entrance_location']['x']
            entrance_y = enchanted_gate['entrance_location']['y']
            entrance_width = enchanted_gate['entrance_width']
            entrance_height = enchanted_gate['entrance_height']
            if ((entrance_x <= 0 <= entrance_x + entrance_width) and
                    (entrance_y <= 0 <= entrance_y + entrance_height)):  # Check if the gate is at (0, 0)
                print("Error: Enchanted gate entrance cannot be placed at (0, 0)")  # Print an error message
                exit(1)  # Terminate the program
            gate = EnchantedGate((entrance_x, entrance_y),  # Create an enchanted gate object
                                 (enchanted_gate['exit_location']['x'], enchanted_gate['exit_location']['y']),
                                 entrance_width, entrance_height)  # Create an enchanted gate object
            gates_list.append(gate)  # Add the enchanted gate object to the list
        return gates_list
    except KeyError as e:  # If the JSON format is invalid
        print(f"Error: Missing key {e} in 'enchanted_gates' in config file.")  # Print an error message
        exit(1)  # Terminate the program


def occupied_locations_check(gates: List[EnchantedGate], obstacles: List[Obstacle], waters: List[Water],
                             sands: List[Sand], grasses: List[Grass]) -> None:
    """
        Check if any objects overlap in the simulation.

        This function checks if any of the gates, obstacles, waters, sands, or grasses in the simulation overlap
        with each other. If any objects overlap, the function prints an error message and terminates the program.

        Args:
            gates (List[EnchantedGate]): A list of EnchantedGate objects.
            obstacles (List[Obstacle]): A list of Obstacle objects.
            waters (List[Water]): A list of Water objects.
            sands (List[Sand]): A list of Sand objects.
            grasses (List[Grass]): A list of Grass objects.

        Example:
            occupied_locations_check(gates, obstacles, waters, sands, grasses)
        """
    all_polygons = ([gate.get_boundary() for gate in gates] +
                    [obstacle.get_boundary() for obstacle in obstacles])  # Combine all polygons
    for i in range(len(all_polygons)):  # Iterate over the polygons
        for j in range(i + 1, len(all_polygons)):  # Iterate over the remaining polygons
            if all_polygons[i].intersects(all_polygons[j]):  # If the polygons intersect
                print("You have overlapping obstacles or gates. Please fix this in the config file.")
                exit(1)  # Terminate the program
    terrain_polygons = ([water.get_boundary() for water in waters] +
                        [sand.get_boundary() for sand in sands] +
                        [grass.get_boundary() for grass in grasses])  # Combine all terrain polygons
    for i in range(len(terrain_polygons)):  # Iterate over the terrain polygons
        for j in range(i + 1, len(terrain_polygons)):  # Iterate over the remaining terrain polygons
            if terrain_polygons[i].intersects(terrain_polygons[j]):  # If the terrain polygons intersect
                print("You have overlapping terrains. Please fix this in the config file.")
                exit(1)  # Terminate the program
    for gate in gates:  # Iterate over the gates
        exit_location = Point(gate.get_exit_location())  # Get the exit location as a Point
        for obstacle in obstacles:  # Iterate over the obstacles
            if obstacle.get_boundary().intersects(exit_location):  # If the exit location intersects with an obstacle
                print("A gate's exit location intersects with an obstacle. Please fix this in the config file.")
                exit(1)  # Terminate the program
        for other_gate in gates:  # Iterate over the other gates
            # If the exit location intersects with the same gate's entrance
            if other_gate == gate and other_gate.get_boundary().intersects(exit_location):
                print("A gate's exit location intersects with the gate's entrance."
                      " Please fix this in the config file.")
                exit(1)  # Terminate the program


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the simulation.

    This function uses the argparse module to parse command-line arguments. It expects four arguments:
    'num_simulations', 'num_steps', 'config_file', and 'stats_dir'.

    'num_simulations' is an integer that specifies the number of simulations to run.
    'num_steps' is an integer that specifies the number of steps for each simulation.
    'config_file' is a string that specifies the path to the JSON config file.
    'stats_dir' is a string that specifies the folder to save all the simulations stats.

    The function returns an argparse.Namespace object that contains the values of the arguments.

    If the arguments are not provided or are not in the correct format, the function will print an error message
    and terminate the program.

    Returns:
       argparse.Namespace: An object that contains the values of the parsed arguments.

    Raises:
       argparse.ArgumentError: If the arguments are not provided or are not in the correct format.

    Example:
        args = parse_arguments()
    """
    try:
        parser = argparse.ArgumentParser(description='Random walk simulation')  # Create an ArgumentParser object
        # Add the command-line arguments
        parser.add_argument('num_simulations', type=int,
                            help='Number of simulations to run (positive integer)')
        parser.add_argument('num_steps', type=int,
                            help='Number of steps for each simulation (positive integer)')
        parser.add_argument('config_file', type=str, help='Path to JSON config file (including file name)')
        parser.add_argument('stats_dir', type=str, help='Folder to save all the simulations stats')
        return parser.parse_args()  # Parse the arguments and return the values
    except argparse.ArgumentError as e:  # If the arguments are not provided or are not in the correct format
        print(f"Error: {e}")  # Print an error message
        exit(1)  # Terminate the program


def ask_interaction_type() -> Optional[str]:
    """
    Ask the user for the interaction type between walkers.

    This function prompts the user to specify whether they want to set an interaction between
    the walkers in the simulation.
    If the user chooses to set an interaction, the function further asks the user to specify the type of interaction,
    which can be either 'repel' or 'attract'.

    The function returns the chosen interaction type as a string, or None if the user chooses not to set an interaction.

    If the user's response is not 'y', 'yes', 'n', 'no', 'repel', or 'attract', the function will print an error message
    and ask again.

    Returns:
        str: The chosen interaction type ('repel' or 'attract') if the user chooses to set an interaction.
        None: If the user chooses not to set an interaction.

    Example:
        interaction_type = ask_interaction_type()
    """
    while True:  # Loop until a valid response is received
        walkers_interaction = input("would you like to set an interaction between the walkers? y/n: ")  # Ask the user
        if walkers_interaction == 'n' or walkers_interaction == 'no':  # If the user chooses not to set an interaction
            return None
        elif walkers_interaction == 'y' or walkers_interaction == 'yes':  # If the user chooses to set an interaction
            while True:  # Loop until a valid response is received
                interaction_type = input("Choose the interaction type: 'repel' or 'attract': ")  # Ask the user
                if interaction_type == 'repel' or interaction_type == 'attract':  # If the response is valid
                    return interaction_type  # Return the interaction type
                else:  # If the response is invalid
                    print("Invalid response. Please choose 'repel' or 'attract'.")  # Print an error message
        else:  # If the response is invalid
            print("Invalid response. Please choose 'y' or 'n'.")  # Print an error message


def get_probabilities() -> List[float]:
    """
    Get probabilities for DirectionalBiasWalker.

    This function prompts the user to input the probabilities for the DirectionalBiasWalker. The probabilities should
    be for the following directions: DOWN, UP, RIGHT, LEFT, ORIGIN. The probabilities should be non-negative numbers
    and should be separated by commas.

    The function returns the probabilities as a list of floats.

    If the user's input is not in the correct format, the function will print an error message and ask again.

    Returns:
        List[float]: A list of probabilities for the DirectionalBiasWalker.

    Example:
        probabilities = get_probabilities()
    """
    while True:  # Loop until a valid input is received
        probs = input("""You selected a DirectionalBiasWalker.    
    Choose the probabilities for it (format: DOWN,UP,RIGHT,LEFT,ORIGIN): """)  # Ask the user
        split_list = probs.split(",")  # Split the input by commas
        if len(split_list) != 5:  # If the input does not contain exactly five probabilities
            print("Input should contain exactly five probabilities separated by commas.")  # Print an error message
            continue  # Ask again
        try:
            float_list = [float(item) for item in split_list]  # Convert the input to a list of floats
        except ValueError:  # If the conversion to float fails
            print("All probabilities should be valid numbers.")  # Print an error message
            continue  # Ask again
        if any(num < 0 for num in float_list):  # If any of the probabilities are negative
            print("Probabilities should be non-negative numbers.")  # Print an error message
            continue  # Ask again
        if all(num == 0 for num in float_list):  # If all probabilities are zero
            print("At least one probability should be greater than 0.")  # Print an error message
            continue  # Ask again
        return float_list  # Return the list of probabilities


def load_sim_objects(data_dict: dict, sim: Simulation) -> None:
    """
    Load simulation objects from a dictionary.

    This function takes a dictionary and a Simulation object as parameters. It uses the dictionary to create walker,
    obstacle, and enchanted gate objects and adds them to the simulation. It also adds water, sand, and grass terrains
    to the simulation if they are present in the dictionary.

    The dictionary should be structured as follows:
    - 'walker_types': a list of dictionaries, each representing a walker.
    - 'obstacles': a list of dictionaries, each representing an obstacle.
    - 'enchanted_gates': a list of dictionaries, each representing an enchanted gate.
    - 'waters', 'sands', 'grasses': lists of dictionaries, each representing a terrain.

    The function does not return anything. It modifies the Simulation object in-place.

    Args:
        data_dict (dict): A dictionary that contains the data for the simulation objects.
        sim (Simulation): A Simulation object to which the simulation objects will be added.

    Example:
        load_sim_objects(data_dict, sim)
    """
    for walker in get_walkers_from_json(data_dict):  # Iterate over the walkers
        sim.add_walker(walker)  # Add the walker to the simulation
    obstacles = get_obstacles_from_json(data_dict)  # Get the obstacles from the data
    if obstacles is None:  # If there are no obstacles
        obstacles = []  # Initialize the obstacles list
    for obstacle in obstacles:  # Iterate over the obstacles
        sim.add_obstacle(obstacle)  # Add the obstacle to the simulation
    gates = get_gates_from_json(data_dict)  # Get the gates from the data
    if gates is None:  # If there are no gates
        gates = []  # Initialize the gates list
    for enchanted_gate in gates:  # Iterate over the enchanted gates
        sim.add_enchanted_gate(enchanted_gate)  # Add the enchanted gate to the simulation

    waters_list, sands_list, grasses_list = get_terrains_from_json(data_dict)  # Get the terrains from the data
    if waters_list is not None:  # If there are water terrains
        for water in waters_list:  # Iterate over the water terrains
            sim.add_water(water)  # Add the water terrain to the simulation
    if sands_list is not None:  # If there are sand terrains
        for sand in sands_list:  # Iterate over the sand terrains
            sim.add_sand(sand)  # Add the sand terrain to the simulation
    if grasses_list is not None:  # If there are grass terrains
        for grass in grasses_list:  # Iterate over the grass terrains
            sim.add_grass(grass)  # Add the grass terrain to the simulation
    occupied_locations_check(sim.get_enchanted_gates(), sim.get_obstacles(), sim.get_waters(),
                             sim.get_sands(), sim.get_grasses())  # Check for overlapping objects


def save_json_with_index(data: dict, folder_path: str, json_name: str) -> None:
    """
    Save JSON data to a file, appending an index if the file already exists.

    This function takes JSON data, a folder path, and a JSON file name as parameters. It saves the JSON data to a file
    in the specified folder. If a file with the same name already exists in the folder, the function appends an index
    to the file name and tries again.

    If the specified folder does not exist, the function creates it.

    The function does not return anything. It modifies the file system by creating a new file or overwriting an existing
    one.

    Args:
        data (dict): The JSON data to save. It should be a dictionary that can be serialized to JSON.
        folder_path (str): The path to the folder where the file should be saved.
        json_name (str): The name of the JSON file. It should include the '.json' extension.

    Example:
        save_json_with_index(data, "/path/to/folder", "file.json")
    """
    if not os.path.exists(folder_path):  # If the folder does not exist
        os.makedirs(folder_path)  # Create the folder
    file_path = os.path.join(folder_path, json_name)  # Create the file path
    index = 1  # Initialize the index
    while os.path.exists(file_path):  # While the file already exists
        base, ext = os.path.splitext(json_name)  # Split the file name into base and extension
        file_path = os.path.join(folder_path, f"{base}_{index}{ext}")  # Add the index to the file name
        index += 1  # Increment the index
    with open(file_path, 'w') as json_file:  # Open the file in write mode
        json.dump(data, json_file)  # Write the JSON data to the file


def ask_sim_plot() -> bool:
    """
    Ask the user if they want to plot a simulation.

    This function prompts the user to specify whether they want to plot the simulation or not. The user should respond
    with 'w' or 'watch' to plot the simulation, or 's' or 'skip' to not plot the simulation.

    The function returns True if the user chooses to plot the simulation, and False otherwise.

    If the user's response is not 'w', 'watch', 's', or 'skip', the function will print an error message and ask again.

    Returns:
        bool: True if the user chooses to plot the simulation, False otherwise.

    Example:
        plot_simulation = ask_sim_plot()
    """
    while True:  # Loop until a valid response is received
        plot_sim = input('Would you like to watch or to skip all simulations? w/s: ')  # Ask the user
        if plot_sim == 'w' or plot_sim == 'watch':  # If the user chooses to plot the simulation
            return True  # Return True
        elif plot_sim == 's' or plot_sim == 'skip':  # If the user chooses not to plot the simulation
            return False  # Return False
        else:  # If the response is invalid
            print("Invalid response. Please enter 'w' or 's'.")  # Print an error message


def ask_stats_plot(stats: Statistics) -> None:
    """
    Ask the user if they want to plot statistics.

    This function prompts the user to specify whether they want to plot the statistics of the simulation or not.
    The user should respond with 'y' or 'yes' to plot the statistics, or 'n' or 'no' to not plot the statistics.

    If the user chooses to plot the statistics, the function further asks the user to specify the type of statistics
    to plot, which can be one of the following:
    1. Average walker distance from origin
    2. Average escape time
    3. Average walker distance along the x-axis
    4. Average walker distance along the y-axis
    5. Average number of times crossing the y-axis

    The function does not return anything. It modifies the state of the Statistics object by plotting the chosen
    statistics.

    If the user's response is not 'y', 'yes', 'n', 'no', or a valid statistic number, the function will print an error
    message and ask again.

    Args:
        stats (Statistics): A Statistics object that contains the statistics of the simulation.

    Example:
        ask_stats_plot(stats)
    """
    plot_dict = {'1': (plot_origin_distance, stats.average_walker_distance_origin),
                 '2': (plot_time_to_escape, stats.average_escape_time),
                 '3': (plot_x_distance, stats.average_walker_distance_x),
                 '4': (plot_y_distance, stats.average_walker_distance_y),
                 '5': (plot_y_crosses, stats.avg_cross_y_axis)}  # Dictionary of plot functions
    while True:  # Loop until the user chooses to stop
        response = input('Would you like to see a plotting of one of your statistics? y/n: ')  # Ask the user
        if response == 'n' or response == 'no':  # If the user chooses not to plot the statistics
            break  # Exit the loop
        elif response == 'y' or response == 'yes':  # If the user chooses to plot the statistics
            while True:  # Loop until a valid response is received
                plot_number = input('''choose a number:
                                    1 - Average distance from origin
                                    2 - Average escape time from radius 10
                                    3 - Average distance from x axis
                                    4 - Average distance from y axis
                                    5 - Average crosses of y axis
                                    6 - End the program
                                    ''')  # Ask the user

                if plot_number == '6':  # If the user chooses to stop
                    return  # Exit the function
                elif plot_number in plot_dict:  # If the response is a valid statistic number
                    plot_dict[plot_number][0](plot_dict[plot_number][1]())  # Plot the chosen statistic
                else:  # If the response is invalid
                    print("Invalid response. Please enter a number between 1 and 6")  # Print an error message
        else:  # If the response is invalid
            print('Invalid response. Please choose y/n')  # Print an error message


def save_stats(stats: Statistics, args: argparse.Namespace) -> None:
    """
    Ask the user if they want to save statistics and save them if confirmed.

    This function prompts the user to specify whether they want to save the statistics of the simulation or not.
    The user should respond with 'y' or 'yes' to save the statistics, or 'n' or 'no' to not save the statistics.

    If the user chooses to save the statistics, the function saves the following statistics to JSON files:
    - Average distance from origin
    - Average escape time from radius 10
    - Average distance from x-axis
    - Average distance from y-axis
    - Average crosses of y-axis

    The function does not return anything. It modifies the file system by creating new files or overwriting existing
    ones.

    Args:
        stats (Statistics): A Statistics object that contains the statistics of the simulation.
        args (argparse.Namespace): An object that contains the values of the parsed command-line arguments. It should
        have a 'stats_dir' attribute that specifies the directory where the statistics files should be saved.

    Example:
        save_stats(stats, args)
    """
    while True:  # Loop until a valid response is received
        save = input('Would you like to save the statistics? y/n: ')  # Ask the user
        if save == 'y' or save == 'yes':  # If the user chooses to save the statistics
            print('exporting stats to json files...')  # Print a message

            # Save the statistics to JSON files
            save_json_with_index(stats.average_walker_distance_origin(),
                                 args.stats_dir, 'average_walker_distance_origin.json')
            save_json_with_index(stats.average_escape_time(), args.stats_dir, 'average_escape_time.json')
            save_json_with_index(stats.average_walker_distance_x(), args.stats_dir, 'average_walker_distance_x.json')
            save_json_with_index(stats.average_walker_distance_y(), args.stats_dir, 'average_walker_distance_y.json')
            save_json_with_index(stats.avg_cross_y_axis(), args.stats_dir, 'average_crosses_y_axis.json')
            return  # Exit the function
        elif save == 'n' or save == 'no':  # If the user chooses not to save the statistics
            return  # Exit the function
        else:  # If the response is invalid
            print("Invalid response. Please enter 'y' or 'n'.")  # Print an error message


def main() -> None:
    """
    Main function to run the simulation.

    This function is the entry point for running the simulation. It performs the following steps:
    1. Parses command-line arguments using the `parse_arguments` function. The arguments should specify the number of
       simulations to run, the number of steps for each simulation, the path to the JSON config file, and the directory
       where the statistics files should be saved.
    2. Creates a Statistics object to store the statistics of the simulation.
    3. Creates a Simulation object with the number of steps specified in the command-line arguments.
    4. Loads the simulation objects (walkers, obstacles, enchanted gates, and terrains) from the JSON config file and
       adds them to the Simulation object.
    5. If there is more than one walker in the simulation, it asks the user to specify the interaction type between the
       walkers.
    6. Asks the user whether they want to watch the simulation or not.
    7. Runs the specified number of simulations, printing a message for each simulation.
    8. After all simulations have been run, it asks the user whether they want to plot the statistics of the simulation.
    9. Finally, it asks the user whether they want to save the statistics of the simulation to JSON files.

    The function does not return anything. It modifies the state of the Simulation and Statistics objects, and it may
    modify the file system by creating new files or overwriting existing ones.

    Example:
        main()
    """
    args = parse_arguments()  # Parse the command-line arguments
    stats = Statistics()  # Create a Statistics object
    sim = Simulation(args.num_steps)  # Create a Simulation object with the number of steps
    load_sim_objects(load_config(args.config_file), sim)  # Load the simulation objects from the JSON config file
    if len(sim.get_walkers()) > 1:  # If there is more than one walker
        interaction_type = ask_interaction_type()  # Ask the user for the interaction type
        if interaction_type is not None:  # If the user chooses to set an interaction
            sim.set_interaction(interaction_type)  # Set the interaction type
    watch_sim = ask_sim_plot()  # Ask the user if they want to watch the simulation
    print('running all simulations...')  # Print a message
    for i in range(1, args.num_simulations + 1):  # Iterate over the number of simulations
        print(f'Running simulation {i}...')  # Print a message
        if watch_sim:  # If the user wants to watch the simulation
            if sim.run_simulation():  # If the simulation runs successfully
                anim = plot_simulation(sim)  # Plot the simulation
                plt.show()
                sim.export_to_statistics(stats, i)  # Export the simulation data to statistics
                watch_sim = ask_sim_plot()  # Ask the user if they want to watch the next simulation
            else:  # If the simulation terminates early
                print(f"Simulation {i} terminated early and will not be included in statistics.")  # Print a message
        else:  # If the user does not want to watch the simulation
            if sim.run_simulation():  # If the simulation runs successfully
                sim.export_to_statistics(stats, i)  # Export the simulation data to statistics
            else:  # If the simulation terminates early
                print(f"Simulation {i} terminated early and will not be included in statistics.")  # Print a message
        sim.reset()  # Reset the simulation for the next run
    save_stats(stats, args)  # Ask the user if they want to save the statistics and save them if confirmed
    ask_stats_plot(stats)  # Ask the user if they want to plot the statistics


# Entry point of the script
if __name__ == "__main__":
    main()
