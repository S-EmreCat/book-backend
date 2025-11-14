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
  user_email_exists = 901, _("Bu e-posta adresi ile zaten bir kullanıcı mevcut.")
  user_phone_exists = 902, _("Bu telefon numarası ile zaten bir kullanıcı mevcut.")
  invalid_user_credentials = 903, _("E-posta veya şifre hatalı.")
  user_not_active = 904, _("Bu kullanıcı sisteme giriş yapamaz.")

  invalid_current_password = 905, _("Mevcut şifre yanlıştır.")
  new_password_same_as_old = 906, _("Yeni şifre mevcut şifreyle aynı olamaz.")


    # Author Errors
    author_already_exists = 1001, _("Author name already exists")

    # Category Errors
    category_name_exists = 1002, _("Category with this name already exists.")
    # Book Errors
    book_isbn_exists = 1003, _("Bu ISBN ile zaten aktif veya pasif bir kitap kaydı mevcut.")
