from flask import request


class LoginForm:
    def __init__(self):
        self.email = request.form.get("email", "").strip().lower()
        self.password = request.form.get("password", "")
        self.errors = {}

    def validate(self):
        if not self.email:
            self.errors["email"] = "Email is required."
        if not self.password:
            self.errors["password"] = "Password is required."
        return not self.errors
