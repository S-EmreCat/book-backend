from app.helpers.hash_helper import hash_helper

admin_user_password = "Admin1234"  # noqa: S105
admin_user = [
    {
        "id": 1,
        "first_name": "admin",
        "last_name": "account",
        "email": "sample@sample.com",
        "phone_number": "+905311111111",
        "password_hash": hash_helper.get_password_hash(admin_user_password),
    },
]
