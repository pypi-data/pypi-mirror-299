# Function to calculate the mean
def mean(*args):
    return sum(args) / len(args)


# Function to calculate the slope for linear regression
def slope(*args):
    # Separate x and y values
    x = args[::2]  # Every even index (starting from 0)
    y = args[1::2]  # Every odd index (starting from 1)

    n = len(x)

    if n < 2:  # Need at least two points to calculate slope
        raise ValueError("At least two points are required to calculate the slope.")

    mean_x = mean(*x)  # Calculate mean_x
    mean_y = mean(*y)  # Calculate mean_y

    # Calculate numerator and denominator
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))

    # Check for division by zero
    if denominator == 0:
        raise ValueError("Slope is undefined (vertical line).")

    return numerator / denominator  # Return the slope value
