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

def print_statistics(player_wins, dealer_wins, ties, player_blackjacks, dealer_blackjacks, hands_played, running_count, true_count, remaining_cards):
    print("Results after playing through the shoe:")
    print("Player wins:", player_wins)
    print("Dealer wins:", dealer_wins)
    print("Ties:", ties)
    print("Player blackjacks:", player_blackjacks)
    print("Dealer blackjacks:", dealer_blackjacks)
    print("Hands played:", hands_played)
    print("Final running count:", running_count)
    print("True count:", true_count)
    print("Remaining cards in shoe", remaining_cards)

def print_hand_results(player_hand, dealer_hand, result):
    print("Player's Hand:", ", ".join([f"{card[0]} of {card[1]}" for card in player_hand]))
    print("Dealer's Hand:", ", ".join([f"{card[0]} of {card[1]}" for card in dealer_hand]))
    print("Result:", result)

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

    while len(deck) / (len(card_values) * len(card_suits) * deck_count) > (1 - shoe_penetration):
        print("Remaining cards in deck:", len(deck))
        if not deck:
            print("Deck is empty, exiting loop")
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

        print("All initial cards have been dealt. Remaining cards in deck:", len(deck))

        # check for dealer blackjack
        if calculate_hand_value(dealer_hand) == 21:
            dealer_blackjacks += 1
            # if dealer blackjack check for player blackjack
            if calculate_hand_value(player_hand) == 21:
                player_blackjacks += 1      
                hands_played += 1
                print_hand_results(player_hand, dealer_hand, "Push (both player and dealer have blackjack)")
                ties += 1
                continue

            dealer_wins += 1
            print_hand_results(player_hand, dealer_hand, "Dealer wins with blackjack")
            hands_played += 1
            
            continue  # Skip the rest of the hand

        print("Dealer blackjack check complete.")

        # Check for player blackjack
        if calculate_hand_value(player_hand) == 21:
            player_blackjacks += 1
            print_hand_results(player_hand, dealer_hand, "Player wins with blackjack")
            player_wins += 1
            hands_played += 1
            continue  # Skip the rest of the hand

        print("Player blackjack check complete.")

        # Player's turn
        while True:
            print("Player hand:", player_hand)
            player_action = basic_strategy(player_hand, dealer_hand[0])
            print("Player action calcuated: ", player_action)
            if player_action == 'h':
                if not deck:
                    break
                player_hand.append(deck.pop())
                running_count = calculate_running_count(player_hand[-1], running_count)
                print("Player hits, hand:", player_hand)
                if calculate_hand_value(player_hand) > 21:
                    break
            elif player_action == 's':
                print("Player stands")
                break
            elif player_action == 'p':
                print("Player splits")
                # Create two hands by splitting the pair
                hand1 = [player_hand[0], None]
                hand2 = [player_hand[1], None]
                running_count = calculate_running_count(hand1[1], running_count)
        
                # Play each hand individually
                for hand in [hand1, hand2]:
                    print("Playing split hand:", hand)
                    while True:
                        print("Hand value:", calculate_hand_value(hand))
                        action = basic_strategy(hand, dealer_hand[0])
                        print("Action:", action)
                        if action == 'h':
                            if not deck:
                                print("Deck is empty, cannot hit")
                                break
                            hand.append(deck.pop())
                            running_count = calculate_running_count(hand[-1], running_count)
                            print("Hit:", hand)
                            if calculate_hand_value(hand) > 21:
                                    print("Bust")
                                break
                        elif action == 's':
                            print("Stand")
                            break
                break

        print("Players turn complete. Remaining cards in deck:", len(deck))

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

        print("Dealers turn complete. Remaining cards in deck:", len(deck))

        # Determine winner
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        if player_value > 21:
            print_hand_results(player_hand, dealer_hand, "Dealer wins on player bust")
            dealer_wins += 1
        elif dealer_value > 21:
            print_hand_results(player_hand, dealer_hand, "Player wins on dealer bust")
            player_wins += 1
        elif player_value > dealer_value:
            print_hand_results(player_hand, dealer_hand, "Player wins with higher hand value")
            player_wins =+ 1
        elif dealer_value > player_value:
            print_hand_results(player_hand, dealer_hand, "Dealer wins with higher hand value")
            dealer_wins += 1
        else:
            print_hand_results(player_hand, dealer_hand, "Push (equal hand values)")
            ties += 1

        hands_played += 1
        print("End of iteration")

    print_statistics(player_wins, dealer_wins, ties, player_blackjacks, dealer_blackjacks, hands_played, running_count, true_count, len(deck))
    print("Simulation completed")

# Run the simulation with a deck size of 6, a shoe penetration of 75%, and a bet size of 10
simulate_blackjack(6, 0.75, 10)
