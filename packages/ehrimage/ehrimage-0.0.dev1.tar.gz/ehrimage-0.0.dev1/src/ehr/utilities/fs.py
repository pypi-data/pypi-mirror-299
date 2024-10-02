import os
import pathlib as pl
from public import public


@public
def filename(path: str):
    return pl.Path(path).name


@public
def list_files(root, full_path=True):
    """list files directly under root"""
    filenames = [fn for fn in os.listdir(root) if os.path.isfile(os.path.join(root, fn))]

    return [os.path.join(root, fn) for fn in filenames] if full_path else filenames


@public
def list_nested_files(root, fn_includes: list[str] = None, fn_excludes: list[str] = None, full_path=True, **kwargs):
    """list files nested under root"""
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(root, **kwargs):
        for fn in filenames:
            # when it doesn't meet any filter condition, skip to next
            if fn_includes:
                if not any(kw in fn for kw in fn_includes):
                    continue
            if fn_excludes:
                if any(kw in fn for kw in fn_excludes):
                    continue

            # when it passes all filters
            file_paths.append(os.path.join(dirpath, fn))

    return file_paths if full_path else [filename(str(fp)) for fp in file_paths]


if __name__ == "__main__":
    test_path = "/Users/san/ds/datasets/physionet.org/files/mimiciv/2.2"
    print(list_files(test_path))
    print(list_nested_files(test_path))
