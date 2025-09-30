# Specify the file path (update this if needed)
filename = "c:\\practice\\practice_sample.txt"

# Dictionary to store word counts
word_counts = {}

# Open the file and read contents
with open(filename, 'r') as file:
    text = file.read().lower()  # Convert text to lowercase for case-insensitive counting

    # Replace punctuation marks with spaces for cleaner splitting
    for ch in ['.', ',', '!', '?', ':', ';', '"', "'"]:
        text = text.replace(ch, " ")

    words = text.split()  # Split text into individual words

    # Count the frequency of each word
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

# Print each word and its frequency
for word, count in word_counts.items():
    print(f"{word}: {count}")
