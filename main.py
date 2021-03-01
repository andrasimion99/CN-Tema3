def read_rare_matrix_file(read_file):
    try:
        f = open(read_file, "r")
        n = int(f.readline())
        f.readline()
        a = [[] for _ in range(n)]
        while True:
            line = [x for x in f.readline().split(", ")]
            if len(line) < 3:
                break
            value = float(line[0])
            row = int(line[1])
            column = int(line[2])

            ok = 1
            for pair in a[row]:
                if pair[1] == column:
                    pair[0] += value
                    ok = 0
                    break
            if ok:
                a[row].append([value, column])
        return a
    except OSError:
        print("Error while reading data!")


def read_tridiagonal_matrix_file(read_file):
    try:
        f = open(read_file, "r")
        n = int(f.readline())
        p = int(f.readline())
        q = int(f.readline())

        f.readline()
        a = [0 for _ in range(n)]
        for i in range(n):
            a[i] = float(f.readline())

        f.readline()
        b = [0 for _ in range(n - q)]
        for i in range(len(b)):
            b[i] = float(f.readline())

        f.readline()
        c = [0 for _ in range(n - p)]
        for i in range(len(c)):
            c[i] = float(f.readline())
        return a, b, c
    except OSError:
        print("Error while reading data!")


def sum_matrix(m, a, b, c):
    n = len(m)
    s = [[] for _ in range(len(m))]
    p = n - len(c)
    q = n - len(b)
    for i in range(n):
        # pair = (value, column)
        for pair in m[i]:
            column = pair[1]
            if column == q + i and i < column:
                # am element in b[i]
                s[i].append([b[i] + pair[0], column])
            elif i - p == column and i > column:
                # am element in c[i-p]
                s[i].append([c[i - p] + pair[0], column])
            elif i == column:
                s[i].append([a[i] + pair[0], column])
            else:
                s[i].append([pair[0], column])
        ok_a = 1
        ok_b = 1
        ok_c = 1
        for pair in s[i]:
            column = pair[1]
            if column == i:
                ok_a = 0
            if column == q + i and i < column:
                ok_b = 0
            if i - p == column and i > column:
                ok_c = 0
        if ok_a:
            s[i].append([a[i], i])
        if ok_b and i < n - 1:
            s[i].append([b[i], i + q])
        if ok_c and i - p >= 0:
            s[i].append([c[i - p], i - p])

    return s


def compare_matrix(a, b):
    for elem in a:
        elem.sort(key=lambda x: x[1])
    for elem in b:
        elem.sort(key=lambda x: x[1])
    return a == b


if __name__ == '__main__':
    m = read_rare_matrix_file("a.txt")
    a, b, c = read_tridiagonal_matrix_file("b.txt")
    s = sum_matrix(m, a, b, c)
    # print(s)
    sum = read_rare_matrix_file("aplusb.txt")
    print("Comparare sumei:", compare_matrix(s, sum))
