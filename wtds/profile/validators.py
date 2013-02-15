import re

from django.core.exceptions import ValidationError

RATIO_PATTERN = re.compile(r'\d+:\d+')

def is_ratio(value):
    if not RATIO_PATTERN.match(value):
        raise ValidationError("Ratio must be a value such as '16:10'")

