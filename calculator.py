import numpy.matlib 
import numpy as np
from numpy.linalg import inv 
import math

def main():
    print("welcome to the calculator")
    while True:
        print()
        print()
        print()

        print("OPTIONS---------------------------------------------------------------------------------")
        print("1 - simple_compounding_interest")
        print("2 - continuous_interest")
        print("3 - stocks_problem")
        print("4 - value_at_risk")
        print()
        print()
        print()

        option = int(input("what would you like to calculate"))
        if option == 1:
            simple_compounding_interest()
        if option == 2:
            continuous_interest()
        if option == 3:
            stocks_problem()
        if option == 4:
            value_at_risk()


def value_at_risk():
    number_of_stocks = int(input("number_of_stocks:"))
    stocks = [[0.0,0.0] for i in range(number_of_stocks)]

    for i in range(number_of_stocks):
        print("mean of stock", i, ":")
        stocks[i][0] = float(input())
    for i in range(number_of_stocks):
        print("SD of stock", i, ":")
        stocks[i][1] = float(input())

    m = np.ones(len(stocks)) 
    s = np.ones(len(stocks)) 

    for i in range(len(stocks)):
        m[i] = stocks[i][0]
        s[i] = stocks[i][1]

    w = np.ones(len(stocks))

    for i in range(len(stocks)):
        print("weight of stock ", i, ":")
        w[i] = float(input())
    
    print("\n\nreturn calculation ------------")

    print("total return:", calculate_return(m,w))

    print("\n\nSD calculation ------------")
    c = calculate_cov_matrix(s)
    variance_of_portfolio =   np.matmul(w, np.matmul(c, w.transpose()))
    print("Variance of portfolio w C w^T  = ", variance_of_portfolio)
    print("SD of portfolio sqrt(w C w^T) = ", math.sqrt(variance_of_portfolio))

    sd = math.sqrt(variance_of_portfolio)
    mu = calculate_return(m,w)
    z = float(input("\n\nwhat is the Z value (less that)?"))
    print("imbetween calculation: (z * sd) + mu  = ", (z * sd) + mu)
    starting_val_of_portfolio = float(input("what is the starting_val_of_portfolio?"))
    value_of_portfolio = (1+(((z * sd) + mu))) * starting_val_of_portfolio
    value_at_risk = starting_val_of_portfolio - value_of_portfolio

    print("value_of_portfolio = (1+(((z * sd) + mu))) * starting_val_of_portfolio")
    print("value_of_portfolio = ", value_of_portfolio)

    print("value_at_risk = starting_val_of_portfolio - value_of_portfolio")
    print("valaue at risk = ", value_at_risk, "\n\n")

def simple_compounding_interest():
    principle = float(input("input_principle:"))
    compund_rate = float(input("number of time compounds happen per year:"))
    rate = float(input("interest rate:"))
    time = float(input("time (in years):"))
    print(principle, "*", "(1 + (", rate, "/", compund_rate, "))^", compund_rate, "*", time)
    print("=", principle * (1.0+(rate/compund_rate))**(compund_rate * time))
    return

def continuous_interest():
    principle = float(input("input_principle:"))
    rate = float(input("rate:"))
    time = float(input("time (in years):"))
    print(principle, "*", "e^(", rate, "*", time,")")
    print("=", principle * 2.71828**(rate*time))
    return

def stocks_problem():
    number_of_stocks = int(input("number_of_stocks:"))
    stocks = [[0.0,0.0] for i in range(number_of_stocks)]

    for i in range(number_of_stocks):
        print("mean of stock", i, ":")
        stocks[i][0] = float(input())
    for i in range(number_of_stocks):
        print("SD of stock", i, ":")
        stocks[i][1] = float(input())

    calculate_mean_SD(stocks)


def calculate_return(m, w):
    ret = np.matmul(m, w.transpose())
    return ret

