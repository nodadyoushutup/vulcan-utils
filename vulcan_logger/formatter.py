# vulcan_logger/formatter.py
MS_IN_SECOND = 1000
MS_IN_MINUTE = 60 * MS_IN_SECOND
MS_IN_HOUR = 60 * MS_IN_MINUTE
MS_IN_DAY = 24 * MS_IN_HOUR
MS_IN_WEEK = 7 * MS_IN_DAY
MS_IN_MONTH = 30 * MS_IN_DAY  # Approximation
MS_IN_YEAR = 365 * MS_IN_DAY  # Simplified, does not account for leap years


class Formatter:
    """
    A class to format durations provided in milliseconds into various formats
    such as list, abbreviated string, or selective dictionary, with support
    for years, months, weeks, hours, minutes, seconds, and milliseconds.
    """

    def duration(self, milliseconds: int, format_type: type = list, delimiter: str = "") -> any:
        """
        Format the given duration in milliseconds to the specified format.

        Args:
            milliseconds (int): The duration in milliseconds.
            format_type (type): The type of format to return (list, str, dict).
            delimiter (str): The delimiter used to separate units in string format.

        Returns:
            list, str, dict: The formatted duration depending on format_type.
        """

        (
            years, months, weeks, days, hours, minutes, seconds, milliseconds
        ) = self._duration_calculate(milliseconds)
        parts = self._duration_parts(
            years, months, weeks, days, hours, minutes, seconds, milliseconds
        )
        if format_type == str:
            return delimiter.join(f"{value}{abbr}" for _, value, abbr in parts)
        elif format_type == list:
            return [(name, value) for name, value, _ in parts]
        elif format_type == dict:
            return {name: value for name, value, _ in parts if value > 0}

    def _duration_calculate(self, milliseconds: int) -> tuple:
        """
        Calculate the duration breakdown from milliseconds to years.

        Args:
            milliseconds (int): Duration in milliseconds.

        Returns:
            tuple: A tuple containing years, months, weeks, days, hours, minutes, seconds, milliseconds.
        """

        years = milliseconds // MS_IN_YEAR
        milliseconds %= MS_IN_YEAR
        months = milliseconds // MS_IN_MONTH
        milliseconds %= MS_IN_MONTH
        weeks = milliseconds // MS_IN_WEEK
        milliseconds %= MS_IN_WEEK
        days = milliseconds // MS_IN_DAY
        milliseconds %= MS_IN_DAY
        hours = milliseconds // MS_IN_HOUR
        milliseconds %= MS_IN_HOUR
        minutes = milliseconds // MS_IN_MINUTE
        milliseconds %= MS_IN_MINUTE
        seconds = milliseconds // MS_IN_SECOND
        milliseconds %= MS_IN_SECOND
        return years, months, weeks, days, hours, minutes, seconds, milliseconds

    def _duration_parts(
            self,
            years: int,
            months: int,
            weeks: int,
            days: int,
            hours: int,
            minutes: int,
            seconds: int,
            milliseconds: int
    ) -> list:
        """
        Gather non-zero duration parts into a list of tuples with abbreviations.

        Args:
            years (int): Duration breakdown.
            months (int): Duration breakdown.
            weeks (int): Duration breakdown.
            days (int): Duration breakdown.
            hours (int): Duration breakdown.
            minutes (int): Duration breakdown.
            seconds (int): Duration breakdown.
            milliseconds (int): Duration breakdown.

        Returns:
            list of tuples: List of non-zero duration parts as (name, value, abbreviation) tuples.
        """

        parts = []
        if years > 0:
            parts.append(("years", years, "y"))
        if months > 0:
            parts.append(("months", months, "mo"))
        if weeks > 0:
            parts.append(("weeks", weeks, "w"))
        if days > 0:
            parts.append(("days", days, "d"))
        if hours > 0:
            parts.append(("hours", hours, "h"))
        if minutes > 0:
            parts.append(("minutes", minutes, "m"))
        if seconds > 0:
            parts.append(("seconds", seconds, "s"))
        if milliseconds > 0:
            parts.append(("milliseconds", milliseconds, "ms"))
        return parts
