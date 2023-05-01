import sys
import pprint

from pangeo_forge_cordex import parse_instance_ids


if __name__ == "__main__":
    ids = sys.argv[1]
    found = parse_instance_ids(ids)
    pprint.pprint(found)

