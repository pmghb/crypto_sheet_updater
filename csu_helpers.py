#!/usr/bin/env python3
"""Module that contains helper functions used in main module."""

def round_float(num: float):
    """Rounds the last digits to two decimal places, keeping the intermediate zeros."""
    if num is None:
        return 0

    s = f"{num:.15f}"
    zeros = 0
    for c in s[2:]:
        if c != "0":
            break
        zeros += 1

    return round(float(s), zeros+2)
