from app.helpers.hash_helper import hash_helper

user_password = "User1234"  # noqa: S105
users = [
    {
        "id": 1,
        "first_name": "user",
        "last_name": "account",
        "email": "sample@sample.com",
        "phone_number": "+905311111111",
        "password_hash": hash_helper.get_password_hash(user_password),
    },
]
