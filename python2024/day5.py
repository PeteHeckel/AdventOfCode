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

def fix_order( rules: dict, order: list[int]) -> list[int]:
    new_order = []
    
    while order:
        test_page = order.pop()
        if test_page in rules.keys():
            priors = rules[test_page]

            if set(priors) & set(order):
                # find where to insert it so that the ordering is valid for the test page
                for i in range(len(order), -1, -1):
                    if not set(priors) & set(order[:i] ):
                        order.insert( i, test_page )
                        break
            else:
                new_order.insert(0, test_page)
        else:
            new_order.insert(0, test_page)
    
    return new_order

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

    valid_middle_sum = 0
    fixed_middle_sum = 0

    for order in orders:
        if check_order( rules, order ):
            valid_middle_sum += order[int(len(order)/2)]
        else:
            new_order = fix_order( rules, order )
            fixed_middle_sum += new_order[int(len(new_order)/2)]

    print(f'valid middle page sum = {valid_middle_sum}' )
    print(f'valid fixed page sum = {fixed_middle_sum}' )