from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from terrains import *  # Importing necessary classes
from simulation import Simulation  # Importing the Simulation class
import numpy as np
from matplotlib.animation import FuncAnimation


def plot_obstacles(obstacles: List[Obstacle]) -> None:
    """
    Plots the obstacles in the simulation on a matplotlib plot.

    This function iterates over a list of Obstacle objects. For each obstacle, it creates a rectangle patch
    on the current plot. The position and dimensions of the rectangle correspond to the position and dimensions
    of the obstacle. The color of the rectangle is set to red to represent an obstacle.

    Args:
        obstacles (List[Obstacle]): A list of Obstacle objects representing the obstacles in the simulation.

    Returns:
        None

    Note:
        This function is called inside the plot_simulation() function.
        It is used to visualize the obstacles in the plot.
    """
    for obstacle in obstacles:  # Iterate over the list of obstacles
        # Add a rectangle patch to the plot for each obstacle
        plt.gca().add_patch(plt.Rectangle((obstacle.get_position()),
                                          obstacle.get_dimensions()[0], obstacle.get_dimensions()[1], color='red'))


def plot_grasses(grasses: List[Grass]) -> None:
    """
    Plots the grass tiles in the simulation on a matplotlib plot.

    This function iterates over a list of Grass objects. For each grass, it creates a rectangle patch
    on the current plot. The position and dimensions of the rectangle correspond to the position and dimensions
    of the grass tile. The color of the rectangle is set to green to represent a grass tile.

    Args:
        grasses (List[Grass]): A list of Grass objects representing the grass tiles in the simulation.

    Returns:
        None

    Note:
        This function is called inside the plot_simulation() function.
        It is used to visualize the grass tiles in the plot.
    """
    for grass in grasses:  # Iterate over the list of grass tiles
        # Add a rectangle patch to the plot for each grass tile
        plt.gca().add_patch(plt.Rectangle((grass.get_position()),
                                          grass.get_dimensions()[0], grass.get_dimensions()[1], color='green'))


def plot_water(waters: List[Water]) -> None:
    """
    Plots the water tiles in the simulation on a matplotlib plot.

    This function iterates over a list of Water objects. For each water, it creates a rectangle patch
    on the current plot. The position and dimensions of the rectangle correspond to the position and dimensions
    of the water tile. The color of the rectangle is set to blue to represent a water tile.

    Args:
        waters (List[Grass]): A list of Water objects representing the water tiles in the simulation.

    Returns:
        None

    Note:
        This function is called inside the plot_simulation() function.
        It is used to visualize the water tiles in the plot.
    """
    for water_tile in waters:  # Iterate over the list of water tiles
        # Add a rectangle patch to the plot for each water tile
        plt.gca().add_patch(plt.Rectangle((water_tile.get_position()),
                                          water_tile.get_dimensions()[0], water_tile.get_dimensions()[1], color='blue'))


def plot_sand(sands: List[Sand]) -> None:
    """
    Plots the sand tiles in the simulation on a matplotlib plot.

    This function iterates over a list of Sand objects. For each sand, it creates a rectangle patch
    on the current plot. The position and dimensions of the rectangle correspond to the position and dimensions
    of the sand tile. The color of the rectangle is set to yellow to represent a sand tile.

    Args:
        sands (List[Sand]): A list of Sand objects representing the sand tiles in the simulation.

    Returns:
        None

    Note:
        This function is called inside the plot_simulation() function.
        It is used to visualize the sand tiles in the plot.
    """
    for sand_tile in sands:  # Iterate over the list of sand tiles
        # Add a rectangle patch to the plot for each sand tile
        plt.gca().add_patch(plt.Rectangle((sand_tile.get_position()),
                                          sand_tile.get_dimensions()[0], sand_tile.get_dimensions()[1], color='yellow'))


