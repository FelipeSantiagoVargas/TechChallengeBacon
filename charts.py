import matplotlib.pyplot as plt
import seaborn as sns

def graph_frequent_words(common_words):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=[word[0] for word in common_words], y=[count[1] for count in common_words])
    plt.title('Frequent Words in Generated Text')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.savefig('bar.png')

def graph_dist_len_words(df):
    df['word_lengths'] = df['transformed'].apply(lambda x: [len(word) for word in x])     
    plt.figure(figsize=(10, 6))
    sns.histplot(df['word_lengths'].explode(), bins=range(1, max(df['word_lengths'].explode()) + 1))
    plt.title('Distribution of Word Lengths in Generated Text')
    plt.xlabel('Word Length')
    plt.ylabel('Frequency')
    plt.savefig("distribution.png")