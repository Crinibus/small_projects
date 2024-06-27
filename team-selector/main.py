import argparse
import random


class NoValidTeam(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Team selector")
    parser.add_argument("--names", "-n", type=str, nargs="+", dest="names", help="Names to put into teams")
    parser.add_argument("--team-count", "-tc", type=int, default=2, dest="team_count", help="Number of teams")
    parser.add_argument(
        "--dont",
        "-d",
        type=str,
        nargs=2,
        dest="dont_constraints",
        action="append",
        default=[],
        help="Two names that cannot be in the same team",
    )
    parser.add_argument("--test", action="store_true", dest="test")
    return parser.parse_args()


def process_dont_constraints(dont_constraints: list[list[str, str]]) -> dict[str, list[str]]:
    processed_constraints: dict[str, list[str]] = dict()
    for dont_constraint in dont_constraints:
        firstName, secondName = dont_constraint

        if firstName not in processed_constraints.keys():
            processed_constraints[firstName] = []
        if secondName not in processed_constraints.keys():
            processed_constraints[secondName] = []

        if firstName not in processed_constraints[secondName]:
            processed_constraints[secondName].append(firstName)
        if secondName not in processed_constraints[firstName]:
            processed_constraints[firstName].append(secondName)

    return processed_constraints


def get_team_sizes(member_count: int, team_count: int) -> tuple[int]:
    if team_count > member_count:
        raise Exception("Team count is greater than member count")

    remainder = member_count % team_count
    base_member_count = member_count // team_count

    teams_with_base_member_count = [base_member_count for _ in range(team_count - remainder)]
    teams_with_extra_member_count = [base_member_count + 1 for _ in range(remainder)]

    return tuple(teams_with_base_member_count + teams_with_extra_member_count)


def find_valid_team_indexes(
    name: str, teams: list[list[str]], spaces_left_in_teams: list[int], name_constraints: list[str]
) -> list[int]:
    valid_team_indexes: list[int] = []

    for index, team in enumerate(teams):
        if spaces_left_in_teams[index] == 0:
            continue

        is_valid_team = all(name not in name_constraints for name in team)

        if is_valid_team:
            valid_team_indexes.append(index)

    if len(valid_team_indexes) == 0:
        raise NoValidTeam(f"No valid team for name in dont constaints - {name=}")

    return valid_team_indexes


def put_names_into_teams(
    names: list[str], team_sizes: tuple[int], processed_dont_constraints: dict[str, list[str]]
) -> tuple[str]:
    names = names.copy()
    spaces_left_in_teams = list(team_sizes)

    teams = [[] for _ in range(len(team_sizes))]

    for constraint_name, name_constraints in processed_dont_constraints.items():
        valid_team_indexes = find_valid_team_indexes(constraint_name, teams, spaces_left_in_teams, name_constraints)
        random_team_index = random.choice(valid_team_indexes)
        teams[random_team_index].append(constraint_name)
        spaces_left_in_teams[random_team_index] -= 1
        names.remove(constraint_name)

    for name in names:
        indexes_of_teams_with_spaces_left = [
            index for index, spaces_left in enumerate(spaces_left_in_teams) if spaces_left > 0
        ]

        team_index = random.choice(indexes_of_teams_with_spaces_left)
        team = teams[team_index]

        team.append(name)
        spaces_left_in_teams[team_index] -= 1

    return teams


def valid_insert_name_in_team(name: str, team: list[str], dont_constraints: list[list[str]]) -> bool:
    for dont_constraint in dont_constraints:
        if name not in dont_constraint:
            continue

        name1, name2 = dont_constraint
        other_name = name1 if name == name2 else name2

        if other_name in team:
            return False
    return True


def is_team_valid(team: list[str], dont_constraints: list[list[str]]) -> bool:
    for dont_constraint in dont_constraints:
        name, other_name = dont_constraint

        if name in team and other_name in team:
            return False
    return True


def main():
    args = parse_arguments()

    names: list[str] = args.names
    team_count: int = args.team_count
    dont_constraints: list[list[str, str]] = args.dont_constraints

    if args.test:
        # test(40)
        test_v2(names, team_count, dont_constraints)
        return

    if not args.names:
        print("Please enter some names and team count and optionally constraints")
        return

    member_count: int = len(names)

    processed_dont_constraints = process_dont_constraints(dont_constraints)

    team_sizes = get_team_sizes(member_count, team_count)
    teams = put_names_into_teams(names, team_sizes, processed_dont_constraints)

    is_valid_teams = all([is_team_valid(team, dont_constraints) for team in teams])

    print("dont_constraints:", dont_constraints)
    print("Team sizes:", team_sizes)
    print("Teams:", teams)
    print("Valid teams:", is_valid_teams)


def test(max_member_count: int) -> None:
    for member_count in range(2, max_member_count + 1):
        for team_count in range(2, member_count + 1):
            team_sizes = get_team_sizes(member_count, team_count)

            print(member_count, team_count, team_sizes)
            # print(" -", actual_member_count, actual_team_count)
            assert len(team_sizes) == team_count, f"NOT MATCH TEAM - Expected {team_count}, got {len(team_sizes)}"
            # assert len(teams) == team_count, f"NOT MATCH TEAM - Expected {team_count}, got {len(teams)}"
            assert sum(team_sizes) == member_count, f"NOT MATCH MEMBER COUNT - Expected {member_count}, got {sum(team_sizes)}"
    print("PASS")


def test_v2(
    names: list[str] | None = None, team_count: int | None = None, dont_constraints: list[list[str, str]] | None = None
) -> None:
    names = names if names else ["one", "two", "three", "four", "five"]
    team_count = team_count if team_count else 2
    dont_constraints = dont_constraints if dont_constraints else [["one", "two"], ["one", "three"]]

    valid_constraints = validate_constraints(names, dont_constraints)

    for try_index in range(1000):
        processed_dont_constraints = process_dont_constraints(dont_constraints)

        member_count: int = len(names)

        team_sizes = get_team_sizes(member_count, team_count)
        try:
            teams = put_names_into_teams(names, team_sizes, processed_dont_constraints)
        except NoValidTeam as ex:
            print(f"Failed at try {try_index} - {ex}")
            return

        print(teams)

        for team in teams:
            assert is_team_valid(team, dont_constraints), f"Failed at try {try_index} - Team is not valid: {team}"


def test_constraints():
    names: list[str] = ["one", "two", "three", "four", "five"]
    team_count: int = 3
    team_sizes = get_team_sizes(len(names), team_count)
    dont_constraints = [["one", "two"], ["one", "three"], ["one", "four"]]

    print("Names:", names)
    print("Team sizes:", team_sizes)
    print("dont_constraints:", dont_constraints)
    print("Team count:", team_count)
    print()

    is_possible = is_constraints_possible(names, team_count, dont_constraints)
    print("Is constraints possible:", is_possible)


def is_constraints_possible(names, num_teams, constraints):
    name_constraint_count = {name: 0 for name in names}

    # Count the number of constraints involving each name
    for constraint in constraints:
        for name in constraint:
            name_constraint_count[name] += 1

    # Check if any name has a constraint with every other name
    for name, count in name_constraint_count.items():
        if count == len(names) - 1:
            if num_teams < len(names):
                return False

    # Check if the number of teams is less than the total number of unique names
    if num_teams < len(set(name for constraint in constraints for name in constraint)):
        return False

    return True


if __name__ == "__main__":
    main()
    # test_constraints()