def plot_gates(gates: List[EnchantedGate]) -> None:
    """
    Plots the enchanted gates in the simulation on a matplotlib plot.

    This function iterates over a list of EnchantedGate objects. For each gate, it creates a rectangle patch
    on the current plot. The position and dimensions of the rectangle correspond to the entrance location and dimensions
    of the gate. The color of the rectangle is set to purple to represent an enchanted gate.

    Additionally, the exit of each gate is represented as a small circle on the plot, and a line is drawn from the
    entrance to the exit of each gate, also in purple.

    Args:
        gates (List[EnchantedGate]): A list of EnchantedGate objects representing the enchanted gates in the simulation.

    Returns:
        None

    Note:
        This function is called inside the plot_simulation() function.
        It is used to visualize the sand tiles in the plot.
    """
    for gate in gates:  # Iterate over the list of enchanted gates
        # Draw entrance as a rectangle
        plt.gca().add_patch(plt.Rectangle((gate.get_entrance_location()),
                                          gate.get_dimensions()[0], gate.get_dimensions()[1], color='purple'))
        # Draw exit as a small circle
        plt.plot(*gate.get_exit_location(), marker='o', color='purple')
        # Draw a line from entrance to exit
        plt.plot([gate.get_entrance_location()[0], gate.get_exit_location()[0]],
                 [gate.get_entrance_location()[1], gate.get_exit_location()[1]], color='purple')


def plot_terrains(sim: Simulation):
    """
    Plots the different terrains in the simulation on a matplotlib plot.

    This function takes a Simulation object as an argument and calls the respective plot functions for each type of
    terrain present in the simulation. These terrains include grass, sand, water, enchanted gates, and obstacles.
    Each of these terrains is represented by a different color on the plot.

    The function does not return any value but modifies the current matplotlib plot in-place.

    Args:
        sim (Simulation): A Simulation object representing the current state of the simulation.

    Returns:
        None

    Note:
        This function modifies the current matplotlib plot in-place. It is called inside the plot_simulation()
        function and is used to visualize the different terrains in the plot.
    """
    plot_grasses(sim.get_grasses())
    plot_sand(sim.get_sands())
    plot_water(sim.get_waters())
    plot_gates(sim.get_enchanted_gates())
    plot_obstacles(sim.get_obstacles())


step_text = None  # Global variable to store the step text object


