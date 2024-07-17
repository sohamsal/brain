import json

prepositions = {"according", "they're", "they'd", "you'd", "it", "i'm", "when","you","you're","it's", "of", "to", "in", "on", "at", "by", "with", "from", "into", "out", "under", "above", "over", "through", "across", "around", "before", "behind", "between", "among", "up", "down", "in", "out", "on", "off", "about", "above", "below", "beside", "between", "beyond"}
articles = {"the", "a", "an", "this", "that", "these", "those", "my", "your", "his", "her", "its", "our", "their"}
auxiliary_verbs = {"is", "are", "am", "be", "been", "being", "was", "were", "will", "would", "can", "could", "may", "might", "shall", "should", "must", "ought", "need", "dare", "do", "does", "did", "done", "has", "had", "having", "have", "has", "had", "having", "will", "would", "can", "could", "may", "might", "shall", "should", "must", "ought", "need", "dare", "do", "does", "did", "done"}
conjunctions = {"and", "but", "or", "nor", "for", "so", "yet", "then", "than", "although", "though", "if", "unless", "until", "while", "as", "since", "because", "inasmuch", "insofar", "provided", "supposing", "lest", "that", "whether", "whichever", "whomever", "whosoever"}

words_to_remove = prepositions | articles | auxiliary_verbs | conjunctions

with open('json_data/transcript.json', 'r') as file:
    data = json.load(file)

# Filter out prepositions
filtered_data = [item for item in data if item['word'].lower() not in words_to_remove]

# Save the filtered data to a new JSON file
with open('json_data/filtered_ungrouped.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)

print("Unnecessary words removed and output saved to filtered_ungrouped.json")