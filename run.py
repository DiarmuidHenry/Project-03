import gspread
from google.oauth2.service_account import Credentials
import numpy as np
import networkx as nx
from timeit import default_timer as timer
import itertools
from itertools import permutations

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

# Create placeholders to work with now. Will be replaced by user input later
assigned_entry_cards = [2, 4, 6, 8, 10, 14, 23, 37]
assigned_town_cards = [5, 31]

def print_cards():
    global dealt_hand, assigned_town_cards, assigned_entry_cards
    
    print("\nAssigned Town Cards are:")
    print(assigned_town_cards)

    print("\nAssigned Entry Cards are:")
    print(assigned_entry_cards)
    
    dealt_hand = np.hstack((assigned_entry_cards, assigned_town_cards))

    # Combining the above to give the dealt hand
    print("\nDealt hand is:")
    print(dealt_hand)
    
def calculate_route():
    # Start timer
    start = timer()
    
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
    
    
    
    end = timer()

    # Time taken shown in seconds to 5sf
    time_taken = round((end - start), 5)

    print("\n\nTime taken to calculate route/s:")
    print(time_taken, "seconds\n")
    
    
    
    