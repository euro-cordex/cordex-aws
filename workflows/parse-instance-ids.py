import pprint
import sys

from pangeo_forge_cordex import parse_instance_ids


def write_comment_body(iids):
    output = "\n"
    output += f"Found {len(iids)} Dataset(s):\n"
    output += "```\n"
    for iid in iids:
        output += f"{iid}\n"
    output += "```"

    with open("body.md", "w") as f:
        f.write(output)

    return


if __name__ == "__main__":
    ids = sys.argv[1].replace("`", "")
    iids = parse_instance_ids(ids)
    pprint.pprint(iids)
    write_comment_body(iids)
