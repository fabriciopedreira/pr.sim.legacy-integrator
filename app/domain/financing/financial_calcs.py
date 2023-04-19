def pgto(monthly_interest_rate, number_of_periods, principal, total_iof, future_value=0):
    total_amount_with_iof = principal + total_iof

    monthly_interest_rate_decimal = monthly_interest_rate / 100

    factor = (1 + monthly_interest_rate_decimal) ** number_of_periods

    payment = -(
        total_amount_with_iof * factor * monthly_interest_rate_decimal - future_value * monthly_interest_rate_decimal
    ) / (factor - 1)

    return payment


def convert_annual_to_monthly_rate(annual_rate: float) -> float:
    annual_rate_decimal = annual_rate / 100
    monthly_rate_decimal = (1 + annual_rate_decimal) ** (1 / 12) - 1
    monthly_rate = monthly_rate_decimal * 100

    return monthly_rate


def convert_registration_fee_to_total_amount(financed_value: float, registration_fee_percent: float) -> float:
    return registration_fee_percent * financed_value / 100
