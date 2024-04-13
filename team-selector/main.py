import argparse
import random


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
    return parser.parse_args()


def get_team_sizes(member_count: int, team_count: int) -> tuple[int]:
    if team_count > member_count:
        raise Exception("Team count is greater than member count")

    remainder = member_count % team_count
    base_member_count = member_count // team_count

    teams_with_base_member_count = [base_member_count for _ in range(team_count - remainder)]
    teams_with_extra_member_count = [base_member_count + 1 for _ in range(remainder)]

    return tuple(teams_with_base_member_count + teams_with_extra_member_count)


def put_names_into_teams(names: list[str], team_sizes: tuple[int], dont_constraints: list[list[str]]) -> tuple[str]:
    spaces_left_in_teams = list(team_sizes)

    teams = [[] for _ in range(len(team_sizes))]

    for name in names:
        indexes_of_teams_with_spaces_left = [
            index for index, spaces_left in enumerate(spaces_left_in_teams) if spaces_left > 0
        ]

        team_index = random.choice(indexes_of_teams_with_spaces_left)
        team = teams[team_index]

        tries = 0
        while valid_insert_name_in_team(name, team, dont_constraints) is False and tries < 5:
            team_index = random.choice(indexes_of_teams_with_spaces_left)
            team = teams[team_index]
            tries += 1

        # print(valid_insert_name_in_team(name, team, dont_constraints), "---", tries)

        team.append(name)
        spaces_left_in_teams[team_index] -= 1

    # Recursive if any of the teams are invalid
    if any([is_team_valid(team, dont_constraints) is False for team in teams]):
        return put_names_into_teams(names, team_sizes, dont_constraints)

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

    member_count: int = len(names)

    team_sizes = get_team_sizes(member_count, team_count)
    teams = put_names_into_teams(names, team_sizes, dont_constraints)

    is_valid_teams = all([is_team_valid(team, dont_constraints) for team in teams])

    print("dont_constraints:", dont_constraints)
    print("Team sizes:", team_sizes)
    print("Teams:", teams)
    print("Valid teams:", is_valid_teams)


def test(max_member_count: int) -> None:
    for member_count in range(2, max_member_count + 1):
        for team_count in range(2, member_count + 1):
            team_sizes = get_team_sizes(member_count, team_count)

            # names = ["a" for _ in range(member_count)]
            # teams = put_names_into_teams(names, team_sizes)

            # actual_team_count = len(team_sizes)
            # actual_member_count = sum(team_sizes)

            print(member_count, team_count, team_sizes)
            # print(" -", actual_member_count, actual_team_count)
            assert len(team_sizes) == team_count, f"NOT MATCH TEAM - Expected {team_count}, got {len(team_sizes)}"
            # assert len(teams) == team_count, f"NOT MATCH TEAM - Expected {team_count}, got {len(teams)}"
            assert sum(team_sizes) == member_count, f"NOT MATCH MEMBER COUNT - Expected {member_count}, got {sum(team_sizes)}"
    print("PASS")


def test_v2() -> None:
    names: list[str] = ["niko", "luka", "mads", "isab"]
    team_count: int = 2
    dont_constraints = [["luka", "isab"]]

    for try_index in range(1000):
        member_count: int = len(names)

        team_sizes = get_team_sizes(member_count, team_count)
        teams = put_names_into_teams(names, team_sizes, dont_constraints)
        print(teams)

        for team in teams:
            assert is_team_valid(team, dont_constraints), f"Failed at try {try_index}"


if __name__ == "__main__":
    main()
    # test(40)
    # test_v2()
