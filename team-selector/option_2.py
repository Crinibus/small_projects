import random
import argparse


def assign_names_to_teams(names, num_teams, constraints=None, pair_constraint=None):
    teams = [[] for _ in range(num_teams)]

    # Define a function for backtracking
    def backtrack(idx):
        if idx == len(names):
            return True  # All names assigned successfully

        for i in range(num_teams):
            if can_assign(names[idx], i):
                teams[i].append(names[idx])

                # Recur to assign next name
                if backtrack(idx + 1):
                    return True  # Successful assignment found

                # Backtrack if assignment failed
                teams[i].pop()

        return False  # Unable to assign names

    def can_assign(name, team_idx):
        if constraints:
            for other_name in teams[team_idx]:
                if (name, other_name) in constraints or (other_name, name) in constraints:
                    return False  # Constraint violated
        if pair_constraint and name not in teams[team_idx]:
            for other_name in teams[team_idx]:
                if (name, other_name) not in pair_constraint and (other_name, name) not in pair_constraint:
                    return False  # Pair constraint not met
        return True

    # Start backtracking
    if backtrack(0):
        return teams
    else:
        raise ValueError("Failed to generate valid teams")


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
    constraints = set(tuple(sorted(pair)) for pair in args.constraint or [])
    pair_constraint = set(tuple(sorted(args.pair_constraint))) if args.pair_constraint else None

    for i in range(100):
        teams = assign_names_to_teams(names, num_teams, constraints, pair_constraint)
        print(i, ">", len(teams[0]), len(teams[1]))
        assert len(teams[0]) == len(teams[1]) - 1 or len(teams[0]) - 1 == len(teams[1])

    # teams = assign_names_to_teams(names, num_teams, constraints, pair_constraint)
    display_teams(teams)
