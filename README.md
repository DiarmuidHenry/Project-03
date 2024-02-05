# Discovering Ireland Solver - PP3<!-- omit from toc -->

This project is a Python program where users who are playing the board game Discovering Ireland can enter their dealt cards and find out the shortest route to take in the game, thereby greatly increasing their chances of winning.

The program is visually pleasing and evokes positive emotions in the user. Instructions, colours and clear prompts make the program simple to follow.


[Deployed Program](https://discovering-ireland-solver-8aea73758694.herokuapp.com/)

## Table of Contents<!-- omit from toc -->
- [Introduction](#introduction)
  - [History](#history)
  - [Game Theory](#game-theory)
- [Aim](#aim)
  - [Program Objective](#website-objective)
  - [Key Features](#key-features)
- [Potential Users](#potential-users)
  - [User Goals](#user-goals)
  - [User Testimonials](#user-testimonials)
- [Design \& Development](#design--development)
  - [Data Model](#data-model)
  - [Game Flow](#game-flow)
  - [Colour Scheme](#colour-scheme)
  - [Banner](#banner) 
  - [Features](#features)
- [Technology \& Resources](#technology--resources)
- [Deployment](#deployment)
- [Issues/Bugs](#issuesbugs)
  - [Resolved](#resolved)
  - [Unresolved](#unresolved)
- [Testing \& Validation](#testing--validation)
  - [Functional Testing](#functional-testing)
  - [PEP8 Validation](#pep8-validation)
- [Future Improvements/Development](#future-improvementsdevelopment)

## Introduction

### History

Discovering Ireland is a board game originally released by Gosling Games in 1987, and has gone on to sell over 250,000 copies. The newer version (which this program was written with in mind) was releasd in 2018. The playing board consists of 52 towns, each connected to some of the other towns by a number of steps/blocks. Each player is dealt 2 Entry/Exit Cards: these indicate where they must start and finish their game/journey. They also receive a predesignated number of Town Cards, which they must visit in between the Entry/Exit Cards. The number of Town Cards chosen must be at least 5, and in theory can be up to $\lfloor\frac{\text{Number of Town Cards}}{\text{Number of Players}}\rfloor$. For a 2 player game, this would be $\lfloor\frac{46}{2}\rfloor = 23$. For a 3 player game, this would be $\lfloor\frac{46}{3}\rfloor = \lfloor 15.\dot{3}\rfloor = 15$ However, the most common number of Town Cards to play with is around 5-8, as anymore than this can lead to a very long game, especially with a larger number of players.

Due to the memory restrictions on the Heroku hosting platform, I have limited the number of Town Cards to 9. Any more than this causes the memory quota to be exceeded. For further information, [see below in Issues/Bugs](#issuesbugs).

The player who visits all of the towns on their Town Cards and ends at their final Entry/Exit card wins.

The player who visits all of the towns on their Town Cards and ends at their final Entry/Exit card wins.

[The game can be seen on their website](https://goslinggames.ie/product/discovering-ireland-board-game/). [The rulebook can be viewed/downloaded here](https://goslinggames.ie/wp-content/uploads/2018/10/Rules-For-Discovering-Ireland-2018.pdf).

### Game Theory

Whilst playing with my partner at home, we have often both been in the situation where it is unclear as to which route is the best/shortest to take. Since their is a relatively small number of towns, each connected to only a few other towns, it seemed apparent to me that one could create a graph that represents the game: each town being a node, and each pair of adjacent towns connected by an edge whose weight is the number of steps between said towns. From this, one could use `numpy` and `networkx` to find the shortest path. This means we can essentially reduce playing the game to a modified Travelling Salesman Problem (those unfamiliar with this problem can [read more about it here](https://en.wikipedia.org/wiki/Travelling_salesman_problem)). The modifications in this case are that we don't want to necessarily end where we started, and we only need to visit a subset of all vertices in the graph (but we may traverse all edges on the graph in our journey).

By creating a graph of the game, I can exploit properties and algorithms used in Graph Theory to systematically explore any/all routes simply through for loops in code, thereby ensuring that the resulting path is the shortest that exists. Due to the relatively small number of towns and Town Cards, this problem can be solved in seconds. For larger numbers of Town Cards, more computing power (or a lot more time) would be needed.

**Things to note:**
- All given shortest paths are symmetrical, i.e. if your given path is `[50, 52, 51, 48, 45, 40, 39]`, then this is the same length as `[39, 40, 45, 48, 51, 52, 50]``. Since this is always the case, I fixed the entry card (the starting point) and just created one order of each of these routes.
- Chance Cards, road blocks, other players' decisions (e.g. to use their Chance Card to send you to a different location on the board) are not taken into account, as these cannot be accuratley accounted for in a simple program. It would take more than 500 lines of code to correctly predict human psychology during a game.
- Making a U-turn (i.e. visiting a town and then returning from the direction you came from) often includes wasted movements, since you can overshoot the town by $n$ steps, leading to you having to backtrack $n$ wasted steps again, adding a total of $2n$ steps to the path length. Compensating for this would lead to a much more in depth analysis of each route, as well as applying probability theory to the dice throws, so I chose therefore to ignore it in this case. In a future version, [I may come back to this](#future-improvementsdevelopmentsure) 

## Aim

To create a program that, given a hand of cards a player is dealt, will create the shortest route possible, starting at one of the Entry/Exit Cards, visiting all Town Cards, then ending on an Entry/Exit card. This will thereby give the user the best chance of winning the game.

### Program Objective

- Grab the attention of the user with a pleasing initial welcome screen/message.
- Give instructions explaining the program, and briefly explaining the rules of the game.
- Get the user to input their given cards in an acceptable form, through the use of clear prompts and error validation.
- Use this data as well as the data from the board itself (see [Data Model](#data-model)) to calculate the shortest possible route.
- Print this route in a clear, visually pleasing manner for the user.

### Key Features

- A large, eye-catching welcome message/banner.
- Instructions that fit well in the limiter terminal screen.
- Explanatory prompts.
- Use of colours for clarity.
- Use of animations to show activity on an otherwise inactive screen. 

## Potential Users

- Anyone who has played - or intends to play - Discovering Ireland.
- Those interested in Graph Theory and/or the Travelling Salesman Problem.
- Those who are starting to learn Python and would like to see a functioning program that uses a relatively small input to perform large calculations.

## Design & Development

### Data Model

This part contains some mathematical terminology that might not be familiar to many. If you are interested, [click here for a brief introduction of Graph Theory](https://en.wikipedia.org/wiki/Graph_theory).

Here is a breakdown of how the program runs its calculations:

1. *Create an adjacency matrix, containing the number of steps between all pairs of adjacent towns*

The only direct data input for this was `counted_distances`, which is a Google Sheet with the distances between adjacent towns. For example, the value of the cell indexed $(41,47)$ is 13, as there **is** a direct path between 42 - Tipperary and 48 - Killarney, and the length of this path is 13. Here, we note that indexing starts at 0, but the town numbers start at 1. (I later rename the vertices in the graph to fix this discrepency). The value in cell indexed $(6,8)$ is 0, since ther **is not** a direct path between 7 - Strabane and 9 - Belfast that doesn't go through another town.

Since `counted_distances` is symmetrical (the shortest distance from town A to town B is the same as from town B to town A), I actually only counted half of the entries and then created a symmetrical spreadsheet from that. This drastically descreased the amount of manual counting needed in order to set up the model.

2. *Use this alongside `networkx` to create a graph (commonly called a network) of the game board, where each node/vertex represents a town (indexed by the town number) and each edge represents the number of steps between adjacent towns*

Thanks to [networkx](https://networkx.org/), this was very straightforward. After using `numpy` to create an array from the data imported from `counted_distances`, I then used this array to create the graph of the board. I then relabelled all vertices of the graph starting at index 1. This means the label of each vertex would match the number of the town it represents.

3. *Using this graph, create 2 objects `all_shortest_paths` and `distances`, respectively containing the shortest path between every pair of towns on the board and the distances between these two towns*

These arrays were created one entry at a time, with each new entry being appended once calculated. The `distances` array was reshaped into a square array. Since `all_shortest_paths` is a list of lists, I struggled to find a way to reshape this into a square array, so it remained as a list. I refer to this later in [Issues/Bugs: Unresolved](#unresolved).

For example, the entry in index $(5,12)$ of `distances` is the length of the path from 6 - Ballymena to 13 - Sligo, which is 16. The corresponding entry in `all_shortest_paths` is the shortest path from Ballymena to Sligo, which is `[6, 10, 12, 13]`. 

4. *User inputs their assigned cards*

Note: During construction, I randomly assignned a valid dealt hand of cards in order to sidestep this in the early stages. This was removed in later commits.

It's here that data validation is crucial, since the input must be in exactly the correct format, in the correct place.

5. *Create a list of all possible routes to visit these towns (whilst abiding by the rules of the game, i.e. starting and finishing on an Entry/Exit Card)*

Use `itertools` to create a list of all permutations of `assigned_town_cards`. This list is then stacked with the 2 Entry/Exit Cards to give `all_routes`: every legal way of completing the game with the users given cards.

6. *Calculate the length of all of these possible routes*

`route_lengths` is constructed by finding the corresponding entry in `distances` for each consecutive pair of towns in a given permutation, and adding them together to give the length of that particular path.

7. *Find the shortest route length value/s, and print the corresponding route that the player should take, including all towns they will visit along their journey*

Find the miniminum value/s in `route_lengths` and the corresponding entry in `all_routes` for this/these. These will then be printed clearly for the user, highlighting when they visit one of the towns on their cards. 


### Game Flow/Logic



### Banner

### Colour Scheme

### Features

## Technology \& Resources

## Deployment

## Issues/Bugs

### Resolved

### Unresolved

## Testing \& Validation

### Functional Testing

### PEP8 Validation

## Future Improvements/Developments

with an extra condition along the lines of `if results_lists[i] = results_lists[i+2]`.















Bugs/fixes:
- pop(0) lead to subsequent items in lists being altered and shortened. After reading up on it, this is because I wasn't just chaning next, but I was also changing what I had set it equal to. I fixed this by making next a soft copy, meaning that popping elements from it would leave the original element unchanged.
- Some of the less obvious paths between adjacent towns were missed when manually counting, e.g. (2,9), (32,39). This meant that resulting shortets paths given seemed odd when the code was run. After spotting these errors, I went back to sym and added in the missed edges.
- Whilst testing, I realised that I had used non-generic integers whilst doing loops, i.e. instead of using `len(all_cards)`, I had just used `52`, since that was the number I was working with. I made sure to change this, so that a change in the setup of the game (new cards, new board layout) wouldn't lead to problems in executing the program in the future.
- Since there are 2 of each Entry/Exit card, I have allowed for both cards to be the same, by changing `random.sample()` (without replacement) to `random.choices()` (with replacement). Since there are only 2 copies of each Town card, this will suffice, but would need to be altered if the program would allow for several people choosing cards in a single execution. Another way to fix this would be to make each element in entry_cards appear twice. 
- When including error messages, I found myself either getting stuck in loops, or jumping over some checks, depending on what/how many loops I was repeating. I solved this breaking the program down into functions, then creating a run_program() function that would neatly organise the logic/flow through the solver.

Approach:
- Create an adjacency matrix/table/array, containing the number of steps between all pairs of adjacent towns.
- Use this alongside `networkx` to create a graph of the game board, where each node represents a town (indexed by the town number) and each edge represents the number of steps between adjacent towns.
- From this, create another array containing the shortest path between every pair of towns on the board (including non-adjacent towns).
- User inputs their assigned cards. (During construction, I randomly assigened a valid dealt hand of cards in order to sidestep this in the early stages),
- Create a list of all possible routes to visit these towns (whilst abiding by the rules of the game).
- Calculate the length of all of these possible routes.
- Find the shortest one/s, and print both the order that the player should visit the cards in their hand, including all the towns they would visit inbetween, to show a more detailed route.

Comments/Criticisms:
- I used the CodeInstitute template in order to make a workspace that could run python coding.
- The output is basic, i.e. text on the console. To make it something that would be more appealing to most people, some sort of front end should be paired with it.
- This program was made to be very adaptable/generic. If the towns on the board were completely moved around; a new list of towns was created; a new sublist of Entry/Exit Cards was created; then all that would need to be changed would be the construction of the lists `all_cards`, `entry_cards` and the `counted_distances` spreadsheet. Although this would still take some time, it would only be a matter of minutes to count the distances on a new board of a similar size, and mere seconds to recontruct the lists of cards.
- The largest contributor to running time is calculating the shortest route (including intermediate towns) for each legal iteration of the dealt cards, of which there are `number_of_town_cards`$!$ (factorial). For a game with 8 Town Cards, that is $8 \times 7 \times 6 \times \dots \times 2 \times 1 = 40320$, with each of these operations containing thousands of suboperations. This could almost certainly be optimised using [Dijkstra's Algorithm](https://www.freecodecamp.org/news/dijkstras-shortest-path-algorithm-visual-introduction/) to greatly narrow the number of operations for higher numbers of town cards, but for the purposes of this project, I felt this was unnecessary.