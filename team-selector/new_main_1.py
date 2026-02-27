import random
import argparse


def shuffle_names(names):
    random.shuffle(names)


def assign_names_to_teams(names, num_teams, constraints=None, pair_constraint=None):
    teams = [[] for _ in range(num_teams)]
    team_sizes = [0] * num_teams

    # Sort names based on their lengths
    sorted_names = sorted(names, key=len, reverse=True)

    for name in sorted_names:
        valid_teams = get_valid_teams(name, teams, num_teams, constraints)
        if not valid_teams:
            raise ValueError(f"No valid teams for {name}")

        # Choose the team with the smallest size among the valid teams
        min_size = min(team_sizes[team] for team in valid_teams)
        min_teams = [team for team in valid_teams if team_sizes[team] == min_size]

        # If constraints are defined, filter out teams violating constraints
        valid_min_teams = [
            team
            for team in min_teams
            if all(
                (name, other_name) not in constraints and (other_name, name) not in constraints for other_name in teams[team]
            )
        ]

        if not valid_min_teams:
            # If no valid team due to constraints, distribute the name randomly among all teams
            team_index = random.randint(0, num_teams - 1)
        else:
            team_index = random.choice(valid_min_teams)

        teams[team_index].append(name)
        team_sizes[team_index] += 1

    if pair_constraint:
        for team in teams:
            if pair_constraint[0] in team and pair_constraint[1] in team:
                return teams

        # If the pair is not in the same team, try to swap one of the pair to another team
        for i, team in enumerate(teams):
            if pair_constraint[0] in team:
                teams[i].remove(pair_constraint[0])
                teams[random.randint(0, num_teams - 1)].append(pair_constraint[0])
                break

    return teams


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

    shuffle_names(names)

    retries = []

    for i in range(100):
        current_retries = 0
        teams = assign_names_to_teams(names, num_teams, constraints, pair_constraint)

        while (len(teams[0]) != len(teams[1]) - 1) and (len(teams[0]) - 1 != len(teams[1])):
            teams = assign_names_to_teams(names, num_teams, constraints, pair_constraint)
            print(i, ">", len(teams[0]), len(teams[1]), "::", current_retries)
            current_retries += 1

        retries.append(current_retries)
        print(i, ">", len(teams[0]), len(teams[1]))
        assert len(teams[0]) == len(teams[1]) - 1 or len(teams[0]) - 1 == len(teams[1])
    print(retries)
    print("Final:")
    display_teams(teams)
