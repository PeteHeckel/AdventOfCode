import sys
from pathlib import PosixPath

CARD_TYPES = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
CARD_VALS = dict(zip(CARD_TYPES, range(len(CARD_TYPES))))

class CamelHand( object ):
    def __init__( self, hand_bid:str ):
        # Each line contains a hand and the bid; space separated
        hand, bid = hand_bid.split()
        self.bid = int(bid.strip())
        self.cards = list(hand)
        self.card_counts = {}
        for card in self.cards:
            if self.card_counts.get(card) is None:
                self.card_counts[card] = 1
            else:
                self.card_counts[card] += 1

    def __lt__(self,other):
        my_value = self.hand_value()
        comp_value = other.hand_value()
        if my_value == comp_value:
            return (self.second_sorting_lt(other))
        
        return my_value < comp_value

    def __repr__(self) -> str:
        return(f'Cards: {self.cards} - Value: {self.hand_value()}')

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
        for i in range(len(self.cards)):
            if self.cards[i] != comparison.cards[i]:
                return CARD_VALS[self.cards[i]] < CARD_VALS[comparison.cards[i]]

        # hands are the same
        return True


def play_camel_camel( hand_list_filepath: str ):
    with open(hand_list_filepath) as f:
        hands = []
        for line in f:
            # Each line contains a hand and the bid; space separated
            hands.append(CamelHand(line))
    hands.sort()

    total_winnings = 0
    for rank, hand in enumerate(hands, start=1):
        total_winnings += rank * hand.bid

    return total_winnings            

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    winnings = play_camel_camel(sys.argv[1])
    print(f'I have {winnings} points')

    exit(0)
