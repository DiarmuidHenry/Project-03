import gspread
from google.oauth2.service_account import Credentials
import numpy as np
import networkx as nx
from timeit import default_timer as timer
import itertools
import sys
import time
import threading
from colorama import Fore, Back, Style, init
init(autoreset=True)
import os

# Define global varibale used in loading_animation
solver_ready = False


# Cycles between 1, 2 and 3 dots printed after word
def loading_dots(word):
    print()
    print()
    for dots in itertools.cycle(["       ", " .     ", " . .   ", " . . . "]):
        if solver_ready:
            break
        sys.stdout.write(f"\r{word}" + dots)
        sys.stdout.flush()
        time.sleep(0.3)


# Animation happens concurrent with rest of code loading/thinking
def play_loading_animation(word):
    loading_animation = threading.Thread(target=loading_dots, args=(word,))
    loading_animation.start()
    return loading_animation


# Loading prints on program startup
loading_animation = play_loading_animation("Loading")

# Setting up API from Google Sheet
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("discovering_ireland")

# Extracting data from counted_distances worksheet
distance_data = SHEET.worksheet("counted_distances")
counted_distances = distance_data.get_all_values()

# Convert values from counted_distances to a NumPy array with integer values
edge_weights_matrix = np.array(counted_distances, dtype=np.int32)

# Extracting town names from town_names, convert to list of strings
town_data = SHEET.worksheet("town_names")
town_names = town_data.get_all_values()
town_names = [town[0] for town in town_names]

# Getting value of MAX_NUMBER_OF_TOWNS from environment variables
MAX_NUMBER_OF_TOWNS = os.environ.get("MAX_NUMBER_OF_TOWNS")

# Check if MAX_NUMBER_OF_TOWNS exists
if MAX_NUMBER_OF_TOWNS is not None:
    # If MAX_NUMBER_OF_TOWNS exists, set to integer value
    MAX_NUMBER_OF_TOWNS = int(MAX_NUMBER_OF_TOWNS)
    town_limit = True
else:
    # If MAX_NUMBER_OF_TOWNS is not set, set town_limit to False
    town_limit = False


# Getting number of Town Cards from length of town_names
number_of_towns = len(town_names)

# Construct list of all cards, labelled by their corresponding numbers
all_cards = list(range(1, number_of_towns + 1))

# List of all Entry/Exit Cards. Must be manually enterred
entry_cards = [
    5, 9, 31, 39, 47, 50
]
# List of all Town Cards, which is all_cards with entry_cards removed
town_cards = [i for i in all_cards if i not in entry_cards]

# Declare assigned card variables in global scope
assigned_town_cards = []
assigned_entry_cards = []
dealt_hand = []

# Welcome message greeting user at start of program
welcome_message = """
                   Welcome to the Discovering Ireland Solver!
         Would you like to read the instructions? Please type YES or NO:
"""

# Written instructions to be printed if necessary
instructions = """

Discovering Ireland is a board game that consists of a playing board with
52 towns spread over Ireland, each given a number from 1 to 52.

Each player is given 2 Entry/Exit Cards; where they start & finish their route.
They also receive at least 5 Town Cards. These may be visited in ANY order, but
each player MUST visit EVERY town for which they have a Town Card.

The winner is the first person to visit all of their Town Cards and
to arrive at their final Entry/Exit Card.

This solver finds the shortest possible route to visit all your dealt cards.
This gives you the best chance of finishing before your opponent/s!

In order to use the solver, simply follow the prompts that appear on screen.
The optimal route/s will be calculated and printed clearly for you.

Entry/Exit Cards: 5, 9, 31, 39, 47, 50
Town Cards: All other numbers from 1 to 52

Enjoy, and good luck!
"""

# Nodes: town_cards, entry_cards. Edge weights: counted_distances.csv
graph = nx.from_numpy_array(edge_weights_matrix)

# Reindexing so that town number matches index
graph = nx.convert_node_labels_to_integers(graph, 1)

# Lists all pairs of nodes; length of path between them; route taken.
distances = []
all_shortest_paths = []
for i in graph.nodes:
    for j in graph.nodes:
        all_shortest_paths.append(nx.shortest_path(
            graph, source=i, target=j, weight="weight"))
        distances.append(nx.shortest_path_length(graph, i, j, weight="weight"))

