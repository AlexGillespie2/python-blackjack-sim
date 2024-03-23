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
def basic_strategy(player_hand, dealer_upcard):
    player_value = calculate_hand_value(player_hand)
    dealer_upcard_value = card_values[dealer_upcard[0]]

    if player_hand[0][0] == player_hand[1][0]:  # If pair
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

def simulate_blackjack(deck_count, shoe_penetration, bet_size):
    deck = create_deck(deck_count)
    player_bankroll = 0
    current_player_bet_size = bet_size
    player_wins = 0
    dealer_wins = 0
    ties = 0
    player_blackjacks = 0
    dealer_blackjacks = 0
    hands_played = 0
    running_count = 0
    true_count = 0

    while len(deck) / (len(card_values) * len(card_suits) * deck_count) > (1- shoe_penetration):
        if not deck:
            break

        true_count = calculate_true_count(running_count, len(deck))

        current_player_bet_size = bet_size
        player_bankroll -= current_player_bet_size

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

        # check for dealer blackjack
        if calculate_hand_value(dealer_hand) == 21:
            dealer_blackjacks += 1
            # if dealer blackjack check for player blackjack
            if calculate_hand_value(player_hand) == 21:
                player_blackjacks += 1      
                hands_played += 1
                ties += 1
                continue

            dealer_wins += 1
            hands_played += 1
            
            continue  # Skip the rest of the hand

        # Check for player blackjack
        if calculate_hand_value(player_hand) == 21:
            player_blackjacks += 1
            player_wins += 1
            hands_played += 1
            continue  # Skip the rest of the hand

        # Player's turn
        while True:
            player_action = basic_strategy(player_hand, dealer_hand[0])
            if player_action == 'h':
                if not deck:
                    break
                player_hand.append(deck.pop())
                running_count = calculate_running_count(player_hand[-1], running_count)
                if calculate_hand_value(player_hand) > 21:
                    dealer_wins += 1
                    break
            elif player_action == 's':
                break

        # Dealer's turn
        while calculate_hand_value(dealer_hand) < 17:
            if not deck:
                break
            dealer_hand.append(deck.pop())
            running_count = calculate_running_count(dealer_hand[-1], running_count)

        # Determine winner
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        if player_value > 21:
            dealer_wins += 1
        elif dealer_value > 21 or player_value > dealer_value:
            player_wins += 1
        elif dealer_value > player_value:
            dealer_wins += 1
        else:
            ties += 1

        hands_played += 1

    print("Results after playing through the shoe:")
    print("Player wins:", player_wins)
    print("Dealer wins:", dealer_wins)
    print("Ties:", ties)
    print("Player blackjacks:", player_blackjacks)
    print("Dealer blackjacks:", dealer_blackjacks)
    print("Hands played:", hands_played)
    total_bet = bet_size * hands_played
    print("Final running count:", running_count)
    true_count = calculate_true_count(running_count, len(deck))
    print("True count:", true_count)

# Run the simulation with a deck size of 6, a shoe penetration of 75%, and a bet size of 10
simulate_blackjack(6, 0.75, 10)
