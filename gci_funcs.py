# here are a bunch of formulas from gci


def c_interest(initial, interest_rate, years_left):
    value = initial * (interest_rate**years_left)
    return value


def s_interest(initial, interest_rate, years_left):
    value = initial * (interest_rate * years_left)
    return value


def pdv(fv, interest, periods):
    value = fv / ((interest)**periods)
    return value


def perpetuity_value(initial, interest):
    value = initial / (interest - 1)
    return value


def long_period_value(initial, interest, periods):
    choice = input('Do you get paid this year? (y or n) \n')
    value = 0
    if 'n' in choice.lower():
        for p in range(1, periods + 1):
            value += initial / (interest**p)
    elif 'y' in choice.lower():
        for p in range(periods):
            value += initial / (interest**p)
    return value


def interest_free_financing(payment, interest, periods):
    value = 0
    choice = input('Is there a downpayment? (y or n) \n')
    if 'y' in choice.lower():
        for p in range(periods):
            value += payment / (interest**p)
    elif 'n' in choice.lower():
        for p in range(periods + 1):
            value += payment / (interest**p)
        value -= payment
    return value


def bond_calc(face_value, coupon_rate, interest, periods):
    coupon = face_value * (coupon_rate - 1)
    value = 0
    for p in range(1, periods + 1):
        value += coupon / (interest**p)
        print(value)
    value += face_value / (interest**periods)
    return value


def enterprise_value():
    # for fixed cost
    ev = input('What is the market cap?')
    debt = input('What is the debt?')
    nci = input('What is the non controlling interest?')
    ps = input('What is the preferred stock')
    cash = input('What is the cash?')
    enterprise_value = ev + debt + nci + ps - cash
    return enterprise_value

# Discounted Cash FLow


def wacc_calc(d, e, cost_of_e, cost_of_d, tax_rate):
    wacc = (e / (d + e)) * (cost_of_e) + (d / (d + e)) * (cost_of_d) * (1 - tax_rate)
    return wacc


# accounting
def ci_step(principle, rate, periods):
    periods = periods + 1
    for i in range(0, periods):
        current_value = c_interest(principle, rate, i)
        if i > 0:
            old_value = c_interest(principle, rate, i - 1)
        else:
            old_value = 0
        print(f"Total interest: {current_value - principle}")
        print(f"Interest: {current_value - old_value}")
        print(f"Current Value: {current_value}")

        if i != periods:
            n = input("\nNext?\n")


def pvoa(principle, interest, periods):
    PV = (principle / interest) * (1 - (1 / ((1 + interest)**periods)))
    return PV
