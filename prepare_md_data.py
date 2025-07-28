# prepare_md_data.py

import re

# Load your Markdown file
with open("plan.md", encoding="utf-8") as f:
    md_text = f.read()

# Split by headings (e.g., '## ', '### ', etc.)
chunks = re.split(r'\n#{1,6} ', md_text)
# Optional: Remove empty or too short chunks
chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20]

# Save to txt (optional, for check)
with open("chunks.txt", "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(c + "\n---\n")
print(f"Splitted into {len(chunks)} chunks.")
