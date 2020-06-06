DECIMAL = int()
from copy import deepcopy


def Get_Total_BurstTime(List):
    time = float(List[0]['Start']) + float(List[0]['Burst_Time'])
    for i in range(1, len(List)):
        time = time + (float(List[i]['Start']) - time) + float(List[i]['Burst_Time'])

    return round(time, DECIMAL)


def RR_Sort(List):
    # arrange processes according to arrival time
    for i in range(len(List) - 1):
        for j in range(len(List) - 1 - i):
            if float(List[j]['Arrival_Time']) > float(List[j + 1]['Arrival_Time']):
                tmp = List[j]
                List[j] = List[j + 1]
                List[j + 1] = tmp

    return List


def Remove_Zero_Burst(List):
    x = 0
    while x < len(List):
        if round(float(List[x]['Burst_Time']), DECIMAL) == 0.0:
            del List[x]
        else:
            x += 1


def Ready_Q_Adj(R_Q, List, time):
    x = 0
    while x < len(List):
        if round(float(List[x]['Arrival_Time']), DECIMAL) <= round(time, DECIMAL):
            R_Q.append(List.pop(x))
            # R_Q.insert(0,List.pop(x))
        else:
            x += 1


def RoundRobin(Processes, Proc_Num, Time_Quantum, X, Y):
    global DECIMAL
    DECIMAL = X
    STEP = Y
    Processes = RR_Sort(Processes)
    Remove_Zero_Burst(Processes)
    Time_Quantum = round(Time_Quantum, DECIMAL)
    P_cpy = deepcopy(Processes)
    timer = round(float(Processes[0]['Arrival_Time']), DECIMAL)
    Ready_Q = []
    Q = []

    while (len(Processes) > 0) or (len(Ready_Q) > 0):
        Ready_Q_Adj(Ready_Q, Processes, round(timer, DECIMAL))
        if len(Ready_Q) == 0:
            timer += STEP
        else:
            if round(float(Ready_Q[0]['Burst_Time']), DECIMAL) >= Time_Quantum:
                Q.append(dict(Task=Ready_Q[0]['Task'], Start=str(timer), Burst_Time=str(Time_Quantum)))
                Ready_Q[0]['Burst_Time'] = str(round(float(Ready_Q[0]['Burst_Time']) - Time_Quantum, DECIMAL))
                timer += Time_Quantum
                tmp = Ready_Q.pop(0)
                Ready_Q_Adj(Ready_Q, Processes, round(timer, DECIMAL))
                Ready_Q.append(tmp)

            elif float(Ready_Q[0]['Burst_Time']) < Time_Quantum:
                Q.append(dict(Task=Ready_Q[0]['Task'], Start=str(timer), Burst_Time=Ready_Q[0]['Burst_Time']))
                timer += round(float(Ready_Q[0]['Burst_Time']), DECIMAL)
                Ready_Q[0]['Burst_Time'] = str(0)
                Ready_Q_Adj(Ready_Q, Processes, round(timer, DECIMAL))
                Ready_Q.append(Ready_Q.pop(0))

        Remove_Zero_Burst(Ready_Q)

    Total_time = Get_Total_BurstTime(Q)
    # adjust the start and finish of each process for the gantt chart
    P_Q = []
    Indx = -1
    for i in range(0, len(Q)):
        for j in range(0, len(P_Q)):
            if Q[i]['Task'] == P_Q[j]['Task']:
                Indx = j
                break

        if Indx == -1:
            P_Q.append(dict(Task=Q[i]['Task'],
                            Time_Slots=[
                                (round(float(Q[i]['Start']), DECIMAL), round(float(Q[i]['Burst_Time']), DECIMAL))]))
        else:
            P_Q[Indx]['Time_Slots'].append(
                (round(float(Q[i]['Start']), DECIMAL), round(float(Q[i]['Burst_Time']), DECIMAL)))
            Indx = -1

    print('P_Q :', P_Q)
    print('Q :', Q)
    print('P_cpy :', P_cpy)

    wait_time = 0
    for i in range(0, len(P_cpy)):
        for j in range(0, len(P_Q)):
            if P_Q[j]['Task'] == P_cpy[i]['Task']:
                wait_time += round(float(P_Q[j]['Time_Slots'][-1][0]) + float(P_Q[j]['Time_Slots'][-1][1]) - float(
                    P_cpy[i]['Arrival_Time']) - float(P_cpy[i]['Burst_Time']), DECIMAL)
                break

    Av_wait_time = round(float(wait_time), DECIMAL * 2) / Proc_Num

    return [P_Q, Total_time, Av_wait_time]
