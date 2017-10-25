import os


def get_last_commit_sha(file_name='version.txt'):
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r') as version_file:
                # If version.txt is available and readable use the version in it.
                return version_file.read().strip()
        except Exception:
            # If accessing the file fails return:
            return 'Unknown/Error'
    else:
        # Otherwise return development. This is the expected version to be shown
        # during local development phase.
        return 'Development'