def plot_simulation(sim: Simulation) -> FuncAnimation:
    """
    Visualizes the movements of different types of walkers in a simulation on a matplotlib plot.

    This function takes a Simulation object as an argument and uses a FuncAnimation object from the
    matplotlib.animation module to animate the movements of the walkers. Each walker type is represented by
    a different line on the plot.

    The function also plots the different terrains in the simulation by calling the plot_terrains function. The x-axis
    represents the steps, and the y-axis represents the locations of the walkers.

    The function does not return any value but displays the plot using plt.show().

    Args:
        sim (Simulation): A Simulation object representing the current state of the simulation.

    Returns:
        None

    Note:
        This function modifies the current matplotlib plot in-place.
        It is used to visualize the movements of the walkers and the different terrains in the simulation.
    """
    data = sim.get_total_dict()  # Get the data for all walkers
    walkers = list(data.keys())  # Get the list of walker types
    walker_data = {walker: ([], []) for walker in walkers}  # Initialize the walker data

    all_x_values = []  # Initialize a list to store all x values
    all_y_values = []  # Initialize a list to store all y values
    for walker in walkers:  # Iterate over the walker types
        for frame_data in data[walker].values():  # Iterate over the data for each walker type
            location = frame_data['locations']  # Get the location of the walker
            all_x_values.append(location[0])  # Append the x value to the list
            all_y_values.append(location[1])  # Append the y value to the list
    min_x, max_x = min(all_x_values), max(all_x_values)  # Get the minimum and maximum x values
    min_y, max_y = min(all_y_values), max(all_y_values)  # Get the minimum and maximum y values
    fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis
    lines = {walker: ax.plot([], [], label=walker)[0] for walker in walkers}  # Create a line for each walker type

    def init() -> list:
        """
        Initializes the plot for the simulation.

        This function sets the initial axis limits based on the overall range of x and y values. It calls the
        `plot_terrains` function to plot the different terrains in the simulation. It also creates a legend for the
        walkers and terrains.

        The function initializes a text object to display the current step number on the plot. The text object is
        positioned in the top left corner of the plot and has a white background for better visibility.

        Returns:
            list: A list containing the line objects for each walker and the text object for the step counter.

        Note:
            This function is called inside the `FuncAnimation` object in the `plot_simulation` function. It is used to
            set up the plot before the animation starts.
        """
        ax.set_xlim(min_x - 1, max_x + 1)  # Set the x-axis limits
        ax.set_ylim(min_y - 1, max_y + 1)  # Set the y-axis limits
        plot_terrains(sim)  # Plot the terrains

        global step_text  # Declare the step_text variable as global
        step_text = ax.text(0.05, 0.95, '', transform=ax.transAxes,
                            bbox=dict(facecolor='white', alpha=0.5))  # Create a text object for the step counter
        walker_legend = ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1))  # Create a legend for the walkers

        legend_elements = [Patch(facecolor='green', label='Grass'),
                           Patch(facecolor='yellow', label='Sand'),
                           Patch(facecolor='blue', label='Water'),
                           Patch(facecolor='purple', label='Gate'),
                           Patch(facecolor='red', label='Obstacle')]  # Create legend elements for terrains
        ax.legend(handles=legend_elements, loc='lower right')  # Create a legend for the terrains

        ax.add_artist(walker_legend)  # Add the walker legend to the plot

        return list(lines.values()) + [step_text]  # Return the line objects and the step text

    def update(frame: int) -> list:
        """
        Updates the plot for each frame of the animation.

        This function takes a frame number as an argument and updates the data for each walker's line on the plot
        based on the data for the current frame. It also updates the step counter text and the axis limits if necessary.

        The function returns a list containing the line objects for each walker and the text object
        for the step counter.

        Args:
            frame (int): The current frame number.

        Returns:
            list: A list containing the line objects for each walker and the text object for the step counter.

        Note:
            This function is called inside the `FuncAnimation` object in the `plot_simulation` function. It is used to
            update the plot for each frame of the animation.
        """
        for walker in walkers:  # Iterate over the walker types
            x, y = walker_data[walker]  # Get the x and y values for the walker
            step_info = data[walker].get(frame)  # Get the data for the current frame
            if step_info:  # If there is data for the current frame
                walker_location = step_info['locations']  # Get the location of the walker
                x.append(walker_location[0])  # Append the x value to the list
                y.append(walker_location[1])  # Append the y value to the list
                lines[walker].set_data(x, y)  # Set the data for the walker's line

        step_text.set_text(f'Step: {frame + 1}')  # Set the text for the step counter

        current_xlims = ax.get_xlim()  # Get the current x-axis limits
        current_ylims = ax.get_ylim()  # Get the current y-axis limits
        if min_x < current_xlims[0] or max_x > current_xlims[1]:  # If the x-axis limits need to be updated
            ax.set_xlim(min_x - 1, max_x + 1)  # Update the x-axis limits
        if min_y < current_ylims[0] or max_y > current_ylims[1]:  # If the y-axis limits need to be updated
            ax.set_ylim(min_y - 1, max_y + 1)  # Update the y-axis limits

        return list(lines.values()) + [step_text]  # Return the line objects and the step text

    ani = FuncAnimation(fig, update, frames=range(len(data[walkers[0]])),
                        init_func=init, blit=False, interval=100, repeat=False)  # Create the animation

    plt.xlabel("X")  # Label for the x-axis
    plt.ylabel("Y")  # Label for the y-axis
    plt.title("Walker Movements")  # Title for the plot
    plt.legend()  # Show the legend
    plt.grid(True)  # Show the grid
    plt.show()  # Display the plot

    return ani  # Return the animation


def plot_y_crosses(y_crosses_dict: Dict[str, Dict[str, float]]) -> None:
    """
    Visualizes the average number of times each type of walker crosses the y-axis at each step in the simulation.

    This function takes a dictionary as an argument, where each key is a walker type and each value is another
    dictionary. In the inner dictionary, each key is a step number (as a string) and each value is the average
    number of times the walker crosses the y-axis for that step.

    The function creates a line plot using matplotlib, where the x-axis represents the steps and the y-axis
    represents the average number of y-axis crossings. Each walker type is represented by a different line on the plot.

    Args:
        y_crosses_dict (Dict[str, Dict[str, float]]): A dictionary where each key is a walker type and each value
        is another dictionary. In the inner dictionary, each key is a step number (as a string) and each value is
        the average number of times the walker crosses the y-axis for that step.

    Returns:
        None

    Note:
        This function creates a new matplotlib plot each time it is called. It does not modify any existing plots
        or figures. The plot is displayed using plt.show().
    """

    # Get the steps from the first walker type. Assuming all walker types have the same steps
    steps = [int(step) for step in y_crosses_dict[list(y_crosses_dict.keys())[0]]]

    # Extract y (average y-axis crossings) for each walker type
    walkers = list(y_crosses_dict.keys())

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.title("Number of times the walkers crossed the y axis")

    # Loop through each walker type and plot its data
    for walker in walkers:  # Iterate over the walker types
        y = [y_crosses_dict[walker][str(step)] for step in steps]  # Get y values for each step
        plt.plot(steps, y, label=walker)  # Plot the data
    plt.xlabel('Steps')  # Label for the x-axis
    plt.ylabel('Number of Crossings')  # Label for the y-axis
    plt.legend()  # Show legend with walker names
    plt.show()  # Display the plot


