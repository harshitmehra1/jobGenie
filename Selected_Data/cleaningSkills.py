# File path
file_path = "./Selected_Data/skills.txt"

# Step 1: Read all words from the file
with open(file_path, "r", encoding="utf-8") as file:
    words = file.read().splitlines()

# Step 2: Clean and normalize
# Remove empty strings, strip whitespace, and convert to lowercase
cleaned_words = [word.strip().lower() for word in words if word.strip()]

# Step 3: Remove duplicates using a set
unique_words = set(cleaned_words)

# Step 4: Sort the words alphabetically
sorted_words = sorted(unique_words)

# Step 5: Write back to the same file
with open(file_path, "w", encoding="utf-8") as file:
    for word in sorted_words:
        file.write(word + "\n")

print("File cleaned and updated successfully.")
