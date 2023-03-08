import random
import copy
import math

# Initialize several parameters
# Define the number of objects (equaling to the number of players) and points per player
num_objects = 19
num_points = 16

# Define the list of objects and players
list_objects_original = []
list_players = []
for i in range(num_objects):
    list_objects_original.append(f"object_{i}") 
    list_players.append(f"player_{i}")


# Define a function describing bidding activity
def bid(player_name, bidding_points, object_name):
    objects_bids_players[object_name][player_name] += bidding_points
    objects_bids_overall[object_name] += bidding_points
    points_left[player_name] -= bidding_points
    return


# Define the strategies to compare
strategies = ["All_In", "Spread_Out", "Linear_Allocation", "Exponential_Allocation"]

# Define the functions of the action details of each strategy
# "All_In" strategy: Bid all the points to the most-wanted object
def All_In(player_name):
    bid(player_name, points_left[player_name], players_wanting_rank[player_name][0])
    return

# "Spread_Out" strategy: Bid one point to almost every object
def Spread_Out(player_name):
    for i in range(num_points):
        if points_left[player_name] == 0:
            return
        bid(player_name, 1, players_wanting_rank[player_name][i])
    return

# "Linear_Allocation" strategy: Allocate the points linear
def Linear_Allocation(player_name):
    m = int(((8*num_points + 1)**(1/2) - 1)//2)
    for i in range(m):
        bid(player_name, i+1, players_wanting_rank[player_name][m - i - 1])
    if points_left[player_name] == 0:
        return
    else:
        for j in range(points_left[player_name]):
            bid(player_name, 1, players_wanting_rank[player_name][m + j])
        return

# "Exponential_Allocation" strategy: Allocate the points exponentially by a factor of 2
def Exponential_Allocation(player_name):
    n = int(math.log2(num_points + 1)) - 1
    for i in range(n):
        bid(player_name, 2**(i+1), players_wanting_rank[player_name][n - i - 1])
    if points_left[player_name] == 0:
        return
    else:
        for j in range(points_left[player_name]):
            bid(player_name, 1, players_wanting_rank[player_name][n + j])
        return

# Define a dictionary to connect the strategies' names to their functions
strategies_functions = {}   
for i in range(len(strategies)):
    strategies_functions[strategies[i]] = strategies[i]

# Define a dictionary to keep track of the number of wins for each strategy
strategies_wins = {strategy: 0 for strategy in strategies}


# Define the number of simulation rounds
num_rounds = 1000

# Simulate the bidding process for each round
for i in range(num_rounds):
    # Recopy the list of objects and players, which are initialized in every round
    list_objects = copy.deepcopy(list_objects_original)
    list_players_competing = copy.deepcopy(list_players)
    list_players_determined = []
    list_players_vain = []


    # Initialize several dictionaries to keep track of... 
    # the points bid by each player for each object，
    objects_bids_players = {object: {player: 0 for player in list_players} for object in list_objects}

    # the overall bids that every object gets，
    objects_bids_overall = {object: 0 for object in list_objects} 

    # and the left points of every player
    points_left = {player: num_points for player in list_players}


    # Define a dictionary to record the rank of their wanted objects
    players_wanting_rank = {}
    for j in range(num_objects):
        players_wanting_rank[list_players[j]] = random.sample(list_objects, num_objects)
    
    # Define a dictionary to record the players and corresponding strategies
    players_strategies = {}
    for j in range(num_objects):
        players_strategies[list_players[j]] = strategies[random.randint(0, len(strategies)-1)]
    

    # Start the bidding process, making use of the sameness of the strategies' name and its function
    for j in range(num_objects):
        eval(players_strategies[list_players[j]] + f'(list_players[{j}])')


    # Determine the winner of every object
    # Dictionary "objects_bids_overall" is sorted into a list whose elements are tuples
    objects_bids_overall_sorted = sorted(objects_bids_overall.items(), key = lambda x: x[1])

    # Define a dictionary to record the winner of each object
    winners = {} 
    for j in range(num_objects):
        object_name = objects_bids_overall_sorted[j][0]

        # Find the player who bid the most to every object
        # Define a dictionary of the players who bid for the object
        dic_players_sorted = sorted(objects_bids_players[object_name].items(), key = lambda x: x[1], reverse = True)
        list_most_bidders = []
        for k in range(num_objects):
            if dic_players_sorted[k][0] not in list_players_determined:
                list_most_bidders.append(dic_players_sorted[k][0])
                break
            else:
                continue

        # Randomly kick the unfortunate player into the "list_players_vain"
        if len(list_most_bidders) == 1:
            winner = list_most_bidders[0]
        else:
            winner = list_most_bidders[random.randint(0, len(list_most_bidders) - 1)]
            list_players_determined.append(winner)
            list_most_bidders.remove(winner)
            list_players_vain.extend(list_most_bidders)
        
        winners[object_name] = winner
        strategies_wins[players_strategies[winner]] += 1 # Calculate the scores of the strategies

    # TO-DO: Calculate the bonus scores

    # Check: If every player's left points == 0; if every player and every object matches one by one

# Print results
print(strategies_wins.items())