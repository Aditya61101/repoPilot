import os

def resolve_import(import_str, curr_file, file_index, module_index):
    import_str = import_str.strip().strip('"').strip("'")

    # ignoring external packages
    if not import_str.startswith((".", "@/")):
        return None
    
    # alias (@/)
    if import_str.startswith("@/"):
        key = import_str[2:]
        return file_index.get(key)
    
    # relative import
    if import_str.startswith('.'):
        base = os.path.dirname(curr_file)
        resolved = os.path.normpath(
            os.path.join(base, import_str)
        ).replace("\\", "/")

        if "src/" in resolved:
            resolved = resolved.split("src/", 1)[1]
        resolved = os.path.splitext(resolved)[0]
        
        if resolved in file_index:
            return file_index[resolved]
        
        module = os.path.basename(resolved)
        if module in module_index:
            return module_index[module][0]

    return None