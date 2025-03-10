import argparse
from fetch import get_advisors
import time


def make_parser():
    parser = argparse.ArgumentParser(description="TODO.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("name", nargs="?", help="Student name.")
    group.add_argument(
        "--file", "-f",
        help="File containing PhD names, one per line."
    )
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    if args.name:
        try:
            advisors = get_advisors(args.name)
            print(name + ":", ' and '.join(advisors))
        except KeyError as exception:
            print("Either none or 2+ names were found.")
            raise exception
    elif args.file:
        print("Note that we space out calls to MathGenealogy.")
        print("This might take a few moments.")
        print_advisors_from_file(args.file)


def print_advisors_from_file(fname):
    missing = []
    with open(fname, "r", encoding="utf8") as namefile:
        for line in namefile:
            name = line.strip()
            try:
                advisors = get_advisors(name)
                print(name + ":", ' and '.join(advisors))
            except KeyError as exception:
                missing.append(name)
                print(f"Found {name} either 0 or 2+ times. Skipping.")
            time.sleep(1)



if __name__ == "__main__":
    main()
