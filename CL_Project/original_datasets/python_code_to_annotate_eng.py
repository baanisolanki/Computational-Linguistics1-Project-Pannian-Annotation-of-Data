import re

DETERMINERS = {"the", "a", "an", "this", "that", "these", "those"}

PREPOSITIONS = {
    "for", "to", "in", "on", "of", "with", "from", "at", "by",
    "after", "before", "across", "into", "upon", "about", "over",
    "under", "between", "among", "through", "during", "without"
}

PUNCTUATION = {".", ",", "!", "?", ";", ":", "-", "...", "\"", "'"}

AUXILIARY_VERBS = {
    "is", "are", "was", "were", "be", "been", "being",
    "has", "have", "had", "do", "does", "did",
    "will", "would", "shall", "should", "may", "might",
    "must", "can", "could", "need", "dare", "used"
}

COMMON_ADVERBS = {
    "sharply", "quickly", "slowly", "suddenly", "recently", "already",
    "always", "never", "often", "sometimes", "usually", "also", "just",
    "still", "again", "too", "very", "quite", "almost", "together",
    "however", "therefore", "thus", "hence", "otherwise", "meanwhile",
    "finally", "initially", "eventually", "certainly", "clearly",
    "significantly", "largely", "mainly", "mostly", "nearly", "rapidly"
}

COMMON_ADJECTIVES = {
    "new", "old", "good", "bad", "large", "small", "big", "high", "low",
    "long", "short", "young", "late", "early", "last", "next", "first",
    "great", "little", "own", "right", "public", "same", "able", "local",
    "central", "global", "national", "western", "eastern", "northern",
    "southern", "record", "major", "key", "main", "general", "important",
    "possible", "real", "best", "strong", "free", "sure", "top", "human"
}

COMMON_VERBS = {
    "announced", "reached", "reacted", "discovered", "said", "told",
    "found", "made", "took", "came", "went", "saw", "knew", "got",
    "gave", "left", "kept", "let", "put", "set", "met", "ran", "held",
    "brought", "thought", "showed", "heard", "led", "read", "grew",
    "lost", "fallen", "risen", "broken", "chosen", "written", "driven",
    "reported", "added", "noted", "stated", "claimed", "argued", "warned",
    "confirmed", "revealed", "suggested", "indicated", "announced",
    "launched", "signed", "passed", "approved", "rejected", "released",
    "opened", "closed", "started", "ended", "increased", "decreased",
    "raised", "cut", "hit", "killed", "died", "lived", "worked", "played",
    "called", "asked", "tried", "used", "turned", "moved", "changed",
    "happened", "appeared", "remained", "included", "continued", "faced"
}

# common preposition to karaka mapping for nouns that follow them
PREP_TO_KARAKA = {
    "for":    "k4",   # recipient
    "to":     "k4",   # recipient/Goal
    "from":   "k5",   # source
    "with":   "k3",   # instrument
    "by":     "k3",   # instrument/Agent (passive)
    "in":     "k7",   # spatio-temporal
    "on":     "k7",   # spatio-temporal
    "at":     "k7",   # spatio-temporal
    "after":  "k7",   # temporal
    "before": "k7",   # temporal
    "across": "k7",   # spatial
    "into":   "k7",   # spatial
    "upon":   "k7",   # spatial
    "about":  "k2",   # theme
    "of":     "k2",   # theme/genitive
    "over":   "k7",
    "under":  "k7",
    "through":"k7",
    "during": "k7",
}

# the pos guesser 
def guess_pos(word):
    w = word.lower()
    if w in PUNCTUATION:           
        return "PUNC"
    if w in DETERMINERS:           
        return "DET"
    if w in PREPOSITIONS:          
        return "PREP"
    if w in AUXILIARY_VERBS:       
        return "AUX"
    if w in COMMON_ADVERBS:        
        return "ADV"
    if w in COMMON_ADJECTIVES:     
        return "ADJ"
    if w in COMMON_VERBS:          
        return "VERB"
    # suffix rules 
    if w.endswith("ly"):                        
        return "ADV"
    if w.endswith("ing"):                       
        return "VERB"
    if w.endswith("ed"):                        
        return "VERB"
    if w.endswith("tion") or w.endswith("sion"):
        return "NOUN"
    if w.endswith("ment") or w.endswith("ness"):
        return "NOUN"
    if w.endswith("ity") or w.endswith("ity"): 
        return "NOUN"
    if w.endswith("al") or w.endswith("ous"): 
        return "ADJ"
    if w.endswith("ive") or w.endswith("ful"): 
        return "ADJ"
    if w.endswith("less") or w.endswith("able"):
        return "ADJ"
    if w.endswith("ible"):                      
        return "ADJ"
    if w.endswith("er") or w.endswith("est"): 
        return "ADJ"  
    if w.endswith("s") and len(w) > 3:          
        return "NOUN" 

    # capitalised mid-sentence means proper noun
    if word[0].isupper():                       
        return "PROPN"
    return "NOUN"  # default


