import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.metrics import (confusion_matrix, f1_score, accuracy_score,precision_score, recall_score, ConfusionMatrixDisplay)

plt.style.use('seaborn-v0_8')

plt.rcParams.update({"font.size": 11,"axes.titlesize": 14,"axes.labelsize": 12,"xtick.labelsize": 10,"ytick.labelsize": 10})

def parse_gold(filepath):
    sentences = []
    current = []

    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')

            if line.startswith('#') or line.strip() == '':
                if current:
                    sentences.append(current)
                    current = []
                continue

            if re.match(r'^\d+$', line.strip()):
                if current:
                    sentences.append(current)
                    current = []
                continue

            parts = line.split('\t')
            if len(parts) >= 3:
                word = parts[1].strip()
                tag  = parts[2].strip()
                current.append((word, tag))

    if current:
        sentences.append(current)

    return sentences[50:100]

def parse_predicted(filepath):
    sentences = []
    current = []

    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')

            if line.startswith('# Sentence'):
                if current:
                    sentences.append(current)
                    current = []
                continue

            if line.strip() == '' or line.startswith('#'):
                continue

            parts = line.split('\t')
            if len(parts) >= 2:
                word = parts[0].strip()
                tag  = parts[1].strip()
                current.append((word, tag))

    if current:
        sentences.append(current)

    return sentences

def align_tags(gold_sents, pred_sents):
    gold_flat, pred_flat = [], []
    skipped_sents = 0

    for g_sent, p_sent in zip(gold_sents, pred_sents):

        g_filtered = [(w, t) for w, t in g_sent if t not in ('PUNC', 'rs', '.')]
        p_filtered = [(w, t) for w, t in p_sent if t not in ('rs', '.')]

        if len(g_filtered) != len(p_filtered):
            skipped_sents += 1

        for (gw, gt), (pw, pt) in zip(g_filtered, p_filtered):
            gold_flat.append(gt)
            pred_flat.append(pt)

    print(f"Sentences with mismatch: {skipped_sents}")
    print(f"Total tokens compared : {len(gold_flat)}")

    return gold_flat, pred_flat

