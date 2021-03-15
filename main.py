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
        # pair = [value, column]
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


def product_matrix(m, a, b, c):
    n = len(m)
    s = [[] for _ in range(len(m))]
    p = n - len(c)
    q = n - len(b)
    for i in range(n):
        for j in range(n):
            # print("j:", j)
            sum = 0
            for pair in m[i]:

                column = pair[1]
                value = pair[0]
                # print("for:", column, pair[0])
                # verificam daca exista element in matricea B pe coloana = j si linia = column
                if j == q + column and column < j:
                    # am element in b[column]
                    sum += value * b[column]
                    # print("b:", value, "*", b[column])
                elif column - p == j and column > j:
                    # am element in c[column-p]
                    sum += value * c[column - p]
                    # print("c:", value, "*", c[column - p])
                elif column == j:
                    sum += value * a[column]
                    # print("a", value, "*", a[column])
            if sum != 0:
                s[i].append([sum, j])

    return s


def compare_matrix(a, b):
    for elem in a:
        elem.sort(key=lambda x: x[1])
    for elem in b:
        elem.sort(key=lambda x: x[1])
    return a == b


def tridiagonal_product(a, b, c, x, y, z):
    n = len(a)
    p1 = n - len(c)
    q1 = n - len(b)
    p2 = n - len(z)
    q2 = n - len(y)
    product = [[] for _ in range(n)]
    for i in range(n):
        print("linia:", i)
        print("a:", a[i])
        if p1 <= i <= n - 1:
            # elem de pe linia i
            print("c:", c[i - p1])
        if 0 <= i <= n - q1 - 1:
            print("b:", b[i])
        for j in range(n):
            s = 0
            print("coloana:", j)
            print("x:", x[j])
            if 0 <= j <= n - p2 - 1:
                # elem de pe col j
                print("z:", z[j])
            if q2 <= j <= n - 1:
                print("y:", y[j - q2])
            product[i].append([s, j])


if __name__ == '__main__':
    m = read_rare_matrix_file("a.txt")
    a, b, c = read_tridiagonal_matrix_file("b.txt")

    # s = sum_matrix(m, a, b, c)
    # sum = read_rare_matrix_file("aplusb.txt")
    # print("Comparare sumei:", compare_matrix(s, sum))
    #
    # p = product_matrix(m, a, b, c)
    # prod = read_rare_matrix_file("aorib.txt")
    # print("Comparare produsului:", compare_matrix(p, prod))

    d, e, f = read_tridiagonal_matrix_file("c.txt")
    x, y, z = read_tridiagonal_matrix_file("d.txt")
    print(d, e, f)
    print(x, y, z)
    tridiagonal_product(d, e, f, x, y, z)
