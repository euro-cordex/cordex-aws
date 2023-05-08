import sys

from pangeo_forge_cordex import parse_instance_ids, total_size_ids


def write_comment_body(iids, total_size):
    output = "\n"
    output += f"Found {len(iids)} Dataset(s):\n"
    output += f"Total size: {total_size/1.e6} MB\n"
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
    total_size = total_size_ids(ids)
    print(iids)
    write_comment_body(iids, total_size)
