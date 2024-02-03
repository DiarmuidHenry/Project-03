import gspread
from google.oauth2.service_account import Credentials
import numpy as np
import networkx as nx
from timeit import default_timer as timer
import itertools
from itertools import permutations
import random
import sys
import time
import threading

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
data = SHEET.worksheet("counted_distances")

counted_distances = data.get_all_values()

# Convert values from counted_distances to a NumPy array with integer values
edge_weights_matrix = np.array(counted_distances, dtype=np.int32)

# List of town names, in oder
town_names = [
    "Ballycastle",
    "Coleraine",
    "Derry",
    "Letterkenny",
    "Larne",
    "Ballymena",
    "Strabane",
    "Donegal",
    "Belfast",
    "Omagh",
    "Armagh",
    "Enniskillen",
    "Sligo",
    "Belmullet",
    "Monaghan",
    "Ballina",
    "Newry",
    "Cavan",
    "Dundalk",
    "Carrick on Shannon",
    "Westport",
    "Knock",
    "Longford",
    "Drogheda",
    "Roscommon",
    "Trim",
    "Mullingar",
    "Clifden",
    "Athlone",
    "Ballinasloe",
    "Dublin",
    "Tullamore",
    "Galway",
    "Naas",
    "Portlaoise",
    "Roscrea",
    "Tullow",
    "Arklow",
    "Shannon",
    "Limerick",
    "Kilkenny",
    "Tipperary",
    "Clonmel",
    "Wexford",
    "Tralee",
    "Waterford",
    "Rosslare Harbour",
    "Killarney",
    "Youghal",
    "Cork",
    "Bantry",
    "Clonakilty"
]

# Getting number of town cards from size of edge_weight_matrix
number_of_towns = edge_weights_matrix.shape[0]

# Construct list of all cards, labelled by their corresponding numbers
all_cards = list(range(1, number_of_towns + 1))

# List of all entry/exit cards. Must be manually enterred
entry_cards = [
    5, 9, 31, 39, 47, 50
]
# List of all town cards, which is all_cards with entry_cards removed
town_cards = [i for i in all_cards if i not in entry_cards]

# Declare assigned card variables in global scope
assigned_town_cards = []
assigned_entry_cards = []
dealt_hand = []

# Welcome message greeting user at start of program
welcome_message = """
Welcome to the Discovering Ireland solver!
Would you like to read the instructions? Please type YES or NO:
"""

