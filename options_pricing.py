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
    return (r-d)/(u-d)

def solve_for_u(p,r,d):
    if p == -1 or r == -1 or d == -1: return -1
    #p(u-d) = (r-d)
    #(u-d) = (r-d)/p
    #u = ((r-d)/p) + d
    return ((r-d)/p) + d

def solve_for_d(p,r,u):
    if p == -1 or r == -1 or u == -1: return -1
    #p(u-d) = (r-d)
    #(u-d) = (r-d)/p
    #(u-d) = (r/p)-(d/p)
    #u = (r/p)-(d/p)+d
    #u+(r/p) = d-(d/p)
    #u+(r/p) = d*(1-(1/p))
    #(u+(r/p))/(1-(1/p)) = d
    return (u+(r/p))/(1-(1/p))

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
        self.custom_payoff = None
        self.root = None
        self.print_welcome_mess()
        self.select_custom_option()
        self.get_r()
        self.root = Node()
        print_tree(self.root)
    
    def solve_for_p_vals_off_others(self):
        q =[self.root]
        while len(q) != 0:
            curr_node = q.pop(0)
            if curr_node.parent != None:
                unkown_p_count = 0
                sum_of_other_p_vals = 0
                for child in curr_node.parent.children:
                    if child.get_p_val() == -1:
                        unkown_p_count += 1
                    else:
                        sum_of_other_p_vals += child.get_p_val()
                if unkown_p_count == 1:
                    curr_node.p_val = 1 - sum_of_other_p_vals
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
                curr_node.parent.children[0].p_val = solve_for_p(self.r,u,d):
                curr_node.parent.children[1].p_val = 1 - curr_node.parent.children[0].p_val
            for child in curr_node.children:
                q.append(child)

    def solve_for_price_off_p_val(self):
        q =[self.root]
        while len(q) != 0:
            curr_node = q.pop(0)
            if curr_node.parent == None: continue
            missing_p_val = False
            missing_u = False
            missing_d = False
            for i, child in enumerate(curr_node.parent.children): 
                if child.get_p_val() == -1:
                    missing_p_val = True
                if child.get_price() == -1: 
                    if i == 0: missing_u = True
                    if i == 1: missing_d = True
            if missing_p_val: continue
            if missing_u and missing_d: continue
            if not missing_u and not missing_d: continue

            parent_price = curr_node.parent.get_price()
            p = curr_node.parent.get_p_val()
            if missing_u and not missing_d:
                d = (curr_node.parent.children[1].get_price() - parent_price) / parent_price
                curr_node.parent.children[0].price = solve_for_u(p, self.r, d)
            if not missing_u and missing_d:
                u = (curr_node.parent.children[0].get_price() - parent_price) / parent_price
                curr_node.parent.children[1].price = solve_for_d(p, self.r, u):
            for child in curr_node.children:
                q.append(child)

    def print_welcome_mess(self):
        print("-------------------------------------")
        print("Welcome to option pricing tool")
        print("-------------------------------------")

    def select_custom_option(self):
        print("Would you like to input a derivative?")
        yes,no = yes_no()
        if no:
            self.custom_payoff = None
            return
        print("Define what you would like the payoff function to be.")
        print("Use stock_price, strike_price.")
        payoff_string = input()
        custom_payoff = "def custom_payoff(stock_price=-1, strike_price = -1):\n\treturn"+ payoff_string
        exec(custom_payoff)
        self.custom_payoff = custom_payoff
    
    def get_r():
        self.r = float(input("What is r?"))

    def call_payoff(self, stock_price=-1, strike_price = -1):
        return max(0,stock_price-strike_price)
    
    def put_payoff(self, stock_price=-1, strike_price = -1):
        return max(0,strike_price-stock_price)





tree = Tree()
