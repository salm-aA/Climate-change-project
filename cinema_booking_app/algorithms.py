"""Searching and sorting algorithms used by the cinema application."""


def merge_sort_movies(movies, field):
    """Return a new movie list sorted by field using recursive merge sort."""
    if len(movies) <= 1:
        return movies[:]

    middle = len(movies) // 2
    left = merge_sort_movies(movies[:middle], field)
    right = merge_sort_movies(movies[middle:], field)
    return _merge(left, right, field)


def _merge(left, right, field):
    """Merge two sorted movie lists."""
    result = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        left_value = left[left_index][field]
        right_value = right[right_index][field]
        if isinstance(left_value, str):
            left_value = left_value.lower()
            right_value = right_value.lower()

        if left_value <= right_value:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def recursive_binary_search(movies, title, low=0, high=None):
    """Find an exact title in a title-sorted list using recursive binary search."""
    if high is None:
        high = len(movies) - 1
    if low > high:
        return None

    middle = (low + high) // 2
    middle_title = movies[middle]["title"].lower()
    wanted_title = title.strip().lower()

    if middle_title == wanted_title:
        return movies[middle]
    if wanted_title < middle_title:
        return recursive_binary_search(movies, title, low, middle - 1)
    return recursive_binary_search(movies, title, middle + 1, high)


def search_movies(movies, search_text):
    """Search exact titles first, then return partial title or genre matches."""
    query = search_text.strip().lower()
    if not query:
        return movies[:]

    title_sorted = merge_sort_movies(movies, "title")
    exact_match = recursive_binary_search(title_sorted, query)
    if exact_match:
        return [exact_match]

    matches = []
    for movie in movies:
        if query in movie["title"].lower() or query in movie["genre"].lower():
            matches.append(movie)
    return matches
