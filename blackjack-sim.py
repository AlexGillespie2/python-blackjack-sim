import random
import math

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

# Determine action based on basic strategy (adjusted for American rules)
def basic_strategy(player_hand, dealer_upcard, can_split):
    player_value = calculate_hand_value(player_hand)
    dealer_upcard_value = card_values[dealer_upcard[0]]

    if player_hand[0][0] == player_hand[1][0] and can_split:  # If pair
        if player_hand[0][0] == '8' or player_hand[0][0] == 'A':  # Split 8s and Aces
            return 'p'  # Split
        elif player_hand[0][0] == '10' or player_hand[0][0] == 'J' or player_hand[0][0] == 'Q' or player_hand[0][0] == 'K':  # Stand
            return 's'  # Stand
    if player_value >= 17:
        return 's'  # Stand
    elif player_value <= 11:
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
        player_action = basic_strategy(hand, dealer_up_card, number_of_splits < 4)
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

def simulate_blackjack(deck_count, shoe_penetration, bet_size, logging_during_hand = False, verbosity_level = 1):
    deck = create_deck(deck_count)
    player_profit = 0
    current_player_bet_size = bet_size
    player_wins = 0
    dealer_wins = 0
    ties = 0
    player_blackjacks = 0
    dealer_blackjacks = 0
    hands_played = 0
    running_count = 0
    true_count = 0

    def print_statistics():
        if verbosity_level == 1:
            print("Hands played:", hands_played)
            print("Player profit: ", player_profit)
            
        if verbosity_level == 2:
            print("Running count:", running_count)
            print("True count: ", true_count)
            print("Current player bet size: ", current_player_bet_size)

        if verbosity_level == 3:
            print("Player wins:", player_wins)
            print("Player blackjacks:", player_blackjacks)
            print("Dealer wins:", dealer_wins)
            print("Dealer blackjacks:", dealer_blackjacks)
            print("Ties:", ties)

        if verbosity_level == 4:
            print("Remaining cards in shoe", len(deck))


    while len(deck) / (len(card_values) * len(card_suits) * deck_count) > (1 - shoe_penetration):
        if not deck:
            print("Deck is empty, exiting loop")
            break

        true_count = calculate_true_count(running_count, len(deck))

        current_player_bet_size = bet_size
        player_profit -= current_player_bet_size

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
                player_profit =+ current_player_bet_size
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
            player_profit =+ current_player_bet_size * 2.5
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
            elif calculate_hand_value(p_hand) > dealer_value:
                if logging_during_hand:
                    print_hand_results(p_hand, dealer_hand, "Player wins with higher hand value")
                player_wins =+ 1
            elif dealer_value > calculate_hand_value(p_hand):
                if logging_during_hand:
                    print_hand_results(p_hand, dealer_hand, "Dealer wins with higher hand value")
                dealer_wins += 1
            else:
                if logging_during_hand:
                    print_hand_results(p_hand, dealer_hand, "Push (equal hand values)")
                ties += 1

        hands_played += 1
        print("End of iteration, statistics: ")
        print_statistics()

    print("Simulation completed")

# Run the simulation with a deck size of 6, a shoe penetration of 75%, and a bet size of 10
simulate_blackjack(6, 0.75, 10, False)
