"""Script which sums together the numbers in the current time."""


def sum_current_time(time_str: str) -> int:
    """Expects data in the format HH:MM:SS"""

    if type(time_str) != str:
        raise TypeError("Error: input not a string.")

    list_of_nums = time_str.split(":")

    if len(list_of_nums) == 3 and all(num.isnumeric() for num in list_of_nums):
        return sum(int(num) for num in list_of_nums)

    raise ValueError("Error: input not in the format HH:MM:SS.")
