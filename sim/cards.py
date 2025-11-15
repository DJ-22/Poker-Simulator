from typing import List, Tuple


RANKS: List[str] = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS: List[str] = ['S', 'H', 'C', 'D']
Card = Tuple[str, str]  


def makeCard(rank: str, suit: str) -> Card:
    """
    Create a card representation from rank and suit.

    Args:
        rank (str): The rank of the card (e.g., '2', 'T', 'A').
        suit (str): The suit of the card (e.g., 'S', 'H', 'C', 'D').

    Returns:
        Card: A tuple representing the card (rank, suit).
    """
    
    rank = str(rank).upper()
    suit = str(suit).upper()
    if rank not in RANKS:
        raise ValueError(f"Invalid rank: {rank}. Must be one of {RANKS}.")
    if suit not in SUITS:
        raise ValueError(f"Invalid suit: {suit}. Must be one of {SUITS}.")
    
    return (rank, suit)

def cardToStr(card: Card) -> str:
    """
    Convert a card tuple to its string representation.

    Args:
        card (Card): A tuple representing the card (rank, suit).

    Returns:
        str: A two-character string representing the card.
    """
    
    return f"{card[0]}{card[1]}"

def strToCard(card: str) -> Card:
    """
    Convert a string representation of a card to a tuple.

    Args:
        card (str): A two-character string representing the card.

    Returns:
        Card: A tuple representing the card (rank, suit).
    """
    
    if not isinstance(card, str):
        raise ValueError(f"Invalid card: {card}")
    
    card = card.strip().upper()
    if len(card) != 2:
        raise ValueError(f"Invalid card {card}")
    
    return makeCard(card[0], card[1])
