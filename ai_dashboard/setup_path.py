import sys
import os

def add_project_root():
    root_dir = os.path.dirname(os.path.abspath(__file__))     # ai_dashboard
    project_dir = os.path.dirname(root_dir)                  # project root

    if project_dir not in sys.path:
        sys.path.append(project_dir)


add_project_root()
