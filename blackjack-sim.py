import random
import math
import csv

# Define card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Define card suits
card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Define a function to create a deck of cards
def create_deck(num_decks):
    deck = []
    for _ in range(num_decks):
        for value in card_values:
            for suit in card_suits:
                deck.append((value, suit))
    random.shuffle(deck)
    return deck

# Define a function to calculate the value of a hand
def calculate_hand_value(hand):
    value = 0
    num_aces = 0
    for card in hand:
        value += card_values[card[0]]
        if card[0] == 'A':
            num_aces += 1
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def is_soft_hand(hand):
    """
    Determine if a hand is a soft hand in blackjack.

    Parameters:
    - hand (list of tuples): The hand to check, represented as a list of card tuples.

    Returns:
    - bool: True if the hand is a soft hand, False otherwise.
    """
    total_value = 0  # Initialize total value

    # Count the total value of the hand, considering Aces as 1s by default
    for card in hand:
        if card[0] == 'A':
            total_value += 1  # Add 1 for Ace
        else:
            total_value += card_values.get(card[0], 10)

    # If the total value is greater than 21, it can't be a soft hand
    if total_value > 21:
        return False

    # If the total value is less than or equal to 21 and there's an Ace in the hand,
    # check if counting that Ace as 1 keeps the total value under or equal to 21
    for card in hand:
        if card[0] == 'A' and total_value + 10 <= 21:
            return True
    
    return False

# Determine action based on basic strategy (adjusted for American rules)
def basic_strategy(player_hand, dealer_upcard, can_split, can_double):
    player_value = calculate_hand_value(player_hand)
    dealer_upcard_value = card_values[dealer_upcard[0]]

    if player_hand[0][0] == player_hand[1][0] and can_split:  # If pair
        if player_hand[0][0] == '8' or player_hand[0][0] == 'A':  # Split 8s and Aces
            return 'p'  # Split
        elif player_hand[0][0] == '10' or player_hand[0][0] == 'J' or player_hand[0][0] == 'Q' or player_hand[0][0] == 'K':  # Stand
            return 's'  # Stand
        elif player_hand[0][0] == '9':
            if 2 <= dealer_upcard_value <= 6 or 8 <= dealer_upcard_value <= 9:
                return 'p'
            else:
                return 's'
        elif player_hand[0][0] == '7':
            if 2 <= dealer_upcard_value <= 7:
                return 'p'
            else:
                return 'h'
        elif player_hand[0][0] == '6':
            if 2 <= dealer_upcard_value <= 6:
                return 'p'
            else:
                return 'h'
        elif player_hand[0][0] == '5':
            if 2 <= dealer_upcard_value <= 9:
                return 'd'
            else:
                return 'h'
        elif player_hand[0][0] == '4':
            if 5 <= dealer_upcard_value <= 6:
                return 'p'
            else:
                return 'h'
        elif player_hand[0][0] == '3' or player_hand[0][0] == '2':
            if 2 <= dealer_upcard_value <= 7:
                return 'p'
            else:
                return 'h'

    if is_soft_hand(player_hand):
        if player_value >= 19:
            return 's'
        elif player_value == 18:
            if 3 <= dealer_upcard_value <= 6:
                return 'd'
            elif dealer_upcard_value >= 9:
                return 'h'
            else:
                return 's'
        elif player_value == 17:
            if 3 <= dealer_upcard_value <= 6:
                return 'd'
            else:
                return 'h'
        elif 15 <= player_value <= 16:
            if 4 <= dealer_upcard_value <= 6:
                return 'd'
            else:
                return 'h'
        elif 13 <= player_value <= 14:
            if 5 <= dealer_upcard_value <= 6:
                return 'd'
            else:
                return 'h'

    if player_value >= 17 and not is_soft_hand(player_hand):
        return 's'  # Stand
    elif player_value == 11:  # Double down if total is 11
        if can_double:
            return 'd'  # Double down
        else:
            return 'h'
    elif player_value == 9:
        if 3 <= dealer_upcard_value <= 6 and can_double:
            return 'd'  # Double down
        else:
            return 'h'  # Hit
    elif player_value == 10:  # Double down if total is 10
        if 2 <= dealer_upcard_value <= 9 and can_double:
            return 'd'  # Double down
        else:
            return 'h'  # Hit
    elif player_value == 12:
        if 2 <= dealer_upcard_value <= 3 or 7 <= dealer_upcard_value <= 11:
            return 'h'  # Hit
        else:
            return 's'  # Stand
    elif 13 <= player_value <= 16:
        if 2 <= dealer_upcard_value <= 6:
            return 's'  # Stand
        else:
            return 'h'  # Hit
    elif 5 <= player_value <= 8:
        return 'h'  # Hit

