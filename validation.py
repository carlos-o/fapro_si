from re import fullmatch


def validate_date(date: str) -> bool:
    """
        Validate is string date format is correct

        :param date: variable string with format dd-mm-yyyy
        :type date: str
        :return: True is validation pass
        :return: False is not pass
    """
    # check if date format is correct
    if fullmatch(r"(^0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4}$)", date):
        return True
    return False
