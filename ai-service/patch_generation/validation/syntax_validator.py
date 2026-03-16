import os
import subprocess
import tempfile
from constants import SYNTAX_CHECKERS

def validate_file_syntax(file_path, code):

    ext = os.path.splitext(file_path)[1].lower()
    
    if ext not in SYNTAX_CHECKERS:
        # unknown language → skip validation
        return True, ""
    
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=ext,
            delete=False,
            mode="w",
            encoding="utf-8"
        ) as tmp:
            tmp.write(code)
            temp_path = tmp.name

        cmd = SYNTAX_CHECKERS[ext] + [temp_path]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            error = result.stderr or result.stdout
            return False, error.strip()

        return True, ""
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
