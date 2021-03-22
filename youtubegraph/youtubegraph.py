import easyocr
from . import helpers
from PIL import Image


def ocr(img_path):
    """

    :param img_path: The path to the YouTube mobile screenshot
    :return: OCR data including location coordinates and text
    """
    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path)


def get_graph_coords(ocr_data):
    """

    :param ocr_data: YouTube mobile screenshot OCR data from EasyOCR
    :return: The left, top, right, and bottom coordinates of the entire time watched bar graph
    """
    left = top = right = bottom = None

    for item in ocr_data:
        coords = item[0]
        text = item[1]

        # Get the graph left coord using the coord of "X hr X min daily average"
        # Get the graph top coord using the coords of either "X hr X min daily average" or "X% from last week"
        # Need the lowest top coord, "X% from last week" might not be there

        if any(x in text for x in ['daily', 'average', 'averaqe']):
            left, graph_top = coords[3]

        if all(x in text for x in ['last', 'week']):
            top = coords[3][1]

        # Get the graph right coord using the top-left coord of one of the graph labels "X hr" or "X min"
        # Check length to skip over "X hr X min daily average" and skip if right already assigned
        if any(x in text for x in ['hr', 'min']) and len(text) < 7 and not right and helpers.has_numbers(text):
            right = coords[0][0]

        # Get the graph bottom coord using the top-left coord of any of the graph labels
        if any(x in text for x in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']):
            bottom = coords[0][1]

    return left, top, right, bottom


def get_bar_coords(graph_coords):
    """

    :param graph_coords: The left, top, right, and bottom coordinates of the entire time watched bar graph
    :return: A list of coordinates for each bar of the time watched bar graph
    """
    graph_left, graph_top, graph_right, graph_bottom = graph_coords

    bar_width = (graph_right - graph_left) / 7

    bar_coords = []
    pos = graph_left
    while pos < graph_right - bar_width:
        left = pos
        right = pos + bar_width
        bar_coords.append((left, graph_top, right, graph_bottom))
        pos += bar_width

    return bar_coords


def get_bars(bar_coords, screenshot):
    """

    :param bar_coords: A list of coordinates for each bar of the time watched bar graph
    :param screenshot: YouTube mobile screenshot PIL Image object
    :return: Separate bars of the bar graph as a list of PIL Image objects
    """
    cropped_bars = []
    for coord in bar_coords:
        cropped_bar = screenshot.crop(coord)
        cropped_bars.append(cropped_bar)

    return cropped_bars


def count_bar_px(bars):
    """

    :param bars: Separate bars of the bar graph as a list of PIL Image objects
    :return: A list containing the number of pixels in each bar, excluding gray and white surrounding pixels
    """
    bar_px_nums = []
    for bar in bars:
        num_px = helpers.count_non_gray_px(bar)
        bar_px_nums.append(num_px)

    return bar_px_nums


def get_bar_times(bar_px_nums, seconds_per_px):
    """

    :param bar_px_nums: A list containing the number of pixels in each bar, excluding gray and white surrounding pixels
    :param seconds_per_px: The estimated number of seconds each pixel represents
    :return: A list of time strings in hh:mm:ss format
    """
    bar_seconds_list = []
    for px_num in bar_px_nums:
        bar_seconds_list.append(px_num * seconds_per_px)

    hms_list = []
    for sec in bar_seconds_list:
        hms_list.append(helpers.seconds_to_hms(sec))

    return hms_list


def get_graph_labels(ocr_data):
    """

    :param ocr_data: YouTube mobile screenshot OCR data from EasyOCR
    :return: The graph labels from the time watched bar graph
    """
    day_strings = []

    for item in ocr_data:
        text = item[1]

        if any(x in text for x in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']):
            day_strings.append(text)

    # The last label is always "Today"
    day_strings.append('Today')

    return day_strings


def get_past_week_seconds(ocr_data):
    """

    :param ocr_data: YouTube mobile screenshot OCR data from EasyOCR
    :return: The last 7 days watched time in seconds
    """
    past_week_sec = None

    for item in ocr_data:
        text = item[1]

        # Get the text of the  last instance of "min" appearing with numbers, that is the last 7 days time string
        if 'min' in text and helpers.has_numbers(text):
            past_week_str = text
            past_week_sec = helpers.hr_min_str_to_seconds(past_week_str)

    return past_week_sec


def estimate(screenshot_path):
    """

    :param screenshot_path: The path to the YouTube mobile screenshot
    :return: A dictionary containing the time watched bar graph labels and times
    """
    screenshot = Image.open(screenshot_path)

    ocr_data = ocr(screenshot_path)

    graph_coords = get_graph_coords(ocr_data)
    bar_coords = get_bar_coords(graph_coords)
    graph_labels = get_graph_labels(ocr_data)

    bars = get_bars(bar_coords, screenshot)
    bar_px_nums = count_bar_px(bars)

    past_week_seconds = get_past_week_seconds(ocr_data)
    seconds_per_px = past_week_seconds / sum(bar_px_nums)

    bar_times = get_bar_times(bar_px_nums, seconds_per_px)

    return dict(zip(graph_labels, bar_times))
