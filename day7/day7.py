import sys
from pathlib import PosixPath

CARD_TYPES = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
CARD_VALS = dict(zip(CARD_TYPES, range(len(CARD_TYPES))))

J_CARD_TYPES = ['J','2','3','4','5','6','7','8','9','T','Q','K','A']
J_CARD_VALS = dict(zip(J_CARD_TYPES, range(len(CARD_TYPES))))

class CamelHand( object ):
    def __init__( self, hand_bid:str, include_joker:bool ):
        # Each line contains a hand and the bid; space separated
        hand, bid = hand_bid.split()

        self.joker = include_joker
        if include_joker:
            self.joker_count = hand.count('J')
        else:
            self.joker_count = 0

        self.bid = int(bid.strip())
        self.cards = list(hand)
        self.card_counts = {}
        for card in self.cards:
            if self.card_counts.get(card) is None:
                self.card_counts[card] = 1
            else:
                self.card_counts[card] += 1
        if self.joker_count > 0:
            self.value = self.joker_hand_value()
        else:
            self.value = self.hand_value()

    def __lt__(self,other):
        comp_value = other.value
        if self.value == comp_value:
            return (self.second_sorting_lt(other))
        
        return self.value < comp_value

    def __repr__(self) -> str:
        return(f'Cards: {self.cards} - Value: {self.value}')

    def joker_hand_value( self ):
        dict_copy = self.card_counts.copy()
        dict_copy.pop('J')
        sorted_card_counts = list(dict_copy.values())
        sorted_card_counts.sort( reverse=True)
        if len(sorted_card_counts) == 1 or self.joker_count == 5:
            return 6    # 5 of a kind

        if sorted_card_counts[0] == 3: # Single joker in a 3 card count turns it to a 4 of a kind
            return 5
        
        if sorted_card_counts[0] == 2:
            if sorted_card_counts[1] == 2:
                return 4    # 2 pair turns to full house
            else:   # 1 joker and 1 pair -> 3 of kind, 2 jokers and 1 pair -> 4 of kind
                return 2*self.joker_count + 1
        
        # Hi card, all points come from jokers
        if self.joker_count == 3:
            return 5
        elif self.joker_count == 2:
            return 3
        else:
            return 1

    def hand_value(self):
        if(len(self.card_counts) == 1):
            return 6 # 5 of a kind

        sorted_card_counts = list(self.card_counts.values())
        sorted_card_counts.sort( reverse=True)
        if(len(self.card_counts) == 2):
            # 4 of a kind or full house
            if sorted_card_counts[0] == 4:
                return 5
            else:
                return 4
        if( sorted_card_counts[0] == 3):    # 3 of a kind
            return 3
        else:
            return len(self.cards) - len(self.card_counts)  # Return 2,1,0 for two pair, one pair, high card respectively.

    def second_sorting_lt( self, comparison:'CamelHand' ):
        # Returns true if self beats the comparison in the secondary check metric
        if self.joker:
            value_dict = J_CARD_VALS
        else:
            value_dict = CARD_VALS
        if comparison.joker:
            compare_dict = J_CARD_VALS
        else:
            compare_dict = CARD_VALS

        for i in range(len(self.cards)):
            if self.cards[i] != comparison.cards[i]:
                return value_dict[self.cards[i]] < compare_dict[comparison.cards[i]]

        # hands are the same
        return True


def play_camel_camel( hand_list_filepath: str ):
    with open(hand_list_filepath) as f:
        hands = []
        joker_hands = []
        for line in f:
            # Each line contains a hand and the bid; space separated
            hands.append(CamelHand(line, False))
            joker_hands.append(CamelHand(line, True))
    hands.sort()
    joker_hands.sort()
    
    total_winnings = 0
    for rank, hand in enumerate(hands, start=1):
        total_winnings += rank * hand.bid
    
    joker_winnings = 0
    for rank, hand in enumerate(joker_hands, start=1):
        joker_winnings += rank * hand.bid

    print(f'I have {total_winnings} points')
    print(f'I have {joker_winnings} points with jokers')

    return total_winnings            

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    winnings = play_camel_camel(sys.argv[1])

    exit(0)
