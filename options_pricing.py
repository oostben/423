#p = (r-d)/(u-d)
def yes_no():
    print("1 -> yes")
    print("2 -> no")
    if int(input()) == 1:
        return True, False
    else:
        return False, True

def solve_for_p(r,u,d):
    if r == -1 or u == -1 or d == -1: return -1
    print("(r-d)/(u-d)")
    print("=",(r-d)/(u-d))
    return (r-d)/(u-d)

def solve_for_u(p,r,d):
    if p == -1 or r == -1 or d == -1: return -1
    #p(u-d) = (r-d)
    #(u-d) = (r-d)/p
    #u = ((r-d)/p) + d
    print("((r-d)/p) + d")
    print("=",((r-d)/p) + d)
    return ((r-d)/p) + d

def solve_for_d(p,r,u):
    if p == -1 or r == -1 or u == -1: return -1
    #p = (r-d)/(u-d)

    #p(u-d) = (r-d)
    #(u-d) = (r-d)/p
    #(u-d) = (r/p)-(d/p)
    #u = (r/p)-(d/p)+d
    #u-(r/p) = d-(d/p)
    #u-(r/p) = d*(1-(1/p))
    #(u-(r/p))/(1-(1/p)) = d
    print("(u-(r/p))/(1-(1/p))")
    print("=", (u-(r/p))/(1-(1/p)))
    return (u-(r/p))/(1-(1/p))

def print_tree(root):
    print("############################### Tree Print ###############################")
    row = 0
    q = [root, "sentinal"]
    while(len(q) != 0):
        node = q.pop(0)
        if node == "sentinal":
            row +=1
            print("Row -> ", row, " -------------------------------------------")
            if len(q) != 0:
                q.append("sentinal")
        else:
            node.print_node()
            for child in node.children:
                q.append(child)

class Node:
    def __init__(self, parent_in=None, row_in=0, index_in=0, root_in=None):
        self.parent = parent_in
        self.row = row_in
        self.index = index_in
        self.root = root_in
        self.children = []
        print("Creating new node.")
        print("Input -1 if value is unkown.")
        self.price = float(input("Price -> "))
        self.p_val = float(input("P value -> "))
        yes = True
        while yes:
            print("You are on node with price ->", self.get_price(), "P value ->", self.get_p_val())
            print("Right now this node has children:")
            if len(self.children) == 0:
                print("No children")
            else:
                for index,child in enumerate(self.children):
                    print("Child #", index)
                    child.print_node()
            print("Do you want to add more children?")
            yes, no = yes_no()
            if yes:
                temp_index = 0
                if self.parent is not None:
                    for sib in self.parent.children:
                        if sib == self:
                            temp_index += len(self.children)
                            break
                        else:
                            temp_index += len(sib.children)
                else:
                    temp_index = len(self.children)
                self.children.append(Node(parent_in=self, row_in=self.get_row()+1, index_in=temp_index, root_in=self.root))

    def print_node(self):
        print("******************")
        print("Node print")
        print("(", self.get_row(), ",", self.get_index(),")")
        print("Price -> ", self.get_price())
        print("P value -> ", self.get_p_val())
        print("******************")

    def get_price(self): return self.price
    def get_p_val(self): return self.p_val
    def get_row(self): return self.row
    def get_index(self): return self.index


