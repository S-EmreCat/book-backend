from enum import IntEnum
from gettext import gettext as _


class Error(IntEnum):
    def __new__(cls, value, phrase):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        return obj

    # General Errors
    record_not_found = -5, _("Record not found.")

    # Auth Errors
    invalid_login = 900, _("Invalid email or password.")
    user_email_exists = 901, _("Email already exists.")
    user_phone_exists = 902, _("Phone number already exists.")
    invalid_user_credentials = 903, _("Email or password is incorrect.")
    user_not_active = 904, _("User is not active.")
    invalid_current_password = 905, _("Current password is incorrect.")
    new_password_same_as_old = 906, _("New password cannot be the same as the current password.")

    # Author Errors
    author_not_found = 1000, _("Author not found.")
    author_already_exists = 1001, _("Author name already exists.")

    # Category Errors
    category_not_found = 2000, _("Category not found.")
    category_name_exists = 2001, _("Category name already exists.")

    # Book Errors
    book_not_found = 3000, _("Book not found.")
    book_isbn_exists = 3001, _("ISBN already exists.")
    favorite_already_exists = 3002, _("Favorite already exists.")

    # User Errors
    user_not_found = 4000, _("User not found.")
    invalid_status_for_update = 4001, _("Status can only be 'active' or 'passive'.")
