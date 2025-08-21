initial_investment = int(input("Vpisi zacetno investicijo (eur): "))
interest_rate = float(input("Vpisi donosnost v %: "))
time_period = int(input("Vpisi časovni period (v letih): "))

"""
FUNKCIJA; OBRESTNO OBRESTOVANJE
@:param principal: zacetna investicija
@:param rate: donosnost v %
@:param time: čas v letih
@:return: koliko imaš skupaj
"""
def calculate_compound_interest(principal, rate, time):
    print("----------------------------------------------------------------")
    print("COMPOUND OBRESTOVANJE")
    interest_rate_decimal = rate / 100  # Uporabnik vnese npr. 10%, mi ga spremenimo v 0.1
    compounded_cash = principal
    for i in range(0, time):
        compounded_cash = compounded_cash * (1 + interest_rate_decimal)
    profit = compounded_cash - principal  # Čisti dobiček
    print(f"V vseh teh letih smo zaslužili čistega {profit:.2f} eur")
    print(f"Vse skupaj pa je sedaj keša: {compounded_cash:.2f} eur")
    return profit

"""
FUNKCIJA; NAVADNO OBRESTOVANJE
@:param principal: zacetna investicija
@:param rate: donosnost v %
@:param time: čas v letih
@:return: koliko imaš skupaj
"""
def calculate_simple_interest(principal, rate, time):
    obresti = principal * rate * time / 100
    skupaj = principal + obresti
    print("----------------------------------------------------------------")
    print("NAVADNO OBRESTOVANJE")
    print(f"V vseh teh letih smo zaslužili čistega: {obresti} eur")
    print(f"Vse skupaj pa je sedaj keša: {skupaj} eur")
    return skupaj


calculate_simple_interest(initial_investment,interest_rate,time_period)
calculate_compound_interest(initial_investment, interest_rate, time_period)