def plot_y_distance(y_distance_dict: Dict[str, Dict[str, float]]) -> None:
    """
    Visualizes the average distance of each type of walker from the y-axis at each step in the simulation.

    This function takes a dictionary as an argument, where each key is a walker type and each value is another
    dictionary. In the inner dictionary, each key is a step number (as a string) and each value is the average
    distance of the walker from the y-axis for that step.

    The function creates a line plot using matplotlib, where the x-axis represents the steps and the y-axis
    represents the average distance from the y-axis. Each walker type is represented by a different line on the plot.

    Args:
        y_distance_dict (Dict[str, Dict[str, float]]): A dictionary where each key is a walker type and each value
        is another dictionary. In the inner dictionary, each key is a step number (as a string) and each value is
        the average distance of the walker from the y-axis for that step.

    Returns:
        None

    Note:
        This function creates a new matplotlib plot each time it is called. It does not modify any existing plots
        or figures. The plot is displayed using plt.show().
    """

    # Get the steps from the first walker type. Assuming all walker types have the same steps
    steps = [int(step) for step in
             y_distance_dict[list(y_distance_dict.keys())[0]]]

    # Extract y (average y-axis crossings) for each walker type
    walkers = list(y_distance_dict.keys())

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.title("Average distance from y axis")

    # Loop through each walker type and plot its data
    for walker in walkers:  # Iterate over the walker types
        y = [y_distance_dict[walker][str(step)] for step in steps]  # Get y values for each step
        plt.plot(steps, y, label=walker)  # Plot the data
    plt.xlabel('Steps')  # Label for the x-axis
    plt.ylabel('Distance from x axis')  # Label for the y-axis
    plt.legend()  # Show legend with walker names
    plt.show()  # Display the plot


def plot_origin_distance(origin_distance_dict: Dict[str, Dict[str, float]]) -> None:
    """
    Visualizes the average distance of each type of walker from the origin at each step in the simulation.

    This function takes a dictionary as an argument, where each key is a walker type and each value is another
    dictionary. In the inner dictionary, each key is a step number (as a string) and each value is the average
    distance of the walker from the origin for that step.

    The function creates a line plot using matplotlib, where the x-axis represents the steps and the y-axis
    represents the average distance from the origin. Each walker type is represented by a different line on the plot.

    Args:
        origin_distance_dict (Dict[str, Dict[str, float]]): A dictionary where each key is a walker type and each value
        is another dictionary. In the inner dictionary, each key is a step number (as a string) and each value is
        the average distance of the walker from the origin for that step.

    Returns:
        None

    Note:
        This function creates a new matplotlib plot each time it is called. It does not modify any existing plots
        or figures. The plot is displayed using plt.show().
    """

    # Get the steps from the first walker type. Assuming all walker types have the same steps
    steps = [int(step) for step in
             origin_distance_dict[list(origin_distance_dict.keys())[0]]]

    # Extract y (average y-axis crossings) for each walker type
    walkers = list(origin_distance_dict.keys())

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.title("Average distance from origin")

    # Loop through each walker type and plot its data
    for walker in walkers:  # Iterate over the walker types
        y = [origin_distance_dict[walker][str(step)] for step in steps]  # Get y values for each step
        plt.plot(steps, y, label=walker)  # Plot the data
    plt.xlabel('Steps')  # Label for the x-axis
    plt.ylabel('Distance from origin')  # Label for the y-axis
    plt.legend()  # Show legend with walker names
    plt.show()  # Display the plot


