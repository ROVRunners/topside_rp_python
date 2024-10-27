"""Does file-related stuff"""


def file_to_dict(file_path: str, splitter: str = "=", comment: str = "#",
                 end_read: str = "|", line_count: int = -1) -> dict | None:
    """Convert the contents of a file into a dictionary of values.

    Args:
        file_path (str):
            The path to the file you want to open.
        splitter (str, optional):
            The character(s) that indicate the split between key and contents.
            Defaults to "=".
        comment (str, optional):
            The character(s) used to start ignored comment lines in the file.
            Defaults to "#".
        end_read (str, optional):
            The character(s) used to indicate that the text to be read stops here.
            Defaults to "|".
        line_count (int, optional):
            The number of lines to read if above 0, otherwise until the end. Includes comments.
            Defaults to -1.

    Returns:
        dict | None: The dictionary from the file or None if the file doesn't open.
    """
    dictionary = {}

    try:
        file = open(file_path, "r", encoding="UTF-8")
    except FileNotFoundError:
        return None

    line_arr = file.readlines[:]

    if line_count > 0:

        for line in line_arr[range(line_count)]:
            if line.startswith(comment):
                continue
            if line.startswith(end_read):
                break
            words = line.split(splitter)
            dictionary[words[0].strip()] = words[1].strip()

        return dictionary

    for line in line_arr:
        if line.startswith(comment):
            continue
        if line.startswith(end_read):
            break
        words = line.split(splitter)
        dictionary[words[0]] = words[1]

    return dictionary


def file_to_list(path: str) -> list[str] | None:
    """Convert the contents of a file into a list of its lines.

    Args:
        path (str):
            The path to the file you want to read.

    Returns:
        list[str] | None:
            An array of the lines in the file or None if the file doesn't open.
    """
    try:
        file = open(path, "r", encoding="UTF-8")
    except FileNotFoundError:
        return None
    
    return file.readlines()[:]
