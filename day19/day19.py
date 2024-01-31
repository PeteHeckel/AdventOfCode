from pathlib import PosixPath
import sys

def make_workflows( input_file: str ):
    parts = []
    workflows = {}

    with open(input_file,'r') as f:
        workflow_parsing = True
        for line in f.readlines():
            if len(line.strip()) == 0:
                workflow_parsing = False
            elif workflow_parsing:
                name, rules = line.strip().split('{')
                rules = rules[0:-1]     # strip trailing '}'
                all_rules = rules.split(',')
                workflows[name] = all_rules
            else:
                part_ratings = line.strip()[1:-1].split(',')
                rating_dict = {}
                for rating in part_ratings:
                    part_key, value = rating.split('=')
                    rating_dict[part_key] = int(value)
                parts.append(rating_dict)

    return workflows, parts

def check_accepted( workflow_key: str, all_workflows:dict, part_ratings:dict ) -> bool:
    # list is an ordered if elif else chain 
    workflow = all_workflows[workflow_key]
    last_line = False

    for i, rule in enumerate(workflow):
        if i == (len(workflow)-1):
            last_line = True
            result = rule
        else:
            conditional, result = rule.split(':')
            part_key = conditional[0]
            op = conditional[1]
            comp_val = int(conditional[2:])

        if (last_line or 
           (op == '>' and part_ratings[part_key] > comp_val) or
           (op == '<' and part_ratings[part_key] < comp_val)):
            if len(result) == 1:
                return (result == 'A')
            else:
                return check_accepted( result, all_workflows, part_ratings )

def get_ratings( workflows:dict, part_ratings:dict ):
    rating = 0
    if check_accepted('in', workflows, part_ratings ):
        for part_val in part_ratings.values():
            rating += part_val

    return rating

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)
    
    print('Part1:')
    workflows, parts = make_workflows(sys.argv[1])
    
    accepted_part_ratings = 0
    for rating_dict in parts:
        accepted_part_ratings += get_ratings(workflows, rating_dict)

    print(f'Accepted Sum: {accepted_part_ratings}')

    print('Part2:')
    

    exit(0)