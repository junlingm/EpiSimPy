import math


def ODE(N, I_0, beta, lambd, gamma, T, dt):

    dg = lambda x: math.exp(lambd * (x - 1)) * lambd
    ddg = lambda x: math.exp(lambd * (x - 1)) * lambd ** 2

    x = 1
    y = I_0 / N
    S = N - I_0
    totals = [S]
    freq = 1 / dt
    count = 0
    while count < T * freq + 1:
        x += -beta * y * dt
        y += (-beta * y - gamma * y + beta * y * ddg(x) / dg(1)) * dt
        S += -beta * y * dg(x) * N * dt
        count += 1
        if count % freq == 0:
            totals.append(S)
    return totals
