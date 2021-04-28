
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

# hedge(quantity=-300, call=True, r=.1, S_0=100, T=120, X=100, sd=.2, S_t=99, t=1)
print("----------------------------------------------------------------------------------")
hedge(quantity=5000, call=False, r=.05, S_0=20, T=90, X=20, sd=.35, S_t=19.5, t=1)
print("----------------------------------------------------------------------------------")
hedge(quantity=5000, call=False, r=.05, S_0=20, T=90, X=20, sd=.35, S_t=20.0, t=1)
print("----------------------------------------------------------------------------------")
hedge(quantity=5000, call=False, r=.05, S_0=20, T=90, X=20, sd=.35, S_t=20.5, t=1)