class Tree:
    def __init__(self):
        self.root = None
        self.depth = 0
        self.scenarios = []

        self.print_welcome_mess()
        self.get_r()
        self.root = Node()
        self.label()
        self.solve()
        print_tree(self.root)
        self.w_calc()
        self.option_pricing_helper()

    def option_pricing_helper(self):
        strike_price = float(input("What strike price do you want?"))
        self.calculate_european(strike_price)
        self.calculate_american(strike_price)
        self.calculate_custom(strike_price)
    
    def w_calc(self):
        depth_calculated = False
        q = [self.root]
        while len(q) > 0:
            curr_node = q.pop(0)
            for child in curr_node.children:
                q.append(child)
            if len(curr_node.children) == 0:
                w_temp = 1
                curr_node2 = curr_node
                while curr_node2.parent is not None:
                    if not depth_calculated: self.depth += 1
                    w_temp *= curr_node2.get_p_val()
                    curr_node2 = curr_node2.parent
                depth_calculated = True
                self.scenarios.append([w_temp, curr_node.price])
        for index, scenario in enumerate(self.scenarios):
            print("Scenario #", index, " = ", scenario[0])
    
    def calculate_european(self, strike_price):
        call_price = 0
        put_price = 0
        for scenario in self.scenarios:
            call_price += scenario[0] * self.call_payoff(scenario[1], strike_price)
            put_price += scenario[0] * self.put_payoff(scenario[1], strike_price)
        call_price /= ((1+self.r)**(self.depth))
        put_price /= ((1+self.r)**(self.depth))
        print("**********************************")
        print("Euopean Option Pricing")
        print("European Call Price = ", call_price)
        print("European Put Price = ", put_price)
        print("**********************************")
    def calculate_american(self,strike_price):
        call_price = 0
        for scenario in self.scenarios:
            call_price += scenario[0] * self.call_payoff(scenario[1], strike_price)
        call_price /= ((1+self.r)**(self.depth))
        print("**********************************")
        print("American Option Pricing")
        print("American Call Price = ", call_price)
        print("American Put Price = ", self.tree_walk_helper(self.root, self.put_payoff, strike_price))
        print("**********************************")
    def calculate_custom(self,strike_price):
        print("**********************************")
        print("Custom Option Pricing")
        print("Custom Price = ", self.tree_walk_helper(self.root, self.custom_payoff, strike_price))
        print("**********************************")

    def tree_walk_helper(self, curr_node, payoff_func, strike_price):
        if len(curr_node.children) == 0:
            return payoff_func(curr_node.get_price(), strike_price)
        expected_val_of_node = 0
        storage = []
        for child in curr_node.children:
            child_value = self.tree_walk_helper(child, payoff_func, strike_price)
            child_p_val = child.get_p_val()
            addition = (child_value * child_p_val) / (1+self.r)
            storage.append([child_value, child_p_val, addition])
            expected_val_of_node += (child_value * child_p_val) / (1+self.r)
        print("Tree Walk -> Node: ", curr_node.row, curr_node.index)
        print("expected value of the node calculation = ")
        for child in storage:
            print("child_value =", child[0])
            print("child_p_val =", child[1])
            print("part_contributed =", child[2])
            print("part_contributed = (child_value * child_p_val) / (1+self.r)\n")
        print("$$$$$$$$$$$$$$$$$$$$")
        cur_val_of_node = payoff_func(curr_node.get_price(), strike_price)
        return max(cur_val_of_node, expected_val_of_node)

    def label(self):
        row = 0 
        index = 0
        q = [self.root, "sentinal"]
        while len(q) > 0:
            curr_node = q.pop(0)

            if curr_node == "sentinal":
                row +=1
                index = 0
                if len(q) != 0:
                    q.append("sentinal")
            else:
                curr_node.row = row
                curr_node.index = index
                index +=1
                for child in curr_node.children:
                    q.append(child)
        
    def solve(self):
        depth = 0
        curr_node = self.root
        while len(curr_node.children) > 0:
            curr_node = curr_node.children[0]
            depth += 1
        for _ in range(depth+1):
            self.solve_for_p_vals_off_others()
            self.solve_for_p_vals_off_price()
            self.solve_for_price_off_p_val()

    def solve_for_p_vals_off_others(self):
        q =[self.root]
        while len(q) != 0:
            curr_node = q.pop(0)
            if curr_node.parent != None:
                unkown_p_count = 0
                index_of_unkown = 0
                sum_of_other_p_vals = 0
                for index, child in enumerate(curr_node.parent.children):
                    if child.get_p_val() == -1:
                        unkown_p_count += 1
                        index_of_unkown = index
                    else:
                        sum_of_other_p_vals += child.get_p_val()
                if unkown_p_count == 1:
                    curr_node.parent.children[index_of_unkown].p_val = 1 - sum_of_other_p_vals
            for child in curr_node.children:
                q.append(child)

    def solve_for_p_vals_off_price(self):
        q =[self.root]
        while len(q) != 0:
            curr_node = q.pop(0)
            if curr_node.parent != None:
                if curr_node.get_p_val() != -1: continue
                missing_price = False
                parent_price = curr_node.parent.get_price()
                for i, child in enumerate(curr_node.parent.children):
                    if child.get_price() == -1:
                        missing_price = True
                    if i == 0:
                        u = (child.get_price()-parent_price)/parent_price
                    if i == 1:
                        d = (child.get_price()-parent_price)/parent_price
                if missing_price: continue
                print("Solve for p_val off of price, node:", curr_node.row, curr_node.index)
                curr_node.parent.children[0].p_val = solve_for_p(self.r,u,d)
                curr_node.parent.children[1].p_val = 1 - curr_node.parent.children[0].p_val
            for child in curr_node.children:
                q.append(child)

    def solve_for_price_off_p_val(self):
        q =[self.root]
        while len(q) > 0:
            curr_node = q.pop(0)
            if curr_node.parent == None: 
                for child in curr_node.children:
                    q.append(child)
                continue
            missing_p_val = False
            missing_u = False
            missing_d = False
            for i, child in enumerate(curr_node.parent.children): 
                if child.get_p_val() == -1:
                    missing_p_val = True
                if child.get_price() == -1: 
                    if i == 0: missing_u = True
                    if i == 1: missing_d = True
            if (missing_p_val) or (missing_u and missing_d) or (not missing_u and not missing_d): 
                for child in curr_node.children:
                    q.append(child)
                continue

            parent_price = curr_node.parent.get_price()
            p = curr_node.parent.children[0].get_p_val()
            if missing_u and not missing_d:
                print("Solve for u off of p_val and d:", curr_node.row, curr_node.index)
                d = (curr_node.parent.children[1].get_price() - parent_price) / parent_price
                curr_node.parent.children[0].price = (solve_for_u(p, self.r, d) + 1) * parent_price
            if not missing_u and missing_d:
                print("Solve for d off of p_val and u:", curr_node.row, curr_node.index)
                u = (curr_node.parent.children[0].get_price() - parent_price) / parent_price
                curr_node.parent.children[1].price = (solve_for_d(p, self.r, u) + 1) * parent_price
            for child in curr_node.children:
                q.append(child)

    def print_welcome_mess(self):
        print("-------------------------------------")
        print("Welcome to option pricing tool")
        print("-------------------------------------")
    
    def get_r(self):
        self.r = float(input("What is r?"))

    def custom_payoff(self, stock_price, strike_price):
        return max(0, stock_price - strike_price)**2

    def call_payoff(self, stock_price=-1, strike_price = -1):
        return max(0, stock_price-strike_price)
    
    def put_payoff(self, stock_price=-1, strike_price = -1):
        return max(0, strike_price-stock_price)

    # def select_custom_option(self):
    #     print("Would you like to input a derivative?")
    #     yes,no = yes_no()
    #     if no:
    #         self.custom_payoff = None
    #         return
    #     print("Define what you would like the payoff function to be.")
    #     print("Use stock_price, strike_price.")
    #     payoff_string = input()
    #     custom_payoff = "def custom_payoff(stock_price=-1, strike_price = -1):\n\treturn"+ payoff_string
    #     exec(custom_payoff)
    #     self.custom_payoff = custom_payoff




tree = Tree()

