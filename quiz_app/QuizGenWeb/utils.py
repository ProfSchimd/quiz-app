import os
import tempfile
import uuid

def make_temp_dir(name: str = None) -> str | None:
    """
    Creates a temporary directory with the given name,
    or a randomly generated name if none is provided.
    Returns the path of the created directory, or None on failure.
    """
    base = tempfile.gettempdir()
    if name is None:
        name = str(uuid.uuid1())
    dir_path = os.path.join(base, name)
    try:
        os.makedirs(dir_path)
    except Exception:
        return None
    print(f"{name} - {dir_path}")
    return dir_path