def plot_x_distance(x_distance_dict: Dict[str, Dict[str, float]]) -> None:
    """
    Visualizes the average distance of each type of walker from the x-axis at each step in the simulation.

    This function takes a dictionary as an argument, where each key is a walker type and each value is another
    dictionary. In the inner dictionary, each key is a step number (as a string) and each value is the average
    distance of the walker from the x-axis for that step.

    The function creates a line plot using matplotlib, where the x-axis represents the steps and the y-axis
    represents the average distance from the x-axis. Each walker type is represented by a different line on the plot.

    Args:
        x_distance_dict (Dict[str, Dict[str, float]]): A dictionary where each key is a walker type and each value
        is another dictionary. In the inner dictionary, each key is a step number (as a string) and each value is
        the average distance of the walker from the x-axis for that step.

    Returns:
        None

    Note:
        This function creates a new matplotlib plot each time it is called. It does not modify any existing plots
        or figures. The plot is displayed using plt.show().
    """
    steps = [int(step) for step in
             x_distance_dict[list(x_distance_dict.keys())[0]]]  # Assuming all walkers have the same steps

    # Extract y (average y-axis crossings) for each walker type
    walkers = list(x_distance_dict.keys())

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.title("Average distance from x axis")

    # Loop through each walker type and plot its data
    for walker in walkers:  # Iterate over the walker types
        y = [x_distance_dict[walker][str(step)] for step in steps]  # Get y values for each step
        plt.plot(steps, y, label=walker)  # Plot the data
    plt.xlabel('Steps')  # Label for the x-axis
    plt.ylabel('Distance from x axis')  # Label for the y-axis
    plt.legend()  # Show legend with walker names
    plt.show()  # Display the plot


def plot_time_to_escape(times_dict: Dict[str, Tuple[float, int]]) -> None:
    """
       Visualizes the average time taken by each type of walker to escape the simulation and the number of simulations
       in which the walker failed to escape.

       This function takes a dictionary as an argument, where each key is a walker type and each value is a tuple.
       The first element of the tuple is the average time taken by the walker to escape, and the second element is
       the number of simulations in which the walker failed to escape.

       The function creates a bar plot using matplotlib, where the x-axis represents the walker types and the y-axis
       represents the average time to escape and the number of failed simulations. Each walker type is represented by
       two bars on the plot, one for the average time to escape and one for the number of failed simulations.

       Args:
           times_dict (Dict[str, Tuple[float, int]]): A dictionary where each key is a walker type and each value is
           a tuple. The first element of the tuple is the average time taken by the walker to escape, and the second
           element is the number of simulations in which the walker failed to escape.

       Returns:
           None

       Note:
           This function creates a new matplotlib plot each time it is called. It does not modify any existing plots
           or figures. The plot is displayed using plt.show().
       """
    labels = list(times_dict.keys())  # Get the walker types
    average_times = [value[0] for value in times_dict.values()]  # Get the average times
    failed_simulations = [value[1] for value in times_dict.values()]  # Get the number of failed simulations

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis

    # Create the bar plot
    rects1 = ax.bar(x - width/2, average_times, width, label='Average Time to Escape')
    rects2 = ax.bar(x + width/2, failed_simulations, width, label='Failed to escape Simulations')

    ax.set_xlabel('Walker Types')  # Label for the x-axis
    ax.set_ylabel('Counts')  # Label for the y-axis
    ax.set_title('Time to Escape and Failed to escape Simulations by Walker Type')  # Title for the plot
    ax.set_xticks(x)  # Set the x-ticks
    ax.set_xticklabels(labels)  # Set the x-tick labels
    ax.legend()  # Show the legend
    plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    def autolabel(rects: list) -> None:
        """
        Attach a text label above each bar in a bar plot, displaying its height.

        This function takes a list of rectangles (representing the bars in the bar plot) as an argument.
        For each rectangle, it calculates the height and creates a text annotation at the top of the rectangle
        with the height value. If the height is an integer, it is displayed as an integer; otherwise,
        it is displayed as a float with two decimal places.

        Args:
            rects (List[Rectangle]): A list of Rectangle objects representing the bars in the bar plot.

        Returns:
            None

        Note:
            This function is called inside the `plot_time_to_escape` function. It is used to annotate the bars in
            the bar plot with their respective heights.
        """
        for rect in rects:  # Iterate over the rectangles
            height = rect.get_height()  # Get the height of the rectangle
            # Check if the height is an integer and format accordingly
            if height.is_integer():  # Check if the float is a whole number
                label_format = f'{int(height)}'  # Convert to integer and format
            else:
                label_format = f'{height:.2f}'  # Format as float with two decimal places
            ax.annotate(label_format,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')  # Set the text position

    # Call the function to attach the labels
    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()  # Adjust the layout
    plt.show()  # Display the plot
