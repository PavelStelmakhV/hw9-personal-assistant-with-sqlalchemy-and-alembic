import functools


def parser_handler(func):
    @functools.wraps(func)
    def wrapper(self, user_input: str):
        try:
            return func(self, user_input)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)

    return wrapper


def command_handler(func):
    @functools.wraps(func)
    def wrapper(*args):
        # return func(*args)
        try:
            return func(*args)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)
        except Exception as e:
            raise SystemExit(f"Good bye! (some exception: {e})")

    return wrapper
