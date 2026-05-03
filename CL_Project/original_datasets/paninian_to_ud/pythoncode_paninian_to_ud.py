
deepti_to_ud = {
    "k1":"nsubj",
    "k2":"dobj",
    "k3":"nmod",
    "k4":"iobj",
    "k5":"nmod",
    "k7":"nmod",
    "rt":"advmod",
    "rh":"advmod",
    "ras":"nmod",
    "k*u":"vocative",
    "k*s":"xcomp",
    "r6":"nmod",
    "relc": "acl",
    "rs":"nmod",
    "adv":"advmod",
    "adj":"amod",
}

ignore={"V", "PUNC", "-"}


def paninian_to_ud(tag):
    return deepti_to_ud.get((tag or "").strip())


def convert_tag(tag):
    tag = (tag or "").strip()
    if tag in ignore:
        return tag
    return paninian_to_ud(tag)


def parse_and_convert_file(input_path, output_path):
  
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    out_lines = []
    stats = {"converted": 0, "passthrough": 0, "unknown": 0}

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        if line.strip() == "":
            out_lines.append("")
            continue

        if line.strip().startswith("#"):
            out_lines.append(line)
            continue

        parts = line.split()
        if len(parts) < 3:
            out_lines.append(line)
            continue

        idx, word, p_tag = parts[0], parts[1], parts[2]
        ud_tag = convert_tag(p_tag)

        if p_tag in ignore:
            stats["passthrough"] += 1
        else:
            stats["converted"] += 1

        out_lines.append(f"{idx}\t{word}\t{ud_tag}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
        if out_lines and out_lines[-1] != "":
            f.write("\n")

    print("Done!")
    print(f"Tags converted: {stats['converted']}")
    print(f"Passed through: {stats['passthrough']}  (V / PUNC / -)")
    print(f"Output written: {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        print(f"Converting '{sys.argv[1]}' -> '{sys.argv[2]}' ...")
        parse_and_convert_file(sys.argv[1], sys.argv[2])
        sys.exit(0)

    print("Tag mapping:")
    for tag, ud in deepti_to_ud.items():
        print(f"  {tag:<6} -> {ud}")
    print()
    print("Usage:  python paninian_to_ud.py  input.txt  output.txt")