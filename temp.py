def solve_for_p(r,u,d):
    if r == -1 or u == -1 or d == -1: return -1
    print("(r-d)/(u-d)")
    print("=",(r-d)/(u-d))
    return (r-d)/(u-d)

#p = (r-d)/(u-d)
u = .09524
d = -.038
r = .0194
print(solve_for_p(r,u,d))
u = .0555555555555
d = .002777777
print(solve_for_p(r,u,d))
u = .05
d = -.1
r = .03
print(solve_for_p(r,u,d))

