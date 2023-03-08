# This is a demo written by ChatGPT.

import random

# Define the number of players, objects, and points per player
num_players = 19
num_objects = 19
num_points = 16

# Define the number of simulation rounds
num_rounds = 10000

# Define the strategies to compare
strategies = ["Strategic Allocation", "Spread Out", "Aggressive Bidding", "Wait and Watch", "Collaboration"]

# Initialize a dictionary to keep track of the number of wins for each strategy
wins = {strategy: 0 for strategy in strategies}

# Simulate the bidding process for each round
for i in range(num_rounds):
    # Initialize a dictionary to keep track of the points bid by each player for each object
    bids = {object: {player: 0 for player in range(num_players)} for object in range(num_objects)}
    
    # Randomly assign points to each player for each object
    for object in range(num_objects):
        points_left = num_points * num_players
        for player in range(num_players):
            if player == num_players - 1:
                bids[object][player] = points_left
            else:
                bid = random.randint(1, points_left - (num_players - player - 1))
                bids[object][player] = bid
                points_left -= bid
        
    # Determine the winning bidder for each object
    for object in range(num_objects):
        max_bid = max(bids[object].values())
        max_bidders = [player for player, bid in bids[object].items() if bid == max_bid]
        if len(max_bidders) == 1:
            wins[strategies[0]] += 1  # Strategic Allocation wins
        else:
            for j in range(1, len(strategies)):
                if strategies[j] == "Spread Out":
                    for player in max_bidders:
                        if bids[object][player] == 1:
                            wins[strategies[j]] += 1  # Spread Out wins
                            break
                elif strategies[j] == "Aggressive Bidding":
                    if len(max_bidders) == num_players:
                        wins[strategies[j]] += 1  # Aggressive Bidding wins
                        break
                elif strategies[j] == "Wait and Watch":
                    if len(max_bidders) > 1:
                        wins[strategies[j]] += 1  # Wait and Watch wins
                        break
                elif strategies[j] == "Collaboration":
                    if len(max_bidders) == 1:
                        wins[strategies[j]] += 1  # Collaboration wins
                        break

# Print the winning probabilities for each strategy
for strategy in strategies:
    print(f"{strategy}: {wins[strategy] / num_rounds}")