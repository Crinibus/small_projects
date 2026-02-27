import random
import argparse


def shuffle_names(names):
    random.shuffle(names)


def assign_names_to_teams(names, num_teams, constraints=None, pair_constraint=None):
    for _ in range(1000):  # Attempt to generate teams up to 1000 times
        teams = [[] for _ in range(num_teams)]
        shuffle_names(names)  # Shuffle names to randomize assignment
        try:
            assign_names_recursive(names, teams, constraints, pair_constraint)
            return teams
        except ValueError:
            continue
    raise ValueError("Failed to generate valid teams")


def assign_names_recursive(names, teams, constraints, pair_constraint, index=0):
    if index == len(names):
        return True

    name = names[index]
    valid_teams = get_valid_teams(name, teams, len(teams), constraints)
    random.shuffle(valid_teams)  # Randomize the order of valid teams

    for team_index in valid_teams:
        teams[team_index].append(name)
        if pair_constraint and pair_constraint[0] in teams[team_index] and pair_constraint[1] not in teams[team_index]:
            teams[team_index].remove(name)  # Rollback the addition if pair constraint is not satisfied
            continue
        if assign_names_recursive(names, teams, constraints, pair_constraint, index + 1):
            return True
        teams[team_index].remove(name)  # Rollback the addition

    return False


def get_valid_teams(name, teams, num_teams, constraints=None):
    if constraints is None:
        return [i for i in range(num_teams)]
    return [
        i
        for i in range(num_teams)
        if all((name, other_name) not in constraints and (other_name, name) not in constraints for other_name in teams[i])
    ]


def display_teams(teams):
    for i, team in enumerate(teams):
        print(f"Team {i+1}: {team}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Assign names to teams with constraints")
    parser.add_argument("--names", metavar="N", type=str, nargs="+", help="List of names to be assigned to teams")
    parser.add_argument("--num-teams", type=int, default=3, help="Number of teams")
    parser.add_argument(
        "--constraint", nargs=2, metavar=("name1", "name2"), action="append", help="Two names that cannot be in the same team"
    )
    parser.add_argument(
        "--pair-constraint", nargs=2, metavar=("name1", "name2"), help="Two names that need to be in the same team"
    )
    return parser.parse_args()


# Main script
if __name__ == "__main__":
    args = parse_arguments()
    names = args.names
    num_teams = args.num_teams
    constraints = args.constraint or []
    pair_constraint = args.pair_constraint

    for i in range(100):
        teams = assign_names_to_teams(names, num_teams, constraints, pair_constraint)
        print(i, ">", len(teams[0]), len(teams[1]))
        assert len(teams[0]) == len(teams[1]) - 1 or len(teams[0]) - 1 == len(teams[1])

    # teams = assign_names_to_teams(names, num_teams, constraints, pair_constraint)
    display_teams(teams)
