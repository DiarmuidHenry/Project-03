Discovering Ireland is a board game originally released by Gosling Games in 1987. The newer version (which this program was written with in mind) was releasd in 2018, and consists of 52 towns, each connected to some of the other towns by a number of steps/blocks. The players are dealt 2 Entry/Exit cards where they must start and finish, and a designated number of Town cards, which they must visit in between the Entry/Exit cards. The player who visits all of their towns and ends at their final Entry/Exit card wins.

Whilst playing with my partner at home, we have often both been in the situation where (especially when playing with fewer town cards) it is unclear as to which route is the best/shortest to take. Since their is a relatively small number of towns, each connected to only a few other towns, it seemed apparent to me that oen could create a graph that represents the game: ecah town being a node, and each pair of adjacent towns connected by an edge whose weight is the number of steps between said towns. From this, one could use numpy and networkx to find the shortets path.

The aim was to create a program that, given a hand of cards a player is dealt, will create the shortest route possible, starting at one of the entry/exit cards, visiting all town cards, then ending on an entry/exit card.

Things to note:
- All given shortest paths are symmetrical, i.e. if your given path is [50, 52, 51, 48, 45, 40, 39], then this is the same length as [39, 40, 45, 48, 51, 52, 50]. Since this is always the case, I fixed the entry card (the starting point) and just created one order of each of these routes.
- Chance cards, road blocks, other players' decisions (e.g. to send you to Ballinasloe to see the horse fair) are not taken into account, as these cannot be accuratley accounted for in a simple program. It would take more than 200 lines of code to correctly predict human psychology during a game.
- Making a U-turn (i.e. visiting a town and then returning from the direction you came from) often includes wasted movements, since you can overshoot the town by n steps, leading to you having to backtrack n steps again, adding a total of 2n steps to the path length. Compensating for this would lead to a much more in depth analysis of each route, as well as applying probability theory to the dice throws, so I chose therefore to ignore it in this case. In a future version, I may come back to this, with an extra condition along the lines of `if lists[i] = lists[i+2]`.
- The only direct data input for this was `counted_distances`, which is a Google Sheet with the distances between adjacent towns. Since `counted_distances` is symmetrical (the shortest distance from town A to town B is the same as from town B to town A), I actually only counted half of the entries and the created a symmetrical spreadsheet from that. This drastically descreased the amount of manual counting needed to set up the corresponding graph. From these values, I created the `distances` array which is the distance between every pair of towns on the board. I manually counted 116 path lengths, which is much less than the $\binom(52)(51) = 1326$ possible pairs of towns.


Bugs/fixes:
- pop(0) lead to subsequent items in lists being altered and shortened. After reading up on it, this is because I wasn't just chaning next, but I was also changing what I had set it equal to. I fixed this by making next a soft copy, meaning that popping elements from it would leave the original element unchanged.
- Some of the less obvious paths between adjacent towns were missed when manually counting, e.g. (2,9), (32,39). This meant that resulting shortets paths given seemed odd when the code was run. After spotting these errors, I went back to sym and added in the missed edges.
- Whilst testing, I realised that I had used non-generic integers whilst doing loops, i.e. instead of using `len(all_cards)`, I had just used `52`, since that was the number I was working with. I made sure to change this, so that a change in the setup of the game (new cards, new board layout) wouldn't lead to problems in executing the program in the future.
- Since there are 2 of each entry/exit card, I have allowed for both cards to be the same, by changing `random.sample()` (without replacement) to `random.choices()` (with replacement). Since there are only 2 copies of each town card, this will suffice, but would need to be altered if the program would allow for several people choosing cards in a single execution. Another way to fix this would be to make each element in entry_cards appear twice. 
- When including error messages, I found myself either getting stuck in loops, or jumping over some checks, depending on what/how many loops I was repeating. I solved this breaking the program down into functions, then creating a run_program() function that would neatly organise the logic/flow through the solver.


Approach:
- Create an adjacency matrix/table/array, containing the number of steps between all pairs of adjacent towns.
- Use this alongside networkx to create a graph of the game board, where each node represents a town (indexed by the town number) and each edge represents the number of steps between adjacent towns.
- From this, create another array containing the shortest path between every pair of towns on the board (including non-adjacent).
- Randomly assign a valid dealt hand of cards.
- Create a list of all possible routes to visit these towns (whilst abiding by the rules of the game).
- Calculate the length of all of these possible routes.
- Find the shortest one/s, and print both the order that the player should visit the cards in their hand, but also all inbetweeen towns, to show a more detailed route.

Comments/Criticisms:
- I used the CodeInstitute template in order to make a workspace that could run python coding.
- The output is basic, i.e. text on the console. To make it something that is simple/usable by most people, some sort of front end should be paired with it.
- I didn't use git commit, as it was done as a project in my free time at home, so the regular structured approach I would otherwise have wasn't my priority. It was written on VSC on my home computer (Mac).
- This program was made to be very adaptable/generic. If the board was completely moved around, a new list of towns was created, a new list of entry/exit cards was created, then all that would need to be changed would be the construction of the lists town_cards, all_cards, entry_cards and the sym spreadsheet. Although this would still take some time, it would only be a matter of minutes to count the distances on a new board of a similar size, and mere seconds to recontruct the lists of cards.
- The largest contributor to running time is calculating the shortest route for each possible route, of which there are `number_of_town_cards!`. When playing with 12 town cards, then this is 12! = 479001600 operations, each of which is a series of many operations.