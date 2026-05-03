import re

def parse_conll(path):
    sentences =[]
    current=[]
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip()
            if not line or line.startswith("#"):
                if current:
                    sentences.append(current)
                    current = []
                continue
            parts = line.split("\t")
            if len(parts) >= 3:          
                current.append((parts[1], parts[2]))
            elif len(parts) == 2:       
                current.append((parts[0], parts[1]))
    if current:
        sentences.append(current)
    return sentences

def parse_gold(path):
    sentences = []
    current = []
    sent_header = re.compile(r"^#?\s*[Ss]entence\s+\d+", re.IGNORECASE)

    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if sent_header.match(line):
                if current:
                    sentences.append(current)
                    current = []
                continue
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                token, tag = parts[0], parts[1]
                current.append((token, tag))
    if current:
        sentences.append(current)
    return sentences

# main comparison logic
def compare(conll_path, gold_path, output_path, max_sentences=50):
    machine_sents =parse_conll(conll_path)
    gold_sents= parse_gold(gold_path)
    n = min(max_sentences, len(machine_sents), len(gold_sents))
    total_tokens= 0
    total_mismatches =0
    discrepancy_blocks = []

    for sent_idx in range(n):
        m_sent =machine_sents[sent_idx]
        g_sent= gold_sents[sent_idx]
        max_len = max(len(m_sent), len(g_sent))
        sent_lines =[]
        for tok_idx in range(max_len):
            total_tokens+= 1
            if tok_idx < len(m_sent):
                m_tok, m_tag = m_sent[tok_idx]
            else:
                m_tok, m_tag = "???", "MISSING"
            if tok_idx < len(g_sent):
                g_tok, g_tag = g_sent[tok_idx]
            else:
                g_tok, g_tag = "???", "MISSING"
            token = m_tok if m_tok != "???" else g_tok
            if m_tag != g_tag:
                total_mismatches += 1
                sent_lines.append(
                    f"{token}\t"
                    f"WRONG_TAG: output={m_tag} | gold={g_tag}"
                )

        if sent_lines:
            sent_text = " ".join(t for t, _ in g_sent)
            block = [f"# Sentence {sent_idx + 1}: {sent_text}"]
            block.extend(sent_lines)
            discrepancy_blocks.append("\n".join(block))

    # writing output 
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("# DISCREPANCY REPORT\n")
        out.write(f"# Compared first {n} sentences\n")
        out.write(f"# Total tokens compared : {total_tokens}\n")
        out.write(f"# Total mismatches found: {total_mismatches}\n")
        out.write(f"# Sentences with errors : {len(discrepancy_blocks)}\n")
        out.write("#\n")
        out.write("# Format for each mismatch:\n")
        out.write("#   token   WRONG_TAG: output=<machine_tag> | gold=<reference_tag>\n")
        out.write("#\n\n")
        if discrepancy_blocks:
            out.write("\n\n".join(discrepancy_blocks))
            out.write("\n")
        else:
            out.write("# No discrepancies found! Both files agree on all tokens.\n")
    return n, total_tokens, total_mismatches, len(discrepancy_blocks)

# run 
if __name__ == "__main__":
    CONLL = "/mnt/user-data/uploads/output_eng_by_python_code.conll"
    GOLD = "/mnt/user-data/uploads/eng_data_first50_deepti_tagset.txt"
    OUTPUT = "/mnt/user-data/outputs/discrepancy_report.conll"

    import os
    os.makedirs("/mnt/user-data/outputs", exist_ok=True)

    n, tokens, mismatches, bad_sents = compare(CONLL, GOLD, OUTPUT)

    print(f"Compared {n} sentences, {tokens} tokens.")
    print(f"Found {mismatches} tag mismatches across {bad_sents} sentences.")
    print(f"Report written → {OUTPUT}")