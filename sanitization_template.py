"""
Implement clean_sensor_readings and then run the simple test cases below.
"""
def clean_sensor_readings(readings):
    cleaned = []
    for value in readings:
        try:
            if value is None:
                continue

            number = float(value)

            # Remove negative values
            if number < 0:
                continue

            # Clip values above 500
            if number > 500.0:
                number = 500.0

            cleaned.append(number)

        except (ValueError, TypeError):
            # Skip values that cannot be converted to float
            continue

    return cleaned



def run_tests():
    # Once implemented, these cases should pass.
    assert clean_sensor_readings([1, "2.5", None, -3, "bad", 700]) == [1.0, 2.5, 500.0]
    assert clean_sensor_readings([]) == []
    assert clean_sensor_readings([None, "nope", -1]) == []
    print("Section 1 tests passed.")

# Test cases
print(clean_sensor_readings([10, "20.5", None, -5, 600, "invalid"]))
# Expected: [10.0, 20.5, 500.0]

print(clean_sensor_readings([]))
# Expected: []

print(clean_sensor_readings([None, "abc", -10, "50.5"]))
# Expected: [50.5]


if __name__ == "__main__":
    run_tests()