# Reshape distances into a square array.
distances = np.reshape(distances, newshape=(len(all_cards), len(all_cards)))

# List acceptable inputs when YES or NO should be provided.
yes_inputs = ["yes", "ye", "y"]
no_inputs = ["no", "n"]

# Possible error messages. Written here due to exceeding line length
min_entry = min(entry_cards)
max_entry = max(entry_cards)
min_town = min(town_cards)
max_town = max(town_cards)
enter_entry = """
Please enter your Entry/Exit Cards, separated by a space:
"""
enter_town = """
Please enter your Town Cards, separated by a space:
"""
invalid_spaces_intergers = """
Invalid input. Input must only contain spaces and integers."""
invalid_entry_between = (
                         f"\nInvalid input. Input musts be between"
                         f" {min_entry} and {max_entry} (inclusive)."
                         )
invalid_town_between = (
                         f"\nInvalid input. Inputs must be between"
                         f" {min_town} and {max_town} (inclusive)."
                         )
invalid_entry_not_town = """
Invalid input. Please enter only your Entry/Exit Cards.
Do not include any Town Cards."""
invalid_town_not_entry = """
Invalid input. Please enter only your Town Cards.
Do not include any Entry/Exit Cards."""
invalid_exactly_two = """
Invalid input. Players must have exactly 2 Entry/Exit Cards."""
invalid_at_least_one = """
Invalid input. Players must have at least 1 Town Card."""
invalid_duplicates = """
Invalid input. Duplicates found."""


def validate_inputs():

    global assigned_town_cards, assigned_entry_cards

    # Get input from the user as a space-separated string
    input_entry = input(Fore.YELLOW + Style.BRIGHT + enter_entry)

    while True:
        # CHECK INPUT MAKES SENSE
        try:
            input_entry = input_entry.split()
            if all(value.isdigit() for value in input_entry):
                assigned_entry_cards = [int(card) for card in input_entry]
                card_is_entry = all(
                    c in entry_cards for c in assigned_entry_cards)
                valid_entry = all(
                    c in all_cards for c in assigned_entry_cards)
            else:
                print(Fore.RED + Style.BRIGHT + invalid_spaces_intergers)
                raise ValueError(
                    "Invalid input format")

            if not valid_entry:
                print(Fore.RED + Style.BRIGHT + invalid_entry_between)
                raise ValueError(
                    "Entry/Exit Cards out of range")

            if (not (card_is_entry)) and valid_entry:
                print(Fore.RED + Style.BRIGHT + invalid_entry_not_town)
                raise ValueError(
                    "Town Cards entered instead of Entry/Exit Cards")

            if len(assigned_entry_cards) != 2:
                print(Fore.RED + Style.BRIGHT + invalid_exactly_two)
                raise ValueError(
                    "Incorrect number of Entry/Exit Cards")
            break

        except ValueError:
            input_entry = input(Fore.YELLOW + Style.BRIGHT + enter_entry)
            continue  # Back to beginning of loop

    # Get input from the user as a space-separated string
    input_town = input(Fore.GREEN + Style.BRIGHT + enter_town)

    while True:
        # CHECK INPUT MAKES SENSE
        try:
            input_town = input_town.split()
            if all(value.isdigit() for value in input_town):
                assigned_town_cards = [int(card) for card in input_town]
                card_is_town = all(
                    c in town_cards for c in assigned_town_cards)
                valid_town = all(
                    c in all_cards for c in assigned_town_cards)
            else:
                print(Fore.RED + Style.BRIGHT + invalid_spaces_intergers)
                raise ValueError("Invalid input format")

            if not valid_town:
                print(Fore.RED + Style.BRIGHT + invalid_town_between)
                raise ValueError("Town Cards out of range")

            if (not (card_is_town)) and valid_town:
                print(Fore.RED + Style.BRIGHT + invalid_town_not_entry)
                raise ValueError(
                    "Entry/Exit Cards entered instead of Town Cards")

            if len(input_town) != len(set(input_town)):
                print(Fore.RED + Style.BRIGHT + invalid_duplicates)
                raise ValueError("Duplicate cards found")

            if len(assigned_town_cards) == 0:
                print(Fore.RED + Style.BRIGHT + invalid_at_least_one)
                raise ValueError("Incorrect number of Town Cards")
            break

        except ValueError:
            input_town = input(Fore.GREEN + Style.BRIGHT + enter_town)
            continue  # Back to beginning of loop


