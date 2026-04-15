PRODUCT_TEMPERATURE_RANGES = {
    "vaccines": {"min_temp": 2.0, "max_temp": 8.0},
    "dairy": {"min_temp": 1.0, "max_temp": 4.0},
    "fresh_food": {"min_temp": 0.0, "max_temp": 5.0},
    "frozen_food": {"min_temp": -18.0, "max_temp": -15.0},
}


def get_product_range(product_type: str):
    return PRODUCT_TEMPERATURE_RANGES.get(product_type.lower())