# Update running count based on the card dealt
def calculate_running_count(card, running_count):
    card_value = card_values[card[0]]
    if card_value in [2, 3, 4, 5, 6]:
        running_count += 1
    elif card_value == 10:
        running_count -= 1
    return running_count

def calculate_true_count(running_count, deck_length):
    return math.floor(running_count / round(deck_length / 52))

def print_hand_results(player_hand, dealer_hand, result):
    print("Player's Hand:", ", ".join([f"{card[0]} of {card[1]}" for card in player_hand]))
    print("Dealer's Hand:", ", ".join([f"{card[0]} of {card[1]}" for card in dealer_hand]))
    print("Result:", result)

def play_players_turn(hand, dealer_up_card, deck, running_count, number_of_splits, logging_during_hand = False):
    while True:
        if logging_during_hand:
            print("Player hand:", hand)
        player_action = basic_strategy(hand, dealer_up_card, number_of_splits < 4 and len(hand) == 2, len(hand) == 2)
        if logging_during_hand:
            print("Player action calcuated: ", player_action)
        if player_action == 'h':
            if not deck:
                break
            hand.append(deck.pop())
            running_count = calculate_running_count(hand[-1], running_count)
            if logging_during_hand:
                print("Player hits, hand:", hand)
            if calculate_hand_value(hand) > 21:
                return [hand], running_count
        elif player_action == 'd':
            if not deck:
                break
            hand.append(deck.pop())
            running_count = calculate_running_count(hand[-1], running_count)
            if logging_during_hand:
                print("Player doubles, hand:", hand)
            return [hand], running_count
        elif player_action == 's':
            if logging_during_hand:
                print("Player stands")
            return [hand], running_count
        elif player_action == 'p':
            if logging_during_hand:
                print("Player splits: ", hand)
            hand_one = [hand[0], deck.pop()]
            running_count = calculate_running_count(hand_one[1], running_count)
            hand_two = [hand[1], None]
            number_of_splits += 1
            if logging_during_hand:
                print("Hand One from split #", number_of_splits, ": ", hand_one)
            # Cant hit aces split
            if hand_one[0][0] == 'A' and hand_one[1][0] != 'A':
                hands_from_hand_one = [hand_one]
            else:
                hands_from_hand_one, running_count = play_players_turn(hand_one, dealer_up_card, deck, running_count, number_of_splits)

            hand_two = [hand_two[0], deck.pop()]
            running_count = calculate_running_count(hand_two[1], running_count)
            if logging_during_hand:
                print("Hand two from split #", number_of_splits, ": ", hand_two)
            # Cant hit aces split
            if hand_two[0][0] == 'A' and hand_two[1][0] != 'A':
                hands_from_hand_two = [hand_two]
            else:
                hands_from_hand_two, running_count = play_players_turn(hand_two, dealer_up_card, deck, running_count, number_of_splits)

            return (hands_from_hand_one + (hands_from_hand_two)), running_count

    return [hand], running_count

