"""String formatter for CLI output."""

from string import Formatter

MAX_LINE_LENGTH = 80


class CustomOutputFormatter(Formatter):
    """Formats common output components."""

    def format_field(self, value, format_spec):
        padding = (MAX_LINE_LENGTH - len(str(value))) // 2
        if format_spec == 'title':
            return ('=' * padding) + str(value).upper() + ('=' * padding)
        if format_spec == 'header':
            return str(value).upper()
        if format_spec == 'diff_minus':
            return '- ' + str(value)
        if format_spec == 'diff_plus':
            return '+ ' + str(value)
        if format_spec == 'separator':
            return '=' * MAX_LINE_LENGTH
        return super().format_field(value, format_spec)
