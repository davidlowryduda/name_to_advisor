import argparse
from .api import login, get_login, advisors_from_name
import time


def make_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve Advisors from MathGenealogy. "
            "Note this requires a MathGenealogy login and password."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("name", nargs="?", help="Student name.")
    group.add_argument(
        "--file", "-f",
        help="File containing PhD names, one per line."
    )
    return parser


def authenticate():
    authdata = get_login()
    token = login(authdata)
    return token


def main():
    parser = make_parser()
    args = parser.parse_args()
    token = authenticate()
    if args.name:
        try:
            advisors = advisors_from_name(args.name, token)
            print(args.name + ":", ' and '.join(advisors))
        except KeyError as exception:
            print("Either none or 2+ names were found.")
            raise exception
    elif args.file:
        print("Note that we space out calls to MathGenealogy.")
        print("This might take a few moments.")
        print()
        print_advisors_from_file(args.file, token)


def print_advisors_from_file(fname, token):
    missing = []
    with open(fname, "r", encoding="utf8") as namefile:
        for line in namefile:
            name = line.strip()
            try:
                advisors = advisors_from_name(name, token)
                if advisors:
                    print(name + ":", ' and '.join(advisors))
                else:
                    missing.append(name)
            except KeyError:
                missing.append(name)
                #print(f"Found {name} either 0 or 2+ times. Skipping.")
            time.sleep(1)
    print("\nThese are the names that were skipped:")
    print('\n'.join(missing))


if __name__ == "__main__":
    main()
