def compact_list_repr(l):
    ret = []
    for i, v in enumerate(l):
        if i == 0 or ret[-1][1] != v:
            ret.append([1, v])
            continue
        ret[-1][0] += 1
    return '[' + ', '.join('%d * %s' % (p[0], p[1]) for p in ret) + ']'