# the paninian label assigner 
def assign_paninian(words, idx):
    word = words[idx]
    w    = word.lower()
    pos  = guess_pos(word)

    # punctuation
    if pos == "PUNC":
        return "PUNC"
    # determiners
    if pos == "DET":
        return "adj"
    # prepositions
    if pos == "PREP":
        return "PSP"
    # adverbs
    if pos == "ADV":
        return "adv"
    # adjectives
    if pos == "ADJ":
        return "adj"
    # auxiliary / main verb
    if pos in {"VERB", "AUX"}:
        return "V"
    # nouns and proper nouns 
    if pos in {"NOUN", "PROPN"}:
        # find the verb index (first verb in sentence)
        verb_idx = None
        for j, w2 in enumerate(words):
            if guess_pos(w2) in {"VERB", "AUX"} and w2.lower() not in AUXILIARY_VERBS:
                verb_idx = j
                break
        # check if preceded by a preposition
        if idx > 0:
            prev_word = words[idx - 1].lower()
            if prev_word in PREP_TO_KARAKA:
                return PREP_TO_KARAKA[prev_word]
            # skip over determiner to look one more back
            if prev_word in DETERMINERS and idx > 1:
                prev2 = words[idx - 2].lower()
                if prev2 in PREP_TO_KARAKA:
                    return PREP_TO_KARAKA[prev2]
        # before verb is subject, goes to k1
        if verb_idx is not None and idx < verb_idx:
            return "k1"
        # after verb is object goes to k2
        if verb_idx is not None and idx > verb_idx:
            return "k2"
        return "k1"  # fallback
    return "adj"  # fallback for all

#compound noun fixer 
def fix_compounds(sentence):
    """
    If two consecutive tokens are both k1 or both k2,
    the first one is a noun modifier → adj.
    E.g. 'Stock(k1) markets(k1)' → 'Stock(adj) markets(k1)'
    """
    result = list(sentence)
    for i in range(len(result) - 1):
        word, tag   = result[i]
        _, next_tag = result[i + 1]
        if tag in {"k1", "k2"} and next_tag in {"k1", "k2"}:
            result[i] = (word, "adj")
    return result

# the file processor 
def process_file(input_path, output_path):
    raw_sentences =[]
    current_words =[]
    meta_lines=[]

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#"):
                meta_lines.append(stripped)
                continue
            if not stripped:
                if current_words:
                    raw_sentences.append((meta_lines, current_words))
                    current_words =[]
                    meta_lines= []
                continue
            parts = stripped.split()
            if len(parts)< 2:
                continue
            try:
                int(parts[0])
            except ValueError:
                continue
            current_words.append(parts[1])

    # flush last sentence
    if current_words:
        raw_sentences.append((meta_lines, current_words))

    print(f"Read {len(raw_sentences)} sentences.")

    # annotate
    annotated = []
    for meta, words in raw_sentences:
        tagged = [(w, assign_paninian(words, i)) for i, w in enumerate(words)]
        tagged = fix_compounds(tagged)
        annotated.append((meta, tagged))

    # write CoNLL output
    with open(output_path, "w", encoding="utf-8") as out:
        for sent_id, (meta, tokens) in enumerate(annotated, start=1):
            out.write(f"# sent_id = {sent_id}\n")
            for m in meta:
                out.write(m + "\n")
            for i, (word, tag) in enumerate(tokens, start=1):
                out.write(f"{i}\t{word}\t{tag}\n")
            out.write("\n")

    print(f"Done! {len(annotated)} sentences written to '{output_path}'")


# run 
process_file(
    "/Users/baanisolanki/Documents/CL1_Sem2/CL1_PROJECT/Computational-Linguistics1-Project-Pannian-Annotation-of-Data/CL_Project/original_datasets/english_dataset.conll",
    "output.conll"
)