def simulate_blackjack_shoe(deck_count, shoe_penetration, min_bet_size, hand_csv_writer, logging_during_hand = False, verbosity_level = 1):
    deck = create_deck(deck_count)
    player_profit_this_shoe = 0
    current_player_bet_size = min_bet_size
    player_wins = 0
    dealer_wins = 0
    ties = 0
    player_blackjacks = 0
    dealer_blackjacks = 0
    hands_played = 0
    running_count = 0
    true_count = 0

    def print_statistics():
        if verbosity_level >= 1:
            print("Hands played:", hands_played)
            print("Player profit: ", player_profit_this_shoe)
            
        if verbosity_level >= 2:
            print("Running count:", running_count)
            print("True count: ", true_count)
            print("Current player bet size: ", current_player_bet_size)

        if verbosity_level >= 3:
            print("Player wins:", player_wins)
            print("Player blackjacks:", player_blackjacks)
            print("Dealer wins:", dealer_wins)
            print("Dealer blackjacks:", dealer_blackjacks)
            print("Ties:", ties)

        if verbosity_level >= 4:
            print("Remaining cards in shoe", len(deck))


    while len(deck) / (len(card_values) * len(card_suits) * deck_count) > (1 - shoe_penetration):
        if not deck:
            print("Deck is empty, exiting loop")
            break

        true_count = calculate_true_count(running_count, len(deck))

        current_player_bet_size = min_bet_size * max(true_count, 1)
        player_profit_this_shoe -= current_player_bet_size

        # All Player's first card
        player_hand = [deck.pop(), None]
        running_count = calculate_running_count(player_hand[0], running_count)

        # dealers first card
        dealer_hand = [deck.pop(), None]
        running_count = calculate_running_count(dealer_hand[0], running_count)

        # All Players second card
        player_hand = [player_hand[0], deck.pop()]
        running_count = calculate_running_count(player_hand[0], running_count)

        # dealers second card
        dealer_hand = [dealer_hand[0], deck.pop()]
        running_count = calculate_running_count(dealer_hand[0], running_count)

        if logging_during_hand:
            print("All initial cards have been dealt. Remaining cards in deck:", len(deck))

        # check for dealer blackjack
        if calculate_hand_value(dealer_hand) == 21:
            dealer_blackjacks += 1
            # if dealer blackjack check for player blackjack
            if calculate_hand_value(player_hand) == 21:
                player_blackjacks += 1      
                hands_played += 1
                if logging_during_hand:
                    print_hand_results(player_hand, dealer_hand, "Push (both player and dealer have blackjack)")
                ties += 1
                player_profit_this_shoe += current_player_bet_size
                continue

            dealer_wins += 1
            if logging_during_hand:
                print_hand_results(player_hand, dealer_hand, "Dealer wins with blackjack")
            hands_played += 1
            
            continue  # Skip the rest of the hand

        if logging_during_hand:
            print("Dealer blackjack check complete.")

        # Check for player blackjack
        if calculate_hand_value(player_hand) == 21:
            player_blackjacks += 1
            if logging_during_hand:
                print_hand_results(player_hand, dealer_hand, "Player wins with blackjack")
            player_wins += 1
            player_profit_this_shoe += (current_player_bet_size * 2.5)
            hands_played += 1
            continue  # Skip the rest of the hand

        if logging_during_hand:
            print("Player blackjack check complete.")

        all_players_hands, running_count = play_players_turn(player_hand, dealer_hand[0], deck, running_count, 0, logging_during_hand)

        if logging_during_hand:
            print("Players turn complete. Remaining cards in deck:", len(deck))
            print("All player hands: ", all_players_hands)

        # Dealer's turn
        while True:
            if not deck:
                break
            dealer_value = calculate_hand_value(dealer_hand)
            if dealer_value >= 17 and ('A' not in [card[0] for card in dealer_hand]):  # Stand on hard 17
                break
            elif dealer_value >= 18:  # Stand on any value above 17
                break
            if not deck:
                break
            dealer_hand.append(deck.pop())
            running_count = calculate_running_count(dealer_hand[-1], running_count)

        if logging_during_hand:
            print("Dealers turn complete. Remaining cards in deck:", len(deck))

        # Determine winner
        dealer_value = calculate_hand_value(dealer_hand)
        for p_hand in all_players_hands:
            if calculate_hand_value(p_hand) > 21:
                if logging_during_hand:
                    print_hand_results(p_hand, dealer_hand, "Dealer wins on player bust")
                dealer_wins += 1
            elif dealer_value > 21:
                if logging_during_hand:
                    print_hand_results(p_hand, dealer_hand, "Player wins on dealer bust")
                player_wins += 1
                player_profit_this_shoe += (current_player_bet_size * 2)
            elif calculate_hand_value(p_hand) > dealer_value:
                if logging_during_hand:
                    print_hand_results(p_hand, dealer_hand, "Player wins with higher hand value")
                player_wins =+ 1
                player_profit_this_shoe += (current_player_bet_size * 2)
            elif dealer_value > calculate_hand_value(p_hand):
                if logging_during_hand:
                    print_hand_results(p_hand, dealer_hand, "Dealer wins with higher hand value")
                dealer_wins += 1
            else:
                if logging_during_hand:
                    print_hand_results(p_hand, dealer_hand, "Push (equal hand values)")
                ties += 1
                player_profit_this_shoe += current_player_bet_size

        hands_played += 1
        # Write statistics to CSV
        hand_csv_writer.writerow([hands_played, player_profit_this_shoe, running_count, true_count, current_player_bet_size, player_wins, dealer_wins, ties, player_blackjacks, dealer_blackjacks])
        print("End of iteration, statistics: ")
        print_statistics()
        
    return player_wins, dealer_wins, ties, hands_played, player_profit_this_shoe