def print_cards():
    global dealt_hand, assigned_town_cards, assigned_entry_cards

    dealt_hand = np.hstack((assigned_entry_cards, assigned_town_cards))

    print(Style.RESET_ALL)
    print("Assigned Entry/Exit Cards are:")
    print(Fore.YELLOW + Style.BRIGHT + str(assigned_entry_cards))
    
    print("\nAssigned Town Cards are:")
    print(Fore.GREEN + Style.BRIGHT + str(assigned_town_cards))


def check_cards():
    while True:
        input_check = input(
            "\nIs the above information correct? Please type YES or NO:\n")
        if input_check.lower() in yes_inputs:
            return True
        elif input_check.lower() in no_inputs:
            return False
        else:
            continue


def too_many_cards():
    too_many_cards_warning = (
                              f"\nYou have entered {len(assigned_town_cards)}"
                              f" Town Cards.\nThis may result in a long"
                              f" processing time and/or\nprogram"
                              f" termination/malfunction due to memory"
                              f" issues.\nDo you wish to continue anyway?"
                              f" Please type YES or NO:\n"
                              )
    env_limit_warning = (
                         f"\nYou have entered {len(assigned_town_cards)}"
                         f" Town Cards.\nThis exceeds the limit"
                         f" of Town Cards for this environment"
                         f" ({MAX_NUMBER_OF_TOWNS}).\nTo enter"
                         f" a new selection of cards, enter 1.\nTo"
                         f" restart the program, enter 2:\n"
                         )
    
    if (not town_limit):
        if len(assigned_town_cards) <= 9:
            return "continue"   
        else:
            while True:
                too_many_cards_check = input(
                    Fore.RED + Style.BRIGHT + too_many_cards_warning)
                if too_many_cards_check.lower() in yes_inputs:
                    return "continue"
                elif too_many_cards_check.lower() in no_inputs:
                    return "restart program"
                else:
                    continue
    
    if town_limit:
        if len(assigned_town_cards) <= MAX_NUMBER_OF_TOWNS:
            return "continue"
        else:
            while True:
                env_limit_choice = input(
                    Fore.RED + Style.BRIGHT + env_limit_warning)
                if env_limit_choice == "1":
                    return "new cards"
                if env_limit_choice == "2":
                    return "restart program"
                else:
                    continue
    

