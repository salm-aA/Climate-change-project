"""Simple searching and sorting algorithms for the cinema program."""


def bubble_sort(movie_list, field):
    """Return movies sorted by a chosen field using bubble sort."""
    sorted_movies = movie_list.copy()

    for pass_number in range(len(sorted_movies) - 1):
        for position in range(len(sorted_movies) - 1 - pass_number):
            first_value = sorted_movies[position][field]
            second_value = sorted_movies[position + 1][field]

            if isinstance(first_value, str):
                first_value = first_value.lower()
                second_value = second_value.lower()

            if first_value > second_value:
                temporary_movie = sorted_movies[position]
                sorted_movies[position] = sorted_movies[position + 1]
                sorted_movies[position + 1] = temporary_movie

    return sorted_movies


def binary_search(movie_list, title, low, high):
    """Use recursion to search a title-sorted movie list."""
    if low > high:
        return None

    middle = (low + high) // 2
    middle_title = movie_list[middle]["title"].lower()
    title = title.lower()

    if middle_title == title:
        return movie_list[middle]
    if title < middle_title:
        return binary_search(movie_list, title, low, middle - 1)
    return binary_search(movie_list, title, middle + 1, high)


def search_movies(movie_list, search_text):
    """Search by exact title, partial title or genre."""
    search_text = search_text.strip().lower()
    title_order = bubble_sort(movie_list, "title")

    exact_match = binary_search(title_order, search_text, 0, len(title_order) - 1)
    if exact_match is not None:
        return [exact_match]

    matches = []
    for movie in movie_list:
        if search_text in movie["title"].lower() or search_text in movie["genre"].lower():
            matches.append(movie)
    return matches
