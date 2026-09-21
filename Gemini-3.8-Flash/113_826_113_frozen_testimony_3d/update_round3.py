import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect what changes we need.
print("Original length:", len(content))
