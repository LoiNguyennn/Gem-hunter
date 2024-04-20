def distribute_and_over_or(terms):
    # Hàm này áp dụng quy tắc phân phối của 'và' qua 'hoặc'
    result = [[]]
    for term in terms:
        new_result = []
        for clause in result:
            for literal in term:
                new_clause = clause.copy()
                new_clause.append(literal)
                new_result.append(new_clause)
        result = new_result
    return result

def dnf_to_cnf(dnf):
    # Biến đổi từ DNF sang CNF
    cnf = []
    for clause in distribute_and_over_or(dnf):
        cnf.append(clause)
    return cnf

# Ví dụ sử dụng hàm
dnf = [[1, 2], [-3, 4]]
cnf = dnf_to_cnf(dnf)
print("DNF:", dnf)
print("CNF:", cnf)
