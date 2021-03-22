import re


def hr_min_str_to_seconds(hr_min_str):
    """

    :param hr_min_str: A time string in the format "H hr M min"
    :return: The total number of seconds
    """
    numbers = [int(num) for num in re.findall(r'\d+', hr_min_str)]

    if len(numbers) < 2:  # Contains only minutes
        minutes = numbers[0]
    else:
        hours = numbers[0]
        minutes = (hours * 60) + numbers[1]

    return minutes * 60


def seconds_to_hms(seconds):
    """

    :param seconds: A number of seconds
    :return: A time string in the format "hh:mm:ss"
    """
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def has_numbers(string):
    """

    :param string: A string
    :return: True if the string contains numbers
    """
    return bool(re.search(r'\d', string))


def count_non_gray_px(img):
    """

    :param img: A PIL Image object
    :return: The number of gray or white pixels in the image with equal RGB channels
    """
    count = 0
    for x in range(img.width):
        for y in range(img.height):
            current_color = img.getpixel((x, y))
            if not current_color[0] == current_color[1] == current_color[2]:  # Pixel is not white or gray
                count += 1
    return count


def print_dictionary(dictionary):
    """
    Prints the key, value pairs of a dictionary
    :param dictionary: A dictionary
    """
    for key, value in dictionary.items():
        print(f'{key}: {value}')