def calculate_route():
    global solver_ready
    # Start timer
    start = timer()

    solver_ready = False
    loading_animation = play_loading_animation("Calculating route/s")

    # List all permutations of assigned_town_cards
    possible_town_routes = list(itertools.permutations(assigned_town_cards))

    # Create start and end card arrays,
    start_entry = np.full((len(possible_town_routes), 1),
                          assigned_entry_cards[0])
    end_entry = np.full((len(possible_town_routes), 1),
                        assigned_entry_cards[1])

    # Stacking the previous to get all possible valid routes.
    all_routes = np.hstack(
        (start_entry, possible_town_routes, end_entry))

    # Calculate total route length for each route.
    route_lengths = []
    for i in range(all_routes.shape[0]):
        for j in range(all_routes.shape[1]-1):
            route_lengths.append(
                distances[all_routes[i, j]-1, all_routes[i, (j+1)]-1])

    # Reshaping route lengths into an array, one row for each route.
    route_lengths = np.reshape(route_lengths, newshape=(
        (all_routes.shape[0]), all_routes.shape[1]-1))

    # Summing each row to get route length for each route
    route_lengths = np.sum(route_lengths, axis=1)

    # Finding the minimum route length, and its corresponding index
    min_length = np.min(route_lengths)
    min_indices = [i for i, x in enumerate(route_lengths) if x == min_length]

    # Find shortest route/s in all_routes using min_indicies.
    routes_to_take = []
    for i in range(len(min_indices)):
        routes_to_take.append(all_routes[min_indices[i]])

    routes_to_take = np.asarray(routes_to_take)

    # Stop loading_animation
    solver_ready = True

    # Printing the route length for the/se route/s.
    print("\n\n\nOptimal route length:")
    print(route_lengths[min_indices[0]])

    # Compile all towns visited from all_shortest_paths and routes_to_take.
    results_list = [[assigned_entry_cards[0]] for _ in range(len(min_indices))]
    for i in range(len(min_indices)):
        for j in range(len(routes_to_take[i])-1):
            # .copy() so no changes are made to all_shortest_paths.
            next_result = all_shortest_paths[(
                (routes_to_take[i][j] - 1) * len(all_cards)) + (
                    routes_to_take[i][j+1] - 1)].copy()
            # pop to remove starting town to avoid duplication in list
            next_result.pop(0)
            results_list[i] += next_result

    # Remove instances where card order is different but route is same.
    for i in range(len(results_list)-1, 0, -1):
        for j in range(len(results_list)-2, -1, -1):
            if (i > j and results_list[i] == results_list[j]):
                del results_list[i]
                break

    print("\nOptimal route/s for dealt cards: ")

    for i in range(len(results_list)):
        a_copy = assigned_town_cards.copy()
        print("\n\n    " +
              Back.WHITE + Fore.BLACK + " Route " +
              Back.WHITE + Fore.BLACK + str(i + 1) +
              Back.WHITE + Fore.BLACK + " ", "\n")
        for j in range(len(results_list[i])):
            town = results_list[i][j]
            if j == 0 or j == (len(results_list[i]) - 1):
                print(Fore.YELLOW + Style.BRIGHT +
                      "    {:>2} : {}".format(town, town_names[town - 1]))
                a_copy = [
                    card for card in a_copy if card != town]
            elif (town in a_copy):
                print(Fore.GREEN + Style.BRIGHT +
                      "    {:>2} : {}".format(town, town_names[town - 1]))
                a_copy = [
                    card for card in a_copy if card != town]
            else:
                print("    {:>2} : {}".format(
                    results_list[i][j], town_names[results_list[i][j]-1]))

    end = timer()

    # Time taken shown in seconds to 5sf
    time_taken = round((end - start), 5)

    print("\nTime taken to calculate route/s:")
    print(time_taken, "seconds\n")
    print(Back.WHITE + Fore.BLACK + "Scroll up to see your optimal route/s!")

    while True:
        restart_choice = input(
                               f"\nDo you want to run the program with"
                               f" another selection of cards?"
                               f"\nPlease type YES or NO:\n"
                               )
        if restart_choice.lower() in yes_inputs:
            run_program()
            break
        elif restart_choice.lower() in no_inputs:
            print_goodbye()
            break
        else:
            print(Fore.RED + Style.BRIGHT +
                  "Invalid input. Please type YES or NO:\n")


def print_banner():
    print(Style.RESET_ALL)
    banner = open('banner-text.txt', 'r')
    banner_image = banner.read()
    print(banner_image)
    banner.close()
    
def print_goodbye():
    print(Style.RESET_ALL)
    goodbye = open('goodbye-text.txt', 'r')
    goodbye_image = goodbye.read()
    print(goodbye_image)
    goodbye.close()


def instructions_prompt():
    global instructions, welcome_message, solver_ready

    # Stop loading_animation
    solver_ready = True

    instructions_check = input(welcome_message)
    while True:
        try:
            if instructions_check.lower() in yes_inputs:
                print(instructions)
                break
            elif instructions_check.lower() in no_inputs:
                break
            else:
                print(Fore.RED + Style.BRIGHT + "\nInvalid input.")
                raise ValueError("Invalid input")
        except Exception:
            print
            instructions_check = input(
                "\nPlease type YES or NO: \n")
            continue  # Back to beginning of loop


def setup():
    print_banner()
    instructions_prompt()


def solver():
    validate_inputs()
    print_cards()
    if check_cards():
        too_many_cards_return = too_many_cards()
        if too_many_cards_return == "continue":
            calculate_route()
        elif too_many_cards_return == "restart program":
            run_program()
        elif too_many_cards_return == "new cards":
            solver()
    else:
        solver()


def run_program():
    setup()
    solver()


run_program()
