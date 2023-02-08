# 第一行為所有人數
# 之後每一行: 付錢的人 付錢金額 平攤給...(人編號從 1 開始)
# ex: 1 1000 2 3 4 -> 1 先付 1000 平攤給 1, 2, 3, 4(一人 250)
TEST_DATA = '''
4
1 1000 1 2 3 4
2 500 1 2
3 70 2 3
'''
IS_PRINT_DETAIL = False
PRINT_SPACE = 9
INF = int(1e10)

sink = 0
totalPeople = 0
edges = []
capacity = []
flow = []
cost = []
distance = []
parents = []
inQueue = []

balance = []


def init_data(totalPeople):
    # 0: super source
    # totalPeople * 2 + 1: sink
    arraySize = totalPeople * 2 + 2

    global edges, capacity, flow, cost, distance, parents, inQueue
    edges = [[] for _ in range(arraySize)]
    capacity = [[0] * arraySize for _ in range(arraySize)]
    flow = [[0] * arraySize for _ in range(arraySize)]
    cost = [[0] * arraySize for _ in range(arraySize)]
    distance = [0] * arraySize
    parents = [0] * arraySize
    inQueue = [False] * arraySize


def process_input(inputData):
    global sink, edges, capacity, flow, cost, distance, parents, inQueue
    global totalPeople, balance

    inputDataSplit = inputData.strip().split('\n')
    totalPeople = int(inputDataSplit[0])
    sink = totalPeople * 2 + 1
    balance = [0] * (totalPeople + 1)  # 值為正: 最後應收回多少錢, 值為負: 最後應付出多少錢
    init_data(totalPeople)

    # 連接 super source 至各節點
    for i in range(1, totalPeople + 1):
        capacity[0][i] = INF

    # cost 紀錄轉帳次數
    for i in range(1, totalPeople + 1):
        for j in range(totalPeople + 1, totalPeople * 2 + 1):
            cost[i][j] = 1

    pay = [0] * (totalPeople + 1)  # 先付多少錢
    get = [0] * (totalPeople + 1)  # 獲得價值多少錢
    for line in inputDataSplit[1:]:
        lst = line.split(' ')
        p1 = int(lst[0])  # 先付的人
        money = int(lst[1])  # 先付的金額
        splitMoney = int(money / (len(lst) - 2))  # 平攤後每個人獲得的價值(整數)
        people = list(map(int, lst[2:]))  # 平攤給

        pay[p1] += money
        for p in people:
            get[p] += splitMoney

    # 應收: 先付 - 獲得
    for i in range(len(balance)):
        balance[i] = pay[i] - get[i]

    # 調整 super source 至各節點的 capacity
    for i in range(1, totalPeople + 1):
        if balance[i] < 0:
            capacity[0][i] = -balance[i]

    if IS_PRINT_DETAIL:
        print(f'{"pay:":>{PRINT_SPACE}}', pay)
        print(f'{"get:":>{PRINT_SPACE}}', get)
        print(f'{"balance:":>{PRINT_SPACE}}', balance)
        print()

    # 建邊
    for i in range(1, totalPeople + 1):
        edges[0].append(i)

        if balance[i] >= 0:
            edges[i + totalPeople].append(sink)
            capacity[i + totalPeople][sink] = balance[i]
            continue

        for j in range(totalPeople + 1, totalPeople * 2 + 1):
            if i + totalPeople != j:
                edges[i].append(j)
                capacity[i][j] = -balance[i]

    if IS_PRINT_DETAIL:
        print(f'{"capacity:":>{PRINT_SPACE}}')
        for i in capacity:
            print(' ' * PRINT_SPACE, i)

        print(f'{"edges:":>{PRINT_SPACE}}')
        for i in edges:
            print(' ' * PRINT_SPACE, i)


def SPFA():
    global sink, edges, capacity, flow, cost, distance, parents, inQueue

    distance = [INF] * len(distance)
    distance[0] = 0

    inQueue = [False] * len(inQueue)

    que = [0]
    inQueue[0] = True

    while que:
        u = que.pop(0)
        inQueue[u] = False

        for v in edges[u]:
            if capacity[u][v] > flow[u][v] and distance[u] + cost[u][v] < distance[v]:
                distance[v] = distance[u] + cost[u][v]
                parents[v] = u
                if not inQueue[v]:
                    que.append(v)
                    inQueue[v] = True
            if flow[v][u] > 0 and distance[u] + (-cost[v][u] < distance[v]):
                distance[v] = distance[u] + (-cost[v][u])
                parents[v] = u
                if not inQueue[v]:
                    que.append(v)
                    inQueue[v] = True

    return distance[sink] != INF


def augment(u, v, bottleNeck):
    global parents, capacity, flow

    if v == 0:
        return bottleNeck
    bottleNeck = augment(parents[u], u, min(capacity[u][v] - flow[u][v], bottleNeck))
    flow[u][v] += bottleNeck
    flow[v][u] -= bottleNeck
    return bottleNeck


def MCMF():
    global edges, capacity, flow, cost, distance, parents, inQueue, sink
    global totalPeople, balance

    times = 0
    while SPFA():
        augment(parents[sink], sink, INF)
        times += 1

    for i, bal in enumerate(balance[1:]):
        pay, get = 0, 0
        if bal < 0:
            pay = -bal
        elif bal > 0:
            get = bal
        print(f'{i + 1:2} 號應付 {pay:4} 元，應得 {get:4} 元')

    print('\n最少轉帳次數:', times)
    for i in range(totalPeople + 1, totalPeople * 2 + 1):
        for j in range(1, totalPeople + 1):
            if flow[i][j] < 0:
                print(f'{j:2} 號需給 {i - totalPeople:2} 號 {-flow[i][j]:4} 元')


def main():
    process_input(TEST_DATA)
    MCMF()


if __name__ == '__main__':
    main()
