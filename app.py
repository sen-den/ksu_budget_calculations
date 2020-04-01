import json
import sys
from typing import Optional

INPUT_FILE_PATH = 'data/data.json'
OUTPUT_FILE_PATH = 'data/result.json'


class Coefficient:
    def __init__(self, data: dict):
        self.A: float = data['A']
        self.RK: float = data['RK']
        self.M: float = data['M']
        self.RP: float = data['RP']
        self.N: float = data['N']
        self.MV: float = data['MV']
        self.PV: float = data['PV']

    def calculate_a(self):
        self.A = self.RK * self.M * self.RP * self.N * self.MV * self.PV
        return self.A


class Budget:
    STUDENTS_AMOUNT = None
    BASE = None
    TOTAL = None
    STABLE = None
    INDEX_BASED = None
    SOCIAL_PAYMENTS = None

    def init(self, data: dict):
        self.STUDENTS_AMOUNT = data["STUDENTS_AMOUNT"]
        self.BASE = data["BASE"]
        self.TOTAL = data["TOTAL"]
        self.STABLE = data["STABLE"]
        self.INDEX_BASED = data["INDEX_BASED"]
        self.SOCIAL_PAYMENTS = data["SOCIAL_PAYMENTS"]
        return self


def correct_total(current_total, next_total, min_ratio, max_ratio):
    next_current_ratio = next_total / current_total

    if next_current_ratio < min_ratio:
        reserve = current_total * (min_ratio - next_current_ratio) / next_current_ratio
    elif next_current_ratio > max_ratio:
        reserve = current_total * (max_ratio - next_current_ratio) / next_current_ratio
    else:
        reserve = 0

    return next_total + reserve


def main(argv):
    input_data = None
    with open(INPUT_FILE_PATH, mode='r') as file:
        input_data = json.load(file)

    coefficient = Coefficient(input_data['COEFFICIENT'])

    base_next_current_ratio = input_data['BASE_NEXT_CURRENT_RATIO']
    min_ratio = input_data['MIN_RATIO']
    max_ratio = input_data['MAX_RATIO']

    current_budget = Budget().init(input_data['CURRENT'])

    next_budget = Budget()
    next_budget.INDEX_BASED = input_data['TMP_L'] * coefficient.calculate_a()
    next_budget.STABLE = input_data['STABILITY_COEFFICIENT'] * (current_budget.TOTAL - current_budget.SOCIAL_PAYMENTS)
    next_budget.SOCIAL_PAYMENTS = current_budget.SOCIAL_PAYMENTS

    next_budget.BASE = next_budget.STABLE + next_budget.INDEX_BASED  # !
    next_budget.TOTAL = correct_total(
        current_budget.BASE,
        next_budget.BASE,
        min_ratio,
        max_ratio
    )

    with open(OUTPUT_FILE_PATH, mode='w') as file:
        result = {
            "coefficients": coefficient.__dict__,
            "next_budget": next_budget.__dict__
        }
        json.dump(result, file, indent=2)

if __name__ == "__main__":
    main(sys.argv[1:])
