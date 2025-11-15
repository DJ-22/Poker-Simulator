import random
from typing import List, Tuple, Optional
from cards import RANKS, SUITS, makeCard


Card = Tuple[str, str]
Deck = List[Card]


def newDeck() -> Deck:
    """
    Create a new standard deck of 52 playing cards.

    Returns:
        Deck: A list of tuples representing the deck of cards.
    """
            
    return [makeCard(rank, suit) for suit in SUITS for rank in RANKS] 

def shuffleDeck(deck: Deck) -> None:
    """
    Shuffle the given deck of cards in place.

    Args:
        deck (Deck): A list of tuples representing the deck of cards.
    """
    
    random.shuffle(deck)

def dealOne(deck: Deck) -> Optional[Card]:
    """
    Deal one card from the top of the deck.

    Args:
        deck (Deck): A list of tuples representing the deck of cards.
    """
    if deck:
        return deck.pop()
    
    return None
    
def burn(deck: Deck, num: int = 1) -> None:
    """
    Burn (remove) a specified number of cards from the top of the deck.

    Args:
        deck (Deck): A list of tuples representing the deck of cards.
        num (int): The number of cards to burn. Default is 1.
    """
    
    if num < 0:
        raise ValueError("Number of cards to burn must be non-negative.")
    
    for _ in range(num):
        if not deck:
            return
        
        deck.pop()      

def deal(deck: Deck, num: int = 1) -> List[Optional[Card]]:
    """
    Deal a specified number of cards from the top of the deck.

    Args:
        deck (Deck): A list of tuples representing the deck of cards.
        num (int): The number of cards to deal. Default is 1.

    Returns:
        List[Optional[Card]]: A list of dealt cards. If the deck runs out of cards,
                              None is returned for remaining cards.
    """
    
    if num < 0:
        raise ValueError("Number of cards to deal must be non-negative.")
    
    out: List[Optional[Card]] = []
    for _ in range(num):
        out.append(dealOne(deck))
    
    return out

def dealPlayers(deck: Deck, players: int) -> List[List[Optional[Card]]]:
    """
    Deal two cards to each player from the deck.

    Args:
        deck (Deck): A list of tuples representing the deck of cards.
        players (int): The number of players.

    Returns:
        List[List[Optional[Card]]]: A list where each element is a list of two cards for a player.
    """
    
    if players < 0:
        raise ValueError("Number of players must be non-negative.")
    
    out: List[List[Optional[Card]]] = []
    for _ in range(2):
        for i in range(players):
            if len(out) <= i:
                out.append([])
            out[i].append(dealOne(deck))
    
    return out

def dealFlop(deck: Deck) -> List[Optional[Card]]:
    """
    Deal the flop (three community cards) from the deck.

    Args:
        deck (Deck): A list of tuples representing the deck of cards.
    
    Returns:
        List[Optional[Card]]: A list of three cards representing the flop.
    """
    
    burn(deck, 1)
    return deal(deck, 3)

def dealTurn(deck: Deck) -> Optional[Card]:
    """
    Deal the turn (fourth community card) from the deck.

    Args:
        deck (Deck): A list of tuples representing the deck of cards.
    
    Returns:
        Optional[Card]: The turn card dealt from the deck.
    """
    
    burn(deck, 1)
    cards = deal(deck, 1)
    if cards:
        return cards[0]
    
    return None

def dealRiver(deck: Deck) -> Optional[Card]:
    """
    Deal the river (fifth community card) from the deck.

    Args:
        deck (Deck): A list of tuples representing the deck of cards.
    
    Returns:
        Optional[Card]: The river card dealt from the deck.
    """
    
    burn(deck, 1)
    cards = deal(deck, 1)
    if cards:
        return cards[0]
    
    return None
