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
    invalid_login = 900, _("Kullanıcı email veya şifresi hatalı.")

    # Book Errors
    book_isbn_exists = 1002, _("Bu ISBN ile zaten aktif veya pasif bir kitap kaydı mevcut.")
