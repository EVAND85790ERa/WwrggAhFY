# 代码生成时间: 2025-08-25 11:40:28
import quart
def random_number_generator(min_value: int, max_value: int) -> dict:
    """Generates a random number between two given values.

    Args:
# 改进用户体验
        min_value (int): The minimum value of the random number.
# FIXME: 处理边界情况
        max_value (int): The maximum value of the random number.

    Returns:
        dict: A dictionary containing the generated random number.

    Raises:
        ValueError: If the minimum value is greater than the maximum value.
    """
    if min_value >= max_value:
        raise ValueError("Minimum value cannot be greater than or equal to maximum value.")
    from random import randint
    return {"random_number": randint(min_value, max_value)}

# Quart route to handle GET request to /random endpoint
@quart.route("/random", methods=["GET"])
async def get_random_number():
# FIXME: 处理边界情况
    "