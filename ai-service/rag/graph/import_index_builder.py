import os
from collections import defaultdict

def build_import_indexes(repo_files):

    file_index = {}
    module_index = defaultdict(list)

    for f in repo_files:
        normalized = os.path.splitext(f)[0]
        normalized = normalized.replace("\\", "/")

        # removing src prefix for easier matching
        if "src/" in normalized:
            normalized = normalized.split("src/", 1)[1]
        file_index[normalized] = f

        module_name = os.path.basename(normalized)
        module_index[module_name].append(f)

    return file_index, module_index 