# Written instructions to be printed if necessary
instructions = """

Discovering Ireland is a board game that consists of a playing board with
52 towns spread over Ireland, each given a number from 1 to 52.

Each player is given 2 Entry/Exit cards; where they start & finish their route.
They also receive at least 5 Town Cards. These may be visited in ANY order, but
each player MUST visit EVERY town for which they have a Town card.

The winner is the first person to visit all of their Town cards and
to arrive at their final Entry/Exit card.

This solver finds the shortest possible route to visit all your dealt cards.
This gives you the best chance of finishing before your opponent/s!

In order to use the solver, simply follow the prompts that appear on screen.
The optimal route/s will be calculated and printed clearly for you.

Entry/Exit cards: 5, 9, 31, 39, 47, 50
Town cards: All other numbers from 1 to 52

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

please_enter_entry = """
Please enter your Entry/Exit Cards, separated by a space:
"""
please_enter_town = """
Please enter your Town Cards, separated by a space:
"""
invalid_spaces_intergers = """
Invalid input. Input must only contain spaces and integers."""
invalid_entry_between = f"""
Invalid input. Must be between {min_entry} and {max_entry} (inclusive)."""
invalid_town_between = f"""
Invalid input. Must be between {min_town} and {max_town} (inclusive)."""
invalid_entry_not_town = """
Invalid input. Please enter only your Entry/Exit cards.
Do not include any Town cards."""
invalid_town_not_entry = """
Invalid input. Please enter only your Town cards.
Do not include any Entry/Exit cards."""
invalid_exactly_two = """
Invalid input. Players must have exactly 2 Entry/Exit cards."""
invalid_at_least_one = """
Invalid input. Players must have at least 1 Town card."""
invalid_duplicates = """
Invalid input, duplicates found."""


def validate_inputs():

    global assigned_town_cards, assigned_entry_cards

    # Get input from the user as a space-separated string
    input_entry = input(please_enter_entry)

    while True:
        # CHECK INPUT MAKES SENSE
        try:
            input_entry = input_entry.split()
            if all(value.isdigit() for value in input_entry):
                assigned_entry_cards = [int(card) for card in input_entry]
                card_is_entry = all(
                    c in entry_cards for c in assigned_entry_cards)
                card_is_town = all(
                    c in entry_cards for c in assigned_entry_cards)
                valid_entry = all(
                    c in all_cards for c in assigned_entry_cards)
                valid_town = all(
                    c in all_cards for c in assigned_town_cards)
            else:
                print(invalid_spaces_intergers)
                raise ValueError(
                    "Invalid input format")

            if not valid_entry:
                print(invalid_entry_between)
                raise ValueError(
                    "Entry/Exit cards out of range")

            if (not (card_is_entry)) and valid_entry:
                print(invalid_entry_not_town)
                raise ValueError(
                    "Town cards entered instead of Entry/Exit cards")

            if len(assigned_entry_cards) != 2:
                print(invalid_exactly_two)
                raise ValueError(
                    "Incorrect number of Entry/Exit cards")
            break

        except ValueError:
            input_entry = input(please_enter_entry)
            continue  # Back to beginning of loop

    # Get input from the user as a space-separated string
    input_town = input(please_enter_town)

    while True:
        # CHECK INPUT MAKES SENSE
        try:
            input_town = input_town.split()
            if all(value.isdigit() for value in input_town):
                assigned_town_cards = [int(card) for card in input_town]
            else:
                print(invalid_spaces_intergers)
                raise ValueError("Invalid input format")

            if not valid_town:
                print(invalid_town_between)
                raise ValueError("Town cards out of range")

            if (not (card_is_town)) and valid_town:
                print(invalid_town_not_entry)
                raise ValueError(
                    "Entry/Exit cards entered instead of Town cards")

            if len(assigned_town_cards) not in range(1, 47):
                print(invalid_at_least_one)
                raise ValueError("Incorrect number of Entry/Exit cards")

            if len(input_town) != len(set(input_town)):
                print(invalid_duplicates)
                raise ValueError("Duplicate cards found")
            break

        except ValueError:
            input_town = input(please_enter_town)
            continue  # Back to beginning of loop


def print_cards():
    global dealt_hand, assigned_town_cards, assigned_entry_cards

    dealt_hand = np.hstack((assigned_entry_cards, assigned_town_cards))

    print("\nAssigned Town Cards are:")
    print(assigned_town_cards)

    print("\nAssigned Entry Cards are:")
    print(assigned_entry_cards)

    # Combining the above to give the dealt hand
    print("\nDealt hand is:")
    print(dealt_hand)


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


too_many_cards_warning = f"""
You have entered {len(assigned_town_cards)} town cards.
This may result in program termination/malfunction due to memory issues.
Do you wish to continue anyway? Please type YES or NO:"
"""


def too_many_cards():
    if len(assigned_town_cards) < 9:
        return True
    if len(assigned_town_cards) == 9:
        print("\n\nEstimated running time: 4 seconds")
        return True
    if len(assigned_town_cards) > 9:
        while True:
            too_many_cards_check = input(too_many_cards_warning)
            if too_many_cards_check.lower() in yes_inputs:
                return True
            elif too_many_cards_check.lower() in no_inputs:
                return False
            else:
                continue


"""
Alternative: alter too_many_cards to only allow
a maximum of 9 cards. Hosted app crashes with
10+ town cards due to lack of memory.
"""


def calculate_route():
    global solver_ready
    # Start timer
    start = timer()

    solver_ready = False
    loading_animation = play_loading_animation("Calculating route/s")

    # List all permutations of assigned_town_cards
    possible_town_routes = list(permutations(assigned_town_cards))

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
    for i in range(0, (len(min_indices))):
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
            # Variables declared only to shorten line length
            a = routes_to_take[i][j] - 1
            b = len(all_cards)
            c = routes_to_take[i][j+1]
            # .copy() so no changes are made to all_shortest_paths.
            next = all_shortest_paths[(a * b) + c - 1].copy()
            next.pop(0)
            results_list[i] += next

    # Remove instances where card order is different but route is same.
    for i in range(len(results_list)-1, 0, -1):
        for j in range(len(results_list)-2, -1, -1):
            if (i > j and results_list[i] == results_list[j]):
                del results_list[i]
                break

    print("\nOptimal route/s for dealt cards: ")

    for i in range(len(results_list)):
        assigned_town_cards_copy = assigned_town_cards.copy()
        print("\n\n     Route", i + 1, "\n")
        for j in range(len(results_list[i])):
            if j == 0 or j == (len(results_list[i]) - 1) or (results_list[i][j] in assigned_town_cards_copy):
                print(
                    "****  {:>2} : {}".format(results_list[i][j], town_names[results_list[i][j]-1]))
                assigned_town_cards_copy = [
                    card for card in assigned_town_cards_copy if card != results_list[i][j]]
            else:
                print("      {:>2} : {}".format(
                    results_list[i][j], town_names[results_list[i][j]-1]))

    end = timer()

    # Time taken shown in seconds to 5sf
    time_taken = round((end - start), 5)

    print("\nTime taken to calculate route/s:")
    print(time_taken, "seconds")
    print("\nScroll up to see your optimal route/s")
    print("\nEnjoy your game!\n")


def print_banner():
    banner = open('banner-text.txt', 'r')
    banner_image = banner.read()
    print(banner_image)
    banner.close()


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
                print("\nInvalid input.")
                raise ValueError("Invalid input")
        except Exception:
            instructions_check = input(
                "\n\nPlease type YES or NO: ")
            continue  # Back to beginning of loop


def setup():
    print_banner()
    instructions_prompt()


def solver():
    validate_inputs()
    print_cards()
    if check_cards():
        if too_many_cards():
            calculate_route()
        else:
            solver()
    else:
        solver()


def run_program():
    setup()
    solver()


run_program()
