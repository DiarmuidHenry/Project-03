import gspread
from google.oauth2.service_account import Credentials
import numpy as np
import networkx as nx
from timeit import default_timer as timer
import itertools
from itertools import permutations
import random

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

# Convert the values from counted_distances to a NumPy array with integer values
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

 # Setting range of number of town cards
min_town_cards = 5
max_town_cards = 9

# Randomly choosing number of town cards from given range
number_of_town_cards = random.randint(min_town_cards, max_town_cards);

# Assigning town cards
# assigned_town_cards = random.sample(town_cards, number_of_town_cards);
# Fix town cards when testing
# assigned_town_cards = [23, 51, 35, 7, 49, 18, 34, 40, 2, 24]

# Assigning entry/exit cards, allowing for both to be the same
# assigned_entry_cards = random.choices(entry_cards, k=2);
# Fix entry cards when testing
# assigned_entry_cards = [31, 39]

# List acceptable inputs when YES or NO should be provided.
yes_inputs = ["yes", "ye", "y"]
no_inputs = ["no", "n"]

def validate_inputs():

    global assigned_town_cards, assigned_entry_cards
    # Get input from the user as a space-separated string
    input_entry = input(
        "\n\nPlease enter your assigned Entry/Exit Cards, separated by a space: ")

    while True:
        # CHECK INPUT MAKES SENSE
        try:
            input_entry = input_entry.split()
            if all(value.isdigit() for value in input_entry):
                assigned_entry_cards = [int(card) for card in input_entry]
            else:
                print("\nInvalid input. Input must only contain spaces and integers.")
                raise ValueError("Invalid input format")

            if not all(card in all_cards for card in assigned_entry_cards):
                print(
                    "\nInvalid input. Entry/Exit cards must be between {} and {} (inclusive).".format(min(entry_cards), max(entry_cards)))
                raise ValueError("Entry/Exit cards out of range")

            if (not all(card in entry_cards for card in assigned_entry_cards)) and all(card in all_cards for card in assigned_entry_cards):
                print(
                    "\nInvalid input. Please enter only your Entry/Exit cards. Do not include any Town cards.")
                raise ValueError(
                    "Town cards entered instead of Entry/Exit cards")

            if len(assigned_entry_cards) != 2:
                print("\nInvalid input. Players must have exactly 2 Entry/Exit cards.")
                raise ValueError("Incorrect number of Entry/Exit cards")
            break

        except ValueError:
            input_entry = input(
                "\n\nPlease enter your assigned Entry/Exit Cards, separated by a space: ")
            continue  # Back to beginning of loop

    # Get input from the user as a space-separated string
    input_town = input(
        "\nPlease enter your assigned Town Cards, separated by a space: ")

    while True:
        # CHECK INPUT MAKES SENSE
        try:
            input_town = input_town.split()
            if all(value.isdigit() for value in input_town):
                assigned_town_cards = [int(card) for card in input_town]
            else:
                print("\nInvalid input. Input must only contain spaces and integers.")
                raise ValueError("Invalid input format")

            if not all(card in all_cards for card in assigned_town_cards):
                print(
                    "\nInvalid input. Town cards must be between {} and {} (inclusive).".format(min(town_cards), max(town_cards)))
                raise ValueError("Town cards out of range")

            if (not all(card in town_cards for card in assigned_town_cards)) and all(card in all_cards for card in assigned_town_cards):
                print(
                    "\nInvalid input. Please enter only your Town cards. Do not include any Entry/Exit cards.")
                raise ValueError(
                    "Entry/Exit cards entered instead of Town cards")

            if len(assigned_town_cards) not in range(1, 47):
                print("\nInvalid input. Players must have at least 1 Town card.")
                raise ValueError("Incorrect number of Entry/Exit cards")

            if len(input_town) != len(set(input_town)):
                print("\nInvalid input, duplicates found.")
                raise ValueError("Duplicate cards found")
            break

        except ValueError:
            input_town = input(
                "\n\nPlease enter your assigned Town Cards, separated by a space: ")
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
            "\nIs the above information correct?\nPlease type YES or NO:")
        if input_check.lower() in yes_inputs:
            return True
        elif input_check.lower() in no_inputs:
            return False
        else:
            continue


