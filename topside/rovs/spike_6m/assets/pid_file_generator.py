import json


def generate_pid_file():
    """Generate a PID file."""

    pid = {
        "depth_pid": {
            "P": 1,
            "I": 1,
            "D": 1,
        },
        "yaw_pid": {
            "P": 1,
            "I": 1,
            "D": 1,
        },
        "pitch_pid": {
            "P": 1,
            "I": 1,
            "D": 1,
        },
        "roll_pid": {
            "P": 1,
            "I": 1,
            "D": 1,
        },
    }

    with open("pid_values.json", "w") as file:
        print("Generating PID file...")
        json.dump({"PID": pid}, file)


if __name__ == "__main__":
    generate_pid_file()