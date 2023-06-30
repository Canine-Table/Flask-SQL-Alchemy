from flask import flash

class QueryException(Exception):
    error_messages = []

    @classmethod
    def add_error_message(cls,error):
        cls.error_messages.append(error)

    @classmethod
    def error_count(cls):
        return bool(len(cls.error_messages) > 0)

    @classmethod
    def show_error_messages(cls):
        for error in cls.error_messages:
            flash(f"{error}", category='danger')
        raise QueryException

    @classmethod
    def clear_errors(cls):
        cls.error_messages = []
