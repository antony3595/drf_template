from django.conf.global_settings import DATETIME_INPUT_FORMATS
from django.conf.global_settings import DATE_INPUT_FORMATS

DATE_FORMAT = "%d.%m.%Y"
DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"
DATETIME_INPUT_FORMATS += [DATETIME_FORMAT, DATE_FORMAT]
DATE_INPUT_FORMATS += [DATE_FORMAT, ]
