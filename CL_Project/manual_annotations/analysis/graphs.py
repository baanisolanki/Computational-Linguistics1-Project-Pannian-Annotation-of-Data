import matplotlib.pyplot as plt

# Data for Graph 1: english
tags1 = ['k1', 'k2', 'V', 'JJ', 'PSP', 'k7', 'VAUX', 'PUNC', 'RB', 'RP', 'k4', 'CC', 'k5', 'k3']
counts1 = [442, 321, 298, 192, 154, 148, 132, 94, 46, 42, 24, 18, 12, 10]
# Data for Graph 2: Hindi
tags2 = ['k1', 'k2', 'k3', 'k4', 'k5', 'k7', 'NN', 'JJ', 'RB', 'V', 'VAUX', 'PSP', 'PUNC', 'SYM', 'RP', 'CC']
counts2 = [76, 69, 9, 18, 7, 64, 105, 88, 12, 112, 40, 212, 141, 4, 4, 1]

def create_simple_plot(tags, counts, title, filename):
    plt.figure(figsize=(10, 6))
    plt.bar(tags, counts, color='skyblue', edgecolor='navy')
    plt.title(title)
    plt.xlabel('Linguistic Tags')
    plt.ylabel('Total Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

create_simple_plot(tags1, counts1, 'Tag Frequency Analysis: English manual Dataset', 'english_manual_analysis.png')
create_simple_plot(tags2, counts2, 'Tag Frequency Analysis: Hindi manual Dataset', 'hindi_manual_analysis.png')
