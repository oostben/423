
import math
import statistics
from statistics import NormalDist
e = 2.718281828


def d_plus(S_t,X,r,sd,T,t):
    ret = math.log((S_t/X),e)
    ret += (r + (.5 * (sd**2))) * (( T - t )/365)
    ret /= (sd * math.sqrt((T-t)/365))

    return ret
def d_minus(S_t,X,r,sd,T,t):
    ret = math.log((S_t/X),e)
    ret += (r - (.5 * (sd**2))) * (( T - t )/365)
    ret /= (sd * math.sqrt( (T-t)/365 ) )

    return ret

def C_euro_at_t(S_t, X, r, d_plus, d_minus, T, t):
    normal_dist = statistics.NormalDist(mu = 0, sigma = 1)
    return (S_t * normal_dist.cdf(d_plus)) - ((e**(-1*r*((T-t)/365))) * X * normal_dist.cdf(d_minus))

def P_euro_at_t(S_t, X, r, d_plus, d_minus, T, t):
    normal_dist = statistics.NormalDist(mu = 0, sigma = 1)
    return X * (e**(-r*((T-t)/365))) * normal_dist.cdf(-d_minus) - S_t * normal_dist.cdf(-d_plus)

def der_C(d_plus):
    normal_dist = statistics.NormalDist(mu = 0, sigma = 1)
    return normal_dist.cdf(d_plus)

def der_P(d_plus):
    normal_dist = statistics.NormalDist(mu = 0, sigma = 1)
    return -normal_dist.cdf(-d_plus)

def calculate_portfolio_values(call, port, S_t, X, r, sd, T, t):
    d_plus_ = d_plus(S_t,X,r,sd,T,t)
    d_minus_ = d_minus(S_t,X,r,sd,T,t)
    
    print("d_plus at t=", t, ":", d_plus_)
    print("d_minus at t=", t, ":", d_minus_, "\n")

    if call:    
        option_price = C_euro_at_t(S_t, X, r, d_plus_, d_minus_, T, t)
    else:
        option_price = P_euro_at_t(S_t, X, r, d_plus_, d_minus_, T, t)
    
    if call: print("call price at t =", t, ":",option_price, "\n")
    else: print("put price at t =", t, ":",option_price, "\n")

    hedged = port.x * S_t + (port.y * (e**((r * t) / 365))) + port.z * option_price
    unhedged = port.x_bar * S_t + (port.y_bar * (e**((r * t) / 365))) + port.z_bar * option_price
    
    return hedged, unhedged



class portfolios:
    def __init__(self, x ,y ,z ,x_bar, y_bar, z_bar):
        self.x = x
        self.y = y
        self.z = z
        self.x_bar = x_bar
        self.y_bar = y_bar
        self.z_bar = z_bar
        print("Portfolio Initialization:")
        print(self)
    
    def __str__(self):
        return "x = " + str(self.x) + "\ny = " + str(self.y) + "\nz = " + str(self.z) + "\nx bar = " + str(self.x_bar) + "\ny_bar = " + str(self.y_bar) + "\nz_bar = " + str(self.z_bar) + "\n"


def hedge(quantity, call, r, S_0, T, X, sd, S_t, t):
    d_plus_ = d_plus(S_0,X,r,sd,T,0)
    d_minus_ = d_minus(S_0,X,r,sd,T,0)
    print("d_plus at t=0: ", d_plus_)
    print("d_minus at t=0: ", d_minus_, "\n")

    if call:    
        option_price = C_euro_at_t(S_0, X, r, d_plus_, d_minus_, T, 0)
        der_of_option_price = der_C(d_plus_)
    else:
        option_price = P_euro_at_t(S_0, X, r, d_plus_, d_minus_, T, 0)
        der_of_option_price = der_P(d_plus_)

    print("option price at t = 0:", option_price)
    print("option derivatie at t = 0:", der_of_option_price, "\n")

    z = quantity
    x = -z * der_of_option_price
    y = (-x * S_0) - (z * option_price)
    z_bar = quantity
    x_bar = 0
    y_bar = -z * option_price

    port = portfolios(x, y, z, x_bar, y_bar, z_bar)
  
    hedged, unhedged = calculate_portfolio_values(call, port, S_t, X, r, sd, T, t)

    print("hedged at t=", t, ", with S(",t,") =", S_t, ":", hedged)
    print("unhedged at t=", t, ", with S(",t,") =", S_t, ":", unhedged)

def prompt():
    quantity_in = float(input("How many options are you hedging?"))
    choice = int(input("Are they calls or options?\n1-> calls\n2-> puts"))
    call_in = True
    if choice == 2:
        call_in = False
    r_in = float(input("What is the interest rate r? (.05 or something)"))
    S_0_in = float(input("What is the price of the stock at time zero (S_0)?"))
    T_in = float(input("How many days until the options expire ?(enter 90 for 90 day options)"))
    X_in = float(input("What is the strike price of the options?"))
    sd_in = float(input("What is the sd  of the stock?"))
    
    compare_prices = []
    price = 9999999999
    while price != -1:
        price = float(input("At what prices do you want to compare the delta hedged portfolio to the unhedged? input -1 to stop. "))
        if price != -1:
            compare_prices.append(price)
    t_in = float(input("How many days in the future do you want to compare the hedged and unhedged portfolios?"))

    for price in compare_prices:
        print("----------------------------------------------------------------------------------")
        hedge(quantity=quantity_in, call=call_in, r=r_in, S_0=S_0_in, T=T_in, X=X_in, sd=sd_in, S_t=price, t=t_in)
prompt()