def too_many_cards():
    if len(assigned_town_cards) < 9:
        return True
    if len(assigned_town_cards) == 9:
        print("\n\nEstimated running time: 4 seconds")
        return True
    if len(assigned_town_cards) == 10:
        print("\n\nEstimated running time: 45 seconds")
        return True
    if len(assigned_town_cards) == 11:
        print("\n\nEstimated running time: 6 minutes")
        return True
    if len(assigned_town_cards) > 11:
        while True:
            too_many_cards_check = input(
                "\nYou have entered {} town cards. This may lead to a run time of several hours and/or the program terminating due to lack of memory.\nDo you wish to continue?\nPlease type YES or NO: ".format(len(assigned_town_cards)))
            if too_many_cards_check.lower() in yes_inputs:
                return True
            elif too_many_cards_check.lower() in no_inputs:
                return False
            else:
                continue


def calculate_route():
    # Start timer
    start = timer()

    print("\n\nCalculating route...")

    # List all permutations of assigned_town_cards
    possible_town_routes = list(permutations(assigned_town_cards))

    # Create start and end card arrays,
    start_entry = np.full((len(possible_town_routes), 1),
                          assigned_entry_cards[0])
    end_entry = np.full((len(possible_town_routes), 1),
                        assigned_entry_cards[1])

    # Stacking the previous to get all possible valid routes.
    all_possible_routes = np.hstack(
        (start_entry, possible_town_routes, end_entry))

    # Calculate total route length for each route.
    route_lengths = []
    for i in range(all_possible_routes.shape[0]):
        for j in range(all_possible_routes.shape[1]-1):
            route_lengths.append(
                distances[all_possible_routes[i, j]-1, all_possible_routes[i,(j+1)]-1])

    # Reshaping route lengths into an array, one row for each route.
    route_lengths = np.reshape(route_lengths, newshape=(
        (all_possible_routes.shape[0]), all_possible_routes.shape[1]-1))

    # Summing each row to get route length for each route
    route_lengths = np.sum(route_lengths, axis=1)

    # Finding the minimum route length, and its corresponding index
    min_length = np.min(route_lengths)
    min_indices = [i for i, x in enumerate(route_lengths) if x == min_length]

    # Find shortest route/s in all_possible_routes using min_indicies.
    routes_to_take = []
    for i in range(0, (len(min_indices))):
        routes_to_take.append(all_possible_routes[min_indices[i]])

    routes_to_take = np.asarray(routes_to_take)

    # Printing the route length for the/se route/s.
    print("\n\nOptimal route length:")
    print(route_lengths[min_indices[0]])

    # Compile all towns visited from all_shortest_paths and routes_to_take.
    lists = [[assigned_entry_cards[0]] for _ in range(len(min_indices))]
    for i in range(len(min_indices)):
        for j in range(len(routes_to_take[i])-1):
            # .copy() is used here so that no changes are made to all_shortest_paths.
            next = all_shortest_paths[(
                routes_to_take[i][j] - 1)*len(all_cards) + routes_to_take[i][j+1] - 1].copy()
            next.pop(0)
            lists[i] += next

    # Remove instances where card order is different but route is same.
    for i in range(len(lists)-1, -0, -1):
        for j in range(len(lists)-2, -1, -1):
            if (i > j and lists[i] == lists[j]):
                del lists[i]
                break

    print("\nOptimal route/s for dealt cards:")
    for i in range(len(lists)):
        print("\n\n\nRoute ", i + 1, "\n")
        # print(routes_to_take[i], ":", lists[i], "\n")
        for j in range(len(lists[i])):
            assigned_town_cards_copy = assigned_town_cards.copy()
            if j == 0 or j == (len(lists[i]) - 1) or (lists[i][j] in assigned_town_cards_copy):
                print("**** ", lists[i][j], ":", town_names[lists[i][j]-1],)
                assigned_town_cards_copy = [card for card in assigned_town_cards_copy if card != lists[i][j]]
            else:
                print("     ",lists[i][j], ":", town_names[lists[i][j]-1])
                

    end = timer()

    # Time taken shown in seconds to 5sf
    time_taken = round((end - start), 5)

    print("\n\nTime taken to calculate route/s:")
    print(time_taken, "seconds\n")
    
def run_program():
    validate_inputs()
    print_cards()
    if check_cards():
        if too_many_cards():
            calculate_route()
        else:
            run_program()
    else:
        run_program()
    
run_program()