if __name__ == '__main__':

    GOLD_FILE = 'cl_eng_python.txt'
    PRED_FILE = 'gpt_eng_few.txt'

    print("Parsing...")
    gold_sents = parse_gold(GOLD_FILE)
    pred_sents = parse_predicted(PRED_FILE)

    print(f"Gold: {len(gold_sents)} | Pred: {len(pred_sents)}")

    print("\nAligning...")
    gold_tags, pred_tags = align_tags(gold_sents, pred_sents)

    all_labels = sorted(set(gold_tags) | set(pred_tags))
                        
    accuracy  = accuracy_score(gold_tags, pred_tags)
    precision = precision_score(gold_tags, pred_tags,labels=all_labels,average='weighted',zero_division=0)
    recall = recall_score(gold_tags, pred_tags,labels=all_labels,average='weighted',zero_division=0)
    f1 = f1_score(gold_tags, pred_tags,labels=all_labels,average='weighted',zero_division=0)

    f1_per_class = f1_score(gold_tags, pred_tags,labels=all_labels,average=None,zero_division=0)
    prec_pc= precision_score(gold_tags, pred_tags,labels=all_labels,average=None,zero_division=0)
    rec_pc= recall_score(gold_tags, pred_tags,labels=all_labels,average=None,zero_division=0)

    print("\nFew Shot Annotation")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1: {f1:.4f}")

    cm = confusion_matrix(gold_tags, pred_tags, labels=all_labels)

    fig1, ax1 = plt.subplots(figsize=(12, 10))
    disp = ConfusionMatrixDisplay(cm, display_labels=all_labels)
    disp.plot(ax=ax1,cmap='Blues',xticks_rotation=45,colorbar=True,values_format='d')
    ax1.grid(False)
    ax1.set_title('Confusion Matrix: Few Shot Annotation',fontsize=16,fontweight='bold',pad=20)
    ax1.tick_params(axis='both', length=0)
    plt.tight_layout()
    fig1.savefig('gpt_few_confusion_matrix.png', dpi=300)

    fig2, axes = plt.subplots(1, 2, figsize=(24, 7))
    fig2.suptitle('POS Tagging Evaluation',fontsize=17,fontweight='bold',y=1.03)
                     
    ax2 = axes[0]

    x = np.arange(len(all_labels)) 
    width = 0.25

    bars1 = ax2.bar(x-width,prec_pc,width,label='Precision')
    bars2 = ax2.bar(x,rec_pc,width,label='Recall')
    bars3 = ax2.bar(x+width,f1_per_class,width,label='F1')

    ax2.set_title('Per-Class Metrics',fontweight='bold')
    ax2.set_ylabel('Score')
    ax2.set_ylim(0, 1.05)
    ax2.set_xticks(x)
    ax2.set_xticklabels(all_labels, rotation=60, ha='right')
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.4)

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            val = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2,val + 0.01,f'{val:.2f}',ha='center',fontsize=7)

    ax3 = axes[1]

    metric_names = ['Accuracy', 'Precision', 'Recall', 'F1']
    metric_values = [accuracy, precision, recall, f1]

    bars2 = ax3.bar(metric_names,metric_values,color=['#4C72B0', '#55A868', '#C44E52', '#8172B3'],edgecolor='black',linewidth=1.0,width=0.55)

    ax3.set_title('Overall Metrics', fontweight='bold')
    ax3.set_ylim(0, 1.05)
    ax3.grid(axis='y', linestyle='--', alpha=0.4)

    for bar, val in zip(bars2, metric_values):
        ax3.text(bar.get_x() + bar.get_width()/2,val + 0.02,f'{val:.3f}',ha='center',fontsize=11,fontweight='bold')

    plt.tight_layout()
    fig2.savefig('few_gpt.png', dpi=300, bbox_inches='tight')


    fig_p, ax_p = plt.subplots(figsize=(12, 6))
    ax_p.bar(all_labels, prec_pc, edgecolor='black')
    ax_p.set_title('Precision per Tag')
    ax_p.set_ylim(0, 1.05)
    ax_p.set_xticks(range(len(all_labels)))
    ax_p.set_xticklabels(all_labels, rotation=60, ha='right')
    plt.tight_layout()
    fig_p.savefig('precision_gpt_few.png', dpi=300)

    fig_r, ax_r = plt.subplots(figsize=(12, 6))
    ax_r.bar(all_labels, rec_pc, edgecolor='black')
    ax_r.set_title('Recall per Tag')
    ax_r.set_ylim(0, 1.05)
    ax_r.set_xticks(range(len(all_labels)))
    ax_r.set_xticklabels(all_labels, rotation=60, ha='right')
    plt.tight_layout()
    fig_r.savefig('recall_gpt_few.png', dpi=300)

    fig_f, ax_f = plt.subplots(figsize=(12, 6))
    ax_f.bar(all_labels, f1_per_class, edgecolor='black')
    ax_f.set_title('F1 per Tag')
    ax_f.set_ylim(0, 1.05)
    ax_f.set_xticks(range(len(all_labels)))
    ax_f.set_xticklabels(all_labels, rotation=60, ha='right')
    plt.tight_layout()
    fig_f.savefig('f1_gpt_few.png', dpi=300)

    print("\n Per-Class Metrics ")
    print(f"{'Tag':<10} {'Prec':>8} {'Rec':>8} {'F1':>8}")
    print("-" * 34)

    for lbl, p, r, f in zip(all_labels, prec_pc, rec_pc, f1_per_class):
        print(f"{lbl:<10} {p:.2f}  {r:.2f}  {f:.2f}")

    plt.show()

    print("\nDone.")

