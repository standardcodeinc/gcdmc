from __future__ import annotations

import datetime
import re

import phonenumbers

# From the W3C HTML5 spec:
# https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address
_email_regex: re.Pattern = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")


def is_valid_email(email: str) -> bool:
    """Returns whether or not the input string is a valid email address as
    defined by the W3C HTML5 spec.

    See: https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address
    """
    return _email_regex.match(email) is not None


def is_parseable_phone(number: str) -> bool:
    """Returns whether or not the input string is a phone number in E.164
    format.
    """
    try:
        # Note that we don't check if the number if valid. We could do this
        # with the `phonenumbers.is_valid_number` function, but this probably
        # isn't the right place to do it. For example, we don't check if
        # emails are real emails.
        phone: phonenumbers.PhoneNumber = phonenumbers.parse(number, None)
        return phonenumbers.is_possible_number(phone)
    except phonenumbers.phonenumberutil.NumberParseException:
        # This error is thrown if the input number is not in E.164 format
        return False


def is_valid_date(dt: datetime.datetime) -> bool:
    """Returns whether or not the input datetime could be considered a valid
    date.

    Note that we use datetime objects to represent dates since the Datastore
    does not have a native date type. To be considered a "date", the datetime
    object must have a UTC timezone and must be at exactly 00:00:00.000000.
    """
    return (dt.tzinfo is datetime.timezone.utc and dt.hour == 0
            and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0)
