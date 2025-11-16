from typing import List, Tuple, Optional
from itertools import combinations
from collections import Counter
from cards import RANKS


Card = Tuple[str, str]
Score = Tuple[int, Tuple[int, ...]]
RANK_VALUE = {rank: index + 2 for index, rank in enumerate(RANKS)}
VALUE_RANK = {v: r for r, v in RANK_VALUE.items()}


def cardValue(card: Card) -> int:
    """
    Get the numerical value of a card based on its rank.

    Args:
        card (Card): A tuple representing the card (rank, suit).

    Returns:
        int: The numerical value of the card.
    """
    
    if not isinstance(card, tuple) or len(card) != 2:
        raise ValueError(f"Invalid card: {card}")
    
    rank = card[0]
    if rank not in RANK_VALUE:
        raise ValueError(f"Invalid rank: {rank}")
    
    return RANK_VALUE[rank]

def values(cards: List[Card]) -> List[int]:
    """
    Get a list of numerical values for a list of cards.

    Args:
        cards (List[Card]): A list of tuples representing the cards.
    
    Returns:
        List[int]: A list of numerical values of the cards.
    """
    
    val: List[int] = []
    for card in cards:
        val.append(cardValue(card))
    
    return val

def checkConsecutive(vals: List[int]) -> Optional[int]:
    """
    Check if a list of integer values are consecutive.

    Args:
        vals (List[int]): A list of integer values.
    
    Returns:
        Optional[int]: The highest value in the consecutive sequence if found, None otherwise.
    """
    
    if len(vals) < 5:
        return None
    
    s = set(vals)
    if 14 in s:
        s = s.union({1})
    else:
        s = s 
    
    sorted_vals = sorted(s, reverse=True)
    for i in range(len(sorted_vals)):
        high = sorted_vals[i]
        consec = [high - offset for offset in range(5)]
        if all(v in s for v in consec):
            return high if high != 1 else 5
    
    return None

def straightFlush(cards: List[Card]) -> Optional[int]:
    """
    Check for a straight flush in a list of cards.
    
    Args:
        cards (List[Card]): A list of tuples representing the cards.

    Returns:
        Optional[int]: The highest value of a straight flush if found, None otherwise.
    """
    
    suits = {}
    for card in cards:
        if card is None:
            continue
        
        val = cardValue(card)
        suit = card[1]
        suits.setdefault(suit, []).append(val)
    
    best: Optional[int] = None
    for vals in suits.values():
        high = checkConsecutive(sorted(set(vals), reverse=True))
        if high is not None:
            if best is None or high > best:
                best = high
    
    return best

def scoreFive(cards: List[Card]) -> Score:
    """
    Evaluate the best poker hand from a list of five cards.

    Args:
        cards (List[Card]): A list of tuples representing the cards.
    
    Returns:
        Score: A tuple representing the score of the hand.
    """ 
    
    vals = [cardValue(card) for card in cards]
    suits = [card[1] for card in cards]
    cnt = Counter(vals)
    is_flush = len(set(suits)) == 1
    is_straight = checkConsecutive(sorted(set(vals), reverse=True))
    
    if is_flush and is_straight is not None:
        return (8, (is_straight,))
    
    four = [val for val, count in cnt.items() if count == 4]
    if four:
        fk = four[0]
        kicker = max(v for v in vals if v != fk)
        return (7, (fk, kicker))

    three = [val for val, count in cnt.items() if count == 3]
    pairs = sorted([val for val, count in cnt.items() if count == 2], reverse=True)
    if three and pairs:
        tk = max(three)
        pk = pairs[0]
        return (6, (tk, pk))
    
    if is_flush:
        return (5, tuple(sorted(vals, reverse=True)))
    
    if is_straight is not None:
        return (4, (is_straight,))
    
    if three:
        tk = max(three)
        kicker = tuple(sorted((v for v in vals if v != tk), reverse=True))
        return (3, (tk,) + kicker)
    
    if len(pairs) >= 2:
        hp, lp = pairs[0], pairs[1]
        kicker = max(v for v in vals if v != hp and v != lp)
        return (2, (hp, lp, kicker))
    
    if len(pairs) == 1:
        pair = pairs[0]
        kicker = tuple(sorted((v for v in vals if v != pair), reverse=True))
        return (1, (pair,) + kicker)
    
    return (0, tuple(sorted(vals, reverse=True)))

def compareScores(score1: Score, score2: Score) -> int:
    """
    Compare two poker hand scores.

    Args:
        score1 (Score): The first hand score.
        score2 (Score): The second hand score.
    
    Returns:
        int: 1 if score1 is better, -1 if score2 is better, 0 if equal.
    """ 
    
    if score1[0] != score2[0]:
        return 1 if score1[0] > score2[0] else -1
    if score1[1] > score2[1]:
        return 1
    if score1[1] < score2[1]:
        return -1
    
    return 0

def bestHand(cards: List[Optional[Card]]) -> Score:
    """
    Evaluate the best poker hand from a list of cards (5 to 7 cards).

    Args:
        cards (List[Optional[Card]]): A list of tuples representing the cards.
    
    Returns:
        Score: A tuple representing the score of the best hand.
    """ 
    
    filtered = [card for card in cards if card is not None]
    n = len(filtered)
    if n < 5 or n > 7:
        raise ValueError("Number of cards must be between 5 and 7.")
    
    if n == 5:
        return scoreFive(filtered)
    
    best: Optional[Score] = None
    for combo in combinations(filtered, 5):
        s = scoreFive(list(combo))
        if best is None or compareScores(s, best) == 1:
            best = s
    
    assert best is not None
    return best

def compareHands(cards1: List[Optional[Card]], cards2: List[Optional[Card]]) -> int:
    """
    Compare two poker hands and determine which is better.

    Args:
        cards1 (List[Optional[Card]]): The first hand's cards.
        cards2 (List[Optional[Card]]): The second hand's cards.
    
    Returns:
        int: 1 if the first hand is better, -1 if the second hand is better, 0 if equal.
    """ 
    
    score1 = bestHand(cards1)
    score2 = bestHand(cards2)
    
    return compareScores(score1, score2)

def scoreToStr(score: Score) -> str:
    """
    Convert a poker hand score to a human-readable string.

    Args:
        score (Score): A tuple representing the score of the hand.
    
    Returns:
        str: A string representation of the poker hand.
    """ 
    
    rank_names = {
        8: "Straight Flush",
        7: "Four of a Kind",
        6: "Full House",
        5: "Flush",
        4: "Straight",
        3: "Three of a Kind",
        2: "Two Pair",
        1: "One Pair",
        0: "High Card"
    }
    rank_name = rank_names.get(score[0], f"Category {score[0]}")
    
    return f"{rank_name} {score[1]}"
