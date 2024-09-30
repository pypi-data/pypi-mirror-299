# timeLib.py
from datetime import datetime



def get_current_time(format_spec):
        """
        Zwraca bieżący czas lub datę zgodnie z podanym formatem.
        :param format_spec: Specyfikacja formatu np. 'DD:mm:YYYY' lub 'hh:mm:ss'
        :return: String z bieżącą datą/czasem
        """
        format_mapping = {
            'DD:mm:YYYY': '%d:%m:%Y',
            'hh:mm:ss': '%H:%M:%S',
            'YYYY-mm-DD': '%Y-%m-%d',
            'DD-mm-YYYY': '%d-%m-%Y',
            'mm/dd/YYYY': '%m/%d/%Y',
            'hh:mm AM/PM': '%I:%M %p'
        }

        if format_spec in format_mapping:
            return datetime.now().strftime(format_mapping[format_spec])
        else:
            raise ValueError(f"Nieznany format: {format_spec}")

def replace_time_tags(text):
        start = 0
        while True:
            start = text.find("{time_lib:(", start)
            if start == -1:
                break

            end = text.find(")}", start)
            if end == -1:
                raise ValueError("Nie znaleziono zamknięcia znacznika {time_lib}")

            # Wydobycie formatu z pomiędzy nawiasów
            format_spec = text[start + 11:end]
            current_time = get_current_time(format_spec)
            text = text[:start] + current_time + text[end + 1:]

            start += len(current_time)
        if "}" in text:
             text = text.replace("}", "")
        return text
