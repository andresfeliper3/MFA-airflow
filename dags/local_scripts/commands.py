import os
import sys

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))  # Get the absolute path of the parent directory
sys.path.append(project_root)  # Add the project root to the Python path

from src.local_scripts.analyze import load_organism, whole_MFA

# Get the command-line arguments
args = sys.argv

# Print the command-line arguments
print("Arguments passed:", args)

# You can access individual arguments by indexing sys.argv

if args[1] == "analyze":
    load_organism()

# change sequences.yaml to include all sequences
# make them be selectable by name or GCF