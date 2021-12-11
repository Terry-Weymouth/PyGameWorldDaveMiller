
def add_points(p1, p2):
    ret_point_list = []
    for i in range(len(p1)):
        n1 = p1[i]
        n2 = p2[i]
        ret_point_list.append(n1 + n2)
    return tuple(ret_point_list)
