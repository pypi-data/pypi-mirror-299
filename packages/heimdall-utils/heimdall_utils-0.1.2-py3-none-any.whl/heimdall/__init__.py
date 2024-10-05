import os


def _get_pickles_folder():
    cwd = os.getcwd()

    current_directory = cwd

    while True:
        pickles_folder = os.path.join(current_directory, ".pickles")

        if os.path.isdir(pickles_folder):
            return pickles_folder

        parent_directory = os.path.dirname(current_directory)

        if parent_directory == current_directory:
            return f"{cwd}/.pickles"

        current_directory = parent_directory


PICKLES_FOLDER = _get_pickles_folder()


__all__ = ["PICKLES_FOLDER"]