# Run the simulation with a deck size of 6, a shoe penetration of 75%, and a bet size of 10
# Open CSV file for writing
with open('./blackjack_hand_results.csv', mode='w', newline='') as file1, open('./blackjack_shoe_results.csv', mode='w', newline='') as file2:
    hand_writer = csv.writer(file1)
    # Write header row
    hand_writer.writerow(['Hand', 'Player Profit', 'Running Count', 'True Count', 'Current Bet Size', 'Player Wins', 'Dealer Wins', 'Ties', 'Player Blackjacks', 'Dealer Blackjacks'])
    
    shoe_writer = csv.writer(file2)
    shoe_writer.writerow(['Shoe', 'Total Player Profit', 'Net Profit Change', 'Player Wins', 'Dealer Wins', 'Ties'])
    
    current_player_profit = 0
    total_player_wins = 0
    total_dealer_wins = 0
    total_ties = 0
    total_hands_played = 0
    total_shoes_played = 0
    hands_to_play = 10000

    def print_total_stats():
        print("Current Player Profit: ", current_player_profit)
        print("Total Player Wins: ", total_player_wins)
        print("Total Dealer Wins: ", total_dealer_wins)
        print("Total Ties: ", total_ties)
        print("Total Hands Played: ", total_hands_played)
        print("Total Shoes Played: ", total_shoes_played)

    while True:
        new_player_wins, new_dealer_wins, new_ties, new_hands_played, net_profit_this_shoe = simulate_blackjack_shoe(6, 0.75, 10, hand_writer, False, 2)
        total_player_wins += new_player_wins
        total_dealer_wins += new_dealer_wins
        total_ties += new_ties
        total_hands_played += new_hands_played
        total_shoes_played += 1
        current_player_profit += net_profit_this_shoe
        
        shoe_writer.writerow([total_shoes_played, current_player_profit, net_profit_this_shoe, new_player_wins, new_dealer_wins, new_ties])
        print_total_stats()

        if total_hands_played > hands_to_play:
            break
