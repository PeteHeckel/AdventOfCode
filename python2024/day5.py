import sys



test_array = "47|53\n\
97|13\n\
97|61\n\
97|47\n\
75|29\n\
61|13\n\
75|53\n\
29|13\n\
97|29\n\
53|29\n\
61|53\n\
97|53\n\
61|29\n\
47|13\n\
75|47\n\
97|75\n\
47|61\n\
75|61\n\
47|29\n\
75|13\n\
53|13\n\
\n\
75,47,61,53,29\n\
97,61,53,29,13\n\
75,29,13\n\
75,97,47,61,53\n\
61,13,29\n\
97,13,75,29,47"

def check_order( rules: dict, order: list[int] ) -> bool:
    for i,pagenum in enumerate(order):
        if pagenum in rules.keys():
            priors = rules[pagenum]
            prevpages = order[:i]
            
            rulebreaks = set(priors) & set(prevpages)
            if len(rulebreaks) != 0:
                return False
    return True

def check_valid( rules: dict, orders: list[list[int]] ) -> int:
    middle_number_sum = 0

    for order in orders:
        if check_order( rules, order ):
            middle_number_sum += order[int(len(order)/2)]

    return middle_number_sum


def parse_input( input: str ) -> tuple[dict, list[list[int]]]:
    
    rules = {}
    orders = []
    for line in input.splitlines():
        if "|" in line:
            [n,m] = line.strip().split("|")
            n = int(n)
            m = int(m)
            if n in rules.keys():
                rules[n].append(m)
            else:
                rules[n] = [m]
        
        elif line.strip() != "":
            orders.append( [int(n) for n in line.strip().split(",")])
    return rules,orders

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        input = test_array
    else:
        input = open("inputs/day5.txt").read()
    
    rules, orders = parse_input(input)

    print(f'valid middle page sum = {check_valid( rules, orders )}' )