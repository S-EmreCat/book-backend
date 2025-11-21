from enum import IntEnum
from gettext import gettext as _


class Error(IntEnum):
    def __new__(cls, value, phrase):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        return obj

    # General Errors
    record_not_found = -5, _("Kayıt bulunamadı.")

    # Auth Errors
    invalid_login = 900, _("Invalid email or password.")
    user_email_exists = 901, _("Email already exists.")
    user_phone_exists = 902, _("Phone number already exists.")
    invalid_user_credentials = 903, _("Email or password is incorrect.")
    user_not_active = 904, _("User is not active.")

    invalid_current_password = 905, _("Current password is incorrect.")
    new_password_same_as_old = 906, _("New password cannot be the same as the current password.")

    # Author Errors
    author_already_exists = 1001, _("Author name already exists")

    # Category Errors
    category_name_exists = 1002, _("Category name already exists")

    # Book Errors
    book_isbn_exists = 1003, _("ISBN already exists.")
