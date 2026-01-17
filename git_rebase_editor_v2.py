import sys
import os
import re

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

print(f"Editing {file_name}")

with open(file_path, 'r') as f:
    content = f.read()

if "git-rebase-todo" in file_name:
    # Aggressively find ANY pick line with 'NIW evidence' and switch to reword
    new_content = []
    for line in content.splitlines():
        if "pick" in line and "NIW evidence" in line:
            new_content.append(line.replace("pick", "reword"))
        else:
            new_content.append(line)
    content = "\n".join(new_content)
    
elif "COMMIT_EDITMSG" in file_name:
    # Replace the sensitive term in the commit message
    content = content.replace("NIW evidence", "System Validation")

with open(file_path, 'w') as f:
    f.write(content)
