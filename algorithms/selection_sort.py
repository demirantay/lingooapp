def descending_selection_sort(array):
    """selection sort algorithm implementation in descending order"""

    for i in range(0, len(array), 1):
        maximum = i

        for j in range(i+1, len(array), 1):
            if array[j] > array[maximum]:
                maximum = j

        # swapping the found element
        temp = array[i]
        array[i] = array[maximum]
        array[maximum] = temp

    return array


def ascending_selection_sort(array):
    """selection sort algorithm implementation in ascending order"""

    for i in range(0, len(array), 1):
        minimum = i

        for j in range(i+1, len(array), 1):
            if array[j] < array[minimum]:
                minimum = j

        # swapping the found element
        temp = array[i]
        array[i] = array[minimum]
        array[minimum] = temp

    return array
