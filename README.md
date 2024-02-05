# Discovering Ireland Solver - PP3<!-- omit from toc -->

This project is a Python program where users who are playing the board game Discovering Ireland can enter their dealt cards and find out the shortest route to take in the game, thereby greatly increasing their chances of winning.

The program is visually pleasing and evokes positive emotions in the user. Instructions, colours and clear prompts make the program simple to follow.


[Deployed Program](https://discovering-ireland-solver-8aea73758694.herokuapp.com/)

## Table of Contents<!-- omit from toc -->
- [Introduction](#introduction)
  - [History](#history)
  - [Game Theory](#game-theory)
  - [Noteworthy Comments](#noteworthy-comments)
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

Discovering Ireland is a board game originally released by Gosling Games in 1987, and has gone on to sell over 250,000 copies. The newer version (which this program was written with in mind) was releasd in 2018. The playing board consists of 52 towns, each connected to some of the other towns by a number of steps/blocks. Each player is dealt 2 Entry/Exit Cards: these indicate where they must start and finish their game/journey. They also receive a predesignated number of Town Cards, which they must visit in between the Entry/Exit Cards. The number of Town Cards chosen must be at least 5 and is most commonly around 6-8, as anymore than this can lead to a very long game, especially with a larger number of players.

The player who visits all of the towns on their Town Cards and ends at their final Entry/Exit card wins.

[The game can be seen on their website](https://goslinggames.ie/product/discovering-ireland-board-game/). [The rulebook can be viewed/downloaded here](https://goslinggames.ie/wp-content/uploads/2018/10/Rules-For-Discovering-Ireland-2018.pdf).

### Game Theory

Whilst playing with my partner at home, we have often both been in the situation where it is unclear as to which route is the best/shortest to take. Since their is a relatively small number of towns, each connected to only a few other towns, it seemed apparent to me that one could create a graph that represents the game: each town being a node, and each pair of adjacent towns connected by an edge whose weight is the number of steps between said towns. From this, one could use `numpy` and `networkx` to find the shortest path. This means we can essentially reduce playing the game to a modified Travelling Salesman Problem (those unfamiliar with this problem can [read more about it here](https://en.wikipedia.org/wiki/Travelling_salesman_problem)). The modifications in this case are that we don't want to necessarily end where we started, and we only need to visit a subset of all vertices in the graph (but we may traverse all edges on the graph in our journey).

By creating a graph of the game, I can exploit properties and algorithms used in Graph Theory to systematically explore any/all routes simply through for loops in code, thereby ensuring that the resulting path is the shortest that exists. Due to the relatively small number of towns and Town Cards, this problem can be solved in seconds. For larger numbers of Town Cards, more computing power (or a lot more time) would be needed.

The number of Town Cards can in theory be up to $\lfloor\frac{\text{Number of Town Cards}}{\text{Number of Players}}\rfloor$. For a 2 player game, this would be $\lfloor\frac{46}{2}\rfloor = 23$. For a 3 player game, this would be $\lfloor\frac{46}{3}\rfloor = \lfloor 15.\dot{3}\rfloor = 15$. Due to the memory restrictions on the Heroku hosting platform, I have limited the number of Town Cards to 9. Any more than this causes the memory quota to be exceeded. For further information, [see below in Issues/Bugs](#issuesbugs). On my own computer at home, I encountered a runtime of around 45 seconds for 10 Town Cards; 6 minutes for 11 Town Cards; 45 minutes for 12 Town Cards. After 6 hours running, the program didn't terminate when 13 Town Cards were entered (which is understandable, as it must iterate through over 6 billion possible routes). 

### Noteworthy Comments

- All given shortest paths are symmetrical, i.e. if your given path is `[50, 52, 51, 48, 45, 40, 39]`, then this is the same length as `[39, 40, 45, 48, 51, 52, 50]`. Since this is always the case, I fixed the entry card (the starting point) and just created one order of each of these routes.
- Chance Cards, road blocks, other players' decisions (e.g. to use their Chance Card to send you to a different location on the board) are not taken into account, as these cannot be accuratley accounted for. It would take more than 500 lines of code to correctly predict human psychology during a game.
- Making a U-turn (i.e. visiting a town and then returning from the direction you came from) often includes wasted movements, since you can overshoot the town by $n$ steps, leading to you having to backtrack $n$ wasted steps again, adding a total of $2n$ steps to the path length. Compensating for this would lead to a much more in depth analysis of each route, as well as applying probability theory to the dice throws, so I chose therefore to ignore it in this case. In a future version, [I may come back to this](#future-improvementsdevelopment).
- The output is basic, i.e. text on the console. To make it something that would be more appealing to most people, some sort of front end should be paired with it.
- This program was made to be very adaptable/generic (as is the goal with writing code in general). If the towns on the board were moved around; a new list of towns was created; a new sublist of Entry/Exit Cards was created; then all that would need to be changed would be the construction of the lists `all_cards`, `entry_cards` and the `counted_distances` spreadsheet. Although this would still take some time, it would only be a matter of minutes to count the distances on a new board of a similar size, and mere seconds to recontruct the lists of cards. The code could also be adapted to other similar board games (such as [Ticket to Ride](https://www.daysofwonder.com/ticket-to-ride/)), although the slightly different rule set would require a slight change in the code's structure.

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

## User Testimonial

Christina - aged 32 - Plays Discovering Ireland regularly

"I was very interested to try out the program, but initially was a bit apprehensive as I am not the best when it comes to computers and programs. However, the program was very easy to follow and easy to understand. I liked the use of colour, and enjoyed the detailed results I got, this helped me create the oath taken during my game, which I ended up winning! I also like the timer function: although it's not a necessity, it's intreesting to see just how quickly the computer can calculate such a complicated problem!"

Jens - 27 - Studying Graph Theory as part of his Maths degree

"When I heard about the maths behind the program, I was interested, as I hadn't heard of this particular modified version of the Travelling Salesman Problem. After reading the instructions and having a look at the game board, I tried it out to see how well the program would perform. I also tried to trick it by giving an input I knew would confuse the program, but the error messages stopped any invalid input from being allowed. When I looked at the source code, I could see that the networkx module was incredibly easy to use, and the way the information is handled and laid out is very easy to make sense of. I'll be sure to explore networkx when I'm doing my projects in the future, and it's good to know I can refer back to this program to remind me how it works!"

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

Find the miniminum value/s in `route_lengths` and the corresponding entry in `all_routes` for this/these. These will then be printed clearly for the user, highlighting when they visit one of the towns corresponding to one of their cards. 


### Game Flow/Logic



### Banner

I wanted a large banner with the title of the program to be what greeted the user once the program was loaded. I also wanted there to be space underneath for a welcome messange and initial prompt. Since I was limited to a $80 \times 24$ terminal, this meant there was some trial and error in getting the size right, but I am happy with the result.

### Colour Scheme

The yellow and green used in the prompts and printed result/s match the colour of the Entry/Exit and Town Cards respectively. I felt this was suitable to use, as it was another way of guiding the user through the program.

I used red for error messages, as people often associate the colour red with warnings; errors; important information.

### Other Features

- Printing the users input directly after it is recieved in order to check that the information received is correct. This gives the user the chance to check for any mistakes, and to restart the input if that is the case.

- Error validation: ensuring that the input is of exactly the correct form. This includes checking if input only contains spaces and integers (as requested); that the numbers are in the range 1 - 52; that Town Cards are entered when asked for Town Cards; that Entry/Exit cards anre entered when asked for Entry/Exit Cards; that no duplicate Town Cards are entered. Here, we note that duplicate Entry/Exit cards are allowed, as there are 2 of each in the game, whereas there is only 1 of each Town Card, so no Town Card duplicates are allowed. This also would be a trivial card, as any duplicates would just be a wasted card. I also created `yes_inputs` and `no_inputs`, which allow several variationns of `YES` and `NO` to be accepted, to allow for a missed letter/spelling mistake/lower case letters. It is also important to note that an incorrect input can often lead to more than 1 error (e.g. if, when prompted to enter Town Cards, the user enters a non-integer value as well as an Entry/Exit card). Rather than flooding the screen with several error messages, I decided to just print one. If the user then fixed this one error and not the other, another relevant error message would appear alerting them of the problem.

- Timer: the user is shown how long the calculation has taken. This is purely to satisfy curiosity, and was a feature that I created during construction and testing, but users have responded well to it, so I left it in.

## Technology \& Resources

- **IDE** : Visual Studio Code
- **Languages** : Python for the program. Markdown for this README
- **Template** : The CodeInstitute template was used in order to install all the relevant tools for the code to function.
- [Github](https://github.com/) was used to host the project. I used `git commit` regularly to create versions of the project at regular intervals. This meant that I could be more precise if I needed to `git reset`.
- [Heroku](https://www.heroku.com/) was used to deploy the program.
- [draw.io](https://app.diagrams.net/) was used to create the flowcharts.
- [fsymbols](https://fsymbols.com/generators/carty/) was used to create the banner.
- [Code Institute Python Linter](https://pep8ci.herokuapp.com/) was used for PEP8 validation.
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Glossary/Python) was used for further information on different Python modules/properties.

## Deployment

### How to Clone Repository

1. Go to the [GitHub repository](https://github.com/DiarmuidHenry/Project-03/).
2. Click the green **Code** drop down button.
3. Click **HTTPS** and copy the URL.
4. Open your IDE, and open a terminal.
5. Type `git clone url`, replacing `url` with the URL copied in step 3.

### How to set up Google Sheets API

1.

### How to deploy to Heroku

1. Log in to [Heroku](https://www.heroku.com/). If you do not already have an account, you can [sign up here](https://signup.heroku.com/).
2. Click **Create new app** on the Heroku Dashboard. Give the app a unique name. Select your region, click **Create app**.
3. Go to the **Settings** tab, click on **Reveal Config Vars**
4. In the **KEY** field, enter `CREDS`. In the **VALUE** field, copy and paste the entire `creds.json` file from the project directory. Click **Add**.
In the **KEY** field, enter `PORT`. In the **VALUE** field, enter **8000**. Click **Add**.
5. Scroll down, click **Add buildpack**. Select **python**, then click **Save changes**. Select **nodejs**, then click **Save changes**. *It is important that `heroku/python` appers above `heroku/nodejs`. If this is not the case, they can be rearranged into the correct order*. 
6. Go to the **Deploy** tab. Beside **Deployment method**, click **GitHub**, then confirm by clicking **Connect to GitHub**.
7. Under **Search for a repository to connect to**, type the name of the repo (whether that be the name of this repo, or of the one you have cloned). Click **Search**, then click **Connect** when the repo name appears. The Heroku app is now linked to the GitHub repo.
8. If you would like Heroku to manually update the app every time you push chances to GitHub, click on **Enable Automatic Deploys**. (This is optional).
9. Deploy the app by scrolling down and clicking **Deploy Branch**. Heroku will show you the deployment logs as it builds the app. This will take a few seconds.
10. When the app is finished being built, a message will appear saying **Your app was successfully deployed**. Click the **View** button to view the app (opens in a new tab).


## Issues/Bugs

### Resolved

- Using `pop(0)` whilst calculating results list lead to subsequent items in lists being altered and shortened. After reading up on it, this is because I wasn't just changing `next_result`, but I was also changing what I had set it equal to. I fixed this by making next a soft copy, meaning that popping elements from it would leave the original object unchanged.
- Some of the less obvious paths between adjacent towns were missed when manually counting, e.g. $(2,9)$, $(32,39)$. This meant that resulting shortest paths given seemed odd/incorrect when the program was run. After spotting these errors, I went back to `counted_distances` and added in the missing values.
- Whilst testing, I realised that I had used non-generic integers whilst doing loops, i.e. instead of using `len(all_cards)`, I had just used `52`, since that was the number I was working with. I made sure to change this, so that a change in the setup of the game (new cards, new board layout) wouldn't lead to problems in executing the program in the future. I didn't extend this to the Instructions, as this would need to be rewritten if the game in question was to change.
- When testing in the early stages, I used `random` to create a hand, which I could then run the program with. I began seeing that the Entry/Exit cards were never the same, even though this is allowed in the game. This was due to me using `random.sample()` (without replacement) to `random.choices()` (with replacement). Since there are only 2 copies of each Town card, this will suffice, but would need to be altered if the program would allow for several people choosing cards in a single execution. Another way to fix this would be to make each element in `entry_cards` appear twice. However, for the current purpose and function of this program, my current solution is fine.
- When including error messages, I found myself either getting stuck in loops, or jumping over some checks, depending on what/how many loops I was repeating. I solved this breaking the program down into functions, then creating a `run_program()` function that would neatly organise the logic/flow through the solver.
- Program was crashing when more than 9 Town Cards were given. This was due to memory being exceeded. I fixed this by ADDING AN ERROR MESSAGE / LIMITING THE NUMBER OF TOWN CARDS THE USER MAY ENTER.

### Unresolved

- I had intended on reshaping `all_shortest_paths` as a 3d array, rather than a list of lists. However, I ran into trouble creating and indexing this 3d array. This led to inelegant indexing of the variable `next_result`. Since the code still functions, I wouldn't consider this a bug as such. However, it is something that could be improved.

## Testing \& Validation

### Functional Testing

|Test Item|Test Carried Out|Result|Pass/Fail|
|-------------|------------------|-----------|-------|
|Instructions prompt|Type `YES` or any element from `yes_inputs`|Instructions appear, followed by the first prompt of the program|PASS|
||Type `NO` or any element from `no_inputs`|The first prompt of the program appears|PASS|
||Type anything other than the elements in `no_inputs` or `yes_inputs`|Input is not accepted. `Invalid input. Please type YES or NO` appears.|PASS|
|Entry/Exit Cards prompt|Type nothing|Input is not accepted. `Invalid input. Players must have exactly 2 Entry/Exit cards.` appears. User is again asked to enter their Entry/Exit Cards.|PASS|
||Type something other than spaces and integers, e.g. `5 i`, `5_9`, `4 a`, `five nine`, `YES`|Input is not accepted. `Invalid input. Input must only contain spaces and integers` appears. User is again asked to enter their Entry/Exit Cards.|PASS|
||Type `0` and/or an integer greater than the highest Entry/Exit Card ($50$), e.g. `0 5`, `39 51`, `88 5 39 65`|Input is not accepted. `Invalid input. Inputs must be between 5 and 50 (inclusive)` appears. User is again asked to enter their Entry/Exit Cards.|PASS|
||Type exactly 1 valid Entry/Exit Cards e.g. `5`, `39`|Input is not accepted. `Invalid input. Players must have exactly 2 Entry/Exit cards.` appears. User is again asked to enter their Entry/Exit Cards.|PASS|
||Type 3 or more valid Entry/Exit Cards e.g. `5 9 39`, `5 5 5`|Input is not accepted. `Invalid input. Players must have exactly 2 Entry/Exit cards.` appears. User is again asked to enter their Entry/Exit Cards.|PASS|
||Type something including a Town Card e.g. `5 8`, `1`|Input is not accepted. `Invalid input. Please enter only your Entry/Exit cards. Do not include any Town cards.` appears. User is again asked to enter their Entry/Exit Cards.|PASS|
|Town Cards prompt|Type nothing|Input is not accepted. `Invalid input. Players must have at least 1 Town Card.` appears. User is again asked to enter their Town Cards.|PASS|
||Type something other than spaces and integers, e.g. `2 e 4 6`, `12 51 17_19`, `5 a`, `two three eleven seventeen thirty-eight`, `NO`|Input is not accepted. `Invalid input. Input must only contain spaces and integers` appears. User is again asked to enter their Town Cards.|PASS|
||Type `0` and/or an integer greater than the highest Town Card ($52$), e.g. `12 37 49 0 16`, `30 32 14 53`, `77 5 39 4`|Input is not accepted. `Invalid input. Inputs must be between 1 and 52 (inclusive)` appears. User is again asked to enter their Town Cards.|PASS|
|||Input is not accepted. `Invalid input. Inputs must be between 1 and 52 (inclusive)` appears. User is again asked to enter their Town Cards.|PASS|



### PEP8 Validation

## Future Improvements/Developments

- Add a front end, to improve the overall look and emotional response of the user. A lot of peolpe would be turned away by a terminal as they might be worried that it is 'too technical', so making it look more like a regular website, and having the input being through an input form using JavaScript would make it more accessible to most people.
- As mentioned in [Noteworthy Comments](#noteworthy-comments), I would like to factor in the fact that players often overshoot their town and waste movements when amknig a U-turn in their route. To compensate for this, I could firstly favour routes without U-turns whilst creating the suggested routes, as routes without U-turns have no wasted moves (here we are ignoring Chance Cards, roadblocks etc.). This could be done by adding an extra condition whilst checking/removing duplicate routes, something along the lines of `if results_lists[i][j] = results_lists[i][j+2]`. Going deeper into Game Theory, I would then need to use Probability Theory to caclculate the average number of wasted steps in such as instance, and add this (multiplied by the number of U-turns in a path) to the length of each relevant path.
- Fix the problem with indexing of `next_result` as was [mentioned in Issues/Bugs: Unresolved](#unresolved)