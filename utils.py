from datetime import datetime


def convert_datetime(date: str) -> datetime:
    """
        Convert date string to datetime format

        :param date: variable string with format dd-mm-yyyy
        :type date: str
        :return: datetime
        :raise: ValueError
    """
    try:
        converted_date = datetime.strptime(date, "%d-%m-%Y")
    except ValueError as e:
        raise ValueError(e)
    # check if the minimum date that can be consulted is lower 01-01-2013.
    if converted_date.year < 2013:
        raise ValueError("The minimum date that can be consulted is 01-01-2013")
    return converted_date
