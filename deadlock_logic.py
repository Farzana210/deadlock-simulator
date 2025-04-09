def can_run(req, avail):
    return all(req[i] <= avail[i] for i in range(len(avail)))

def check_deadlock(allocation, request_, available):
    n = len(allocation)
    finished = [False] * n
    safe_sequence = []

    while True:
        ran = False
        for i in range(n):
            if not finished[i] and can_run(request_[i], available):
                available = [available[j] + allocation[i][j] for j in range(len(available))]
                finished[i] = True
                safe_sequence.append(f"P{i}")
                ran = True
        if not ran:
            break

    return {
        "safe": all(finished),
        "sequence": safe_sequence
    }

def bankers_algorithm(allocation, max_need, available):
    n = len(allocation)
    m = len(available)
    finish = [False] * n
    work = available.copy()
    safe_sequence = []

    while True:
        ran = False
        for i in range(n):
            if not finish[i]:
                need = [max_need[i][j] - allocation[i][j] for j in range(m)]
                if all(need[j] <= work[j] for j in range(m)):
                    work = [work[j] + allocation[i][j] for j in range(m)]
                    finish[i] = True
                    safe_sequence.append(f"P{i}")
                    ran = True
        if not ran:
            break

    return {
        "safe": all(finish),
        "sequence": safe_sequence
    }
