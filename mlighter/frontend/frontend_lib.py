import sys
import os

sys.stdout = open('/dev/stdout', 'w')


def initialise_session():
    home_value = os.getenv('MLIGHTER_HOME')
    print("MLIGHTER_HOME: ", home_value)

    if home_value is None:
        home_value = os.path.join(os.getenv('HOME'),
            "mlighter", "mlighter")

    sys.path.append(home_value + "/backend")

    from MLighter import MLighter  # noqa

    session = MLighter({})

    return session


def log(string_to_log):
    print(string_to_log, file=sys.stdout)