def calculate_cov_matrix(s):
    option = int(input("how would you like to put in the corr/cov --> 1 = corr coef, 2 = cov"))
    c = np.ones((len(s),len(s)))
    for i in range(len(s)):
        for j in range(len(s)):
            if i == j:
                c[i][j] = s[i]**2.0
    for i in range(len(s)):
        for j in range(i,len(s)):
            if i != j:
                if option == 1:
                    print("what is the correlation coefficient between stock ", i, ", ", j )
                    corr_coef = float(input())
                    cov = corr_coef * (s[i]*s[j])
                    c[i][j] = cov
                    c[j][i] = cov
                else:
                    print("what is the covariance between stock ", i, ", ", j )
                    cov = float(input())
                    c[i][j] = cov
                    c[j][i] = cov
    return c

def calculate_mean_SD(stocks):
    m = np.ones(len(stocks)) 
    s = np.ones(len(stocks)) 

    for i in range(len(stocks)):
        m[i] = stocks[i][0]
        s[i] = stocks[i][1]

    w = np.ones(len(stocks))

    for i in range(len(stocks)):
        print("weight of stock ", i, ":")
        w[i] = float(input())

    print("\n\ntotal return ------------------------------------------------------------------------------------")

    print("total return:", calculate_return(m,w))

    print("\n\nSD calculation -----------------------------------------------------------------------------------")

    c = calculate_cov_matrix(s)
    variance_of_portfolio =   np.matmul(w, np.matmul(c, w.transpose()))
    print("Variance of portfolio w C w^T  = ", variance_of_portfolio)
    print("SD of portfolio sqrt(w C w^T) = ", math.sqrt(variance_of_portfolio))


    print("\n\nMVP calculation ------------------------------------------------------------------------------------")
    top = np.matlib.ones((len(stocks),1))
    print("1 C^-1  /  1 C^-1 1^T")
    ones = np.ones(len(stocks))
    print(c)
    c_inv = inv(c)
    top = np.matmul(ones, c_inv)
    bottom = np.matmul(ones, np.matmul(c_inv, ones.transpose()))

    print("top w_mvp = ", top)
    print("bottom w_mvp= ", bottom)
    w_mvp = top / bottom
    print("weights w_mvp = ", w_mvp)

    print("return of MVP: ", calculate_return(m, w_mvp))
    variance_of_MVP =   np.matmul(w_mvp, np.matmul(c, w.transpose()))
    print("Variance of MVP w C w^T  = ", variance_of_MVP)
    print("SD of MVP sqrt(w C w^T) = ", math.sqrt(variance_of_MVP))

    print("\n\nW_star calculation ------------------------------------------------------------------------------------")

    top_star = np.matmul(m, c_inv)
    bottom_star = np.matmul(m, np.matmul(c_inv, ones.transpose()))
    w_star = top_star / bottom_star

    print("w_star = m c_inv  /  m c_inv 1^T")
    print("w_star = ", w_star)
    print("\n\nW_efficient frontier calculation ------------------------------------------------------------------------------------")

    first_term_w_eff = w_star
    second_term_w_eff = (-1.0 * w_star) + w_mvp

    print("w_eff = sig * w_mvp + (1-sig) * w_star")
    print("w_eff = first_term + sig * second_term")

    print("w_eff first_term = ", first_term_w_eff)
    print("w_eff second_term = ", second_term_w_eff)

    print("w_eff return parameterized by sigma: mu(sigma) = ", np.matmul(m, first_term_w_eff.transpose()), " + sigma * ", np.matmul(m, second_term_w_eff.transpose()))

    print("\n\nfunctions of portfolios on efficient frontier with no risk free --------------------------------------------------------------------------------------------------")

    while int(input("Would you like to calculate something on efficient frontier? type 1 if yes")) == 1:
        print("would you like to calculate given a return? input 1")
        print("would you like to calculate given a SD? input 2")

        # print("would you like to calculate a return given a sigma? input 3")
        # print("would you like to calculate a SD given a sigma? input 4")
        option = int(input("whats your option?"))

        if option == 1:
            ret = float(input("whats your return?"))
            first_num = np.matmul(m,first_term_w_eff.transpose())
            second_num = np.matmul(m,second_term_w_eff.transpose())
            sigma = (ret - first_num) / second_num
            print("sigma = ", sigma)
            w_in = first_term_w_eff + (sigma * second_term_w_eff)
            print("weights = ", w_in)
            variance_of_portfolio =   np.matmul(w_in, np.matmul(c, w_in.transpose()))
            print("Variance of portfolio w C w^T  = ", variance_of_portfolio)
            print("SD of portfolio sqrt(w C w^T) = ", math.sqrt(variance_of_portfolio))
            
        elif option == 2:
            sd = float(input("whats your SD?"))
            sigma = 0
            potentials = []
            for s in range(-100000, 100000,1):
                s/=1000.0
                w_temp = first_term_w_eff + (second_term_w_eff * s)
                
                compar = math.sqrt(np.matmul(w_temp, np.matmul(c, w_temp.transpose())))
                # print(s, compar,sd)
                if abs(compar - sd) < .0001:
                    print(compar-sd)
                    w_in = first_term_w_eff + (second_term_w_eff * s)
                    ret = calculate_return(m,w_in)
                    potentials.append([ret, w_in, s])
            
            max_index = 0
            max_val = 0
            i = 0
            while i < len(potentials):
                print(potentials[i])
                if potentials[i][0] > max_val:
                    max_index = i
                    max_val = potentials[i][0]
                i+=1
            print("sigma = ", potentials[max_index][2])
            print("weights = ", potentials[max_index][1])
            print("total return:")
            print(potentials[max_index][0])
    
    print("Done with calculate something on efficient frontier -------------")
    while int(input("Would you like to calculate a market portfolio? -- 1 if yes")) == 1:

        rfr = float(input("whats the risk free rate?"))

        top = np.matmul((m - (rfr * ones)), c_inv)
        print("top = (m - rfr 1) c_inv")
        print("top = ", top)

        bottom = np.matmul(np.matmul((m - (rfr * ones)), c_inv), ones.transpose())
        print("bottom = (m - rfr 1) c_inv ones^T)")
        print("bottom = ", bottom)

        w_market = top / bottom
        print("w_market = ", w_market, "\n\n")

        
        while 1 == int(input("would you like to calculate somehting on this efficient frontier? 1 if yes")):
            if 1 == int(input("calculate a return given an sd --> 1 \n calculate a sd given an return --> 2 \nwhats your choice?")):
                sd = float(input("Whats your sd?"))
                print("[sqrt(1) / [(m - rfr 1) c_inv (m - rfr1)^T))]] * (return - rfr)")
                first_term_bottom = np.matmul(m - (rfr * ones), np.matmul(c_inv, (m - (rfr * ones)).transpose()))
                print("first_term_bottom = ", first_term_bottom)

                first_term_total = math.sqrt(1.0/ first_term_bottom)
                print("first_term_total = sqrt(1.0/ first_term_bottom)")
                print("first_term_total = ", first_term_total)
                
                ret = sd / first_term_total
                ret += rfr
                print("return = ", ret, "\n\n")
            else:
                ret = float(input("Whats your return?"))
                print("[sqrt(1) / [(m - rfr 1) c_inv (m - rfr1)^T))]] * (return - rfr)")

                first_term_bottom = np.matmul(m - (rfr * ones), np.matmul(c_inv, (m - (rfr * ones)).transpose()))
                print("first_term_bottom = ", first_term_bottom)

                first_term_total = math.sqrt(1.0/ first_term_bottom)
                print("first_term_total = sqrt(1.0/ first_term_bottom)")
                print("first_term_total = ", first_term_total)
                
                second_term = (ret - rfr)
                print("second_term = (ret - rfr)")
                print("second_term = ", second_term )

                sd = first_term_total * second_term
                print("sd = first_term_total * second_term")
                print("sd = ", sd, "\n\n")
    print("\n\nTHNAKS FOR DOING STOCKS PROBLEM -------------")

main()