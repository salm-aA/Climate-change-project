"""Searching and sorting algorithms for the cinema application."""


def merge_sort(movie_list, field):
    """Sort movies using a recursive merge sort algorithm."""
    # A list with zero or one item is already sorted.
    if len(movie_list) <= 1:
        return movie_list[:]

    middle = len(movie_list) // 2
    left_half = merge_sort(movie_list[:middle], field)
    right_half = merge_sort(movie_list[middle:], field)

    sorted_list = []
    left_position = 0
    right_position = 0

    while left_position < len(left_half) and right_position < len(right_half):
        left_value = left_half[left_position][field]
        right_value = right_half[right_position][field]

        # Lowercase text so capital letters do not affect the order.
        if isinstance(left_value, str):
            left_value = left_value.lower()
            right_value = right_value.lower()

        if left_value <= right_value:
            sorted_list.append(left_half[left_position])
            left_position += 1
        else:
            sorted_list.append(right_half[right_position])
            right_position += 1

    sorted_list.extend(left_half[left_position:])
    sorted_list.extend(right_half[right_position:])
    return sorted_list


def binary_search(movie_list, title, low, high):
    """Recursively search a title-sorted movie list for an exact title."""
    if low > high:
        return None

    middle = (low + high) // 2
    middle_title = movie_list[middle]["title"].lower()
    wanted_title = title.lower()

    if middle_title == wanted_title:
        return movie_list[middle]
    if wanted_title < middle_title:
        return binary_search(movie_list, title, low, middle - 1)
    return binary_search(movie_list, title, middle + 1, high)


def search_movies(movie_list, search_text):
    """Search for an exact title, partial title, or genre."""
    search_text = search_text.strip().lower()
    if search_text == "":
        return movie_list[:]

    title_sorted = merge_sort(movie_list, "title")
    exact_movie = binary_search(title_sorted, search_text, 0, len(title_sorted) - 1)
    if exact_movie is not None:
        return [exact_movie]

    matching_movies = []
    for movie in movie_list:
        title_match = search_text in movie["title"].lower()
        genre_match = search_text in movie["genre"].lower()
        if title_match or genre_match:
            matching_movies.append(movie)
    return matching_movies
