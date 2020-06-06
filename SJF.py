from copy import deepcopy

DECIMAL = int()


def Get_Total_BurstTime(List):
    time = float(List[0]['Start']) + float(List[0]['Burst_Time'])
    for i in range(1, len(List)):
        time = time + (float(List[i]['Start']) - time) + float(List[i]['Burst_Time'])

    return round(time, DECIMAL)


def SJF_Sort(List):
    # arrange processes according to arrival time and if equal arrival time then arranged according to burst time
    for i in range(len(List) - 1):
        for j in range(len(List) - 1 - i):
            if float(List[j]['Arrival_Time']) > float(List[j + 1]['Arrival_Time']):
                tmp = List[j]
                List[j] = List[j + 1]
                List[j + 1] = tmp
            elif float(List[j]['Arrival_Time']) == float(List[j + 1]['Arrival_Time']):
                if float(List[j]['Burst_Time']) > float(List[j + 1]['Burst_Time']):
                    tmp = List[j]
                    List[j] = List[j + 1]
                    List[j + 1] = tmp
    return List


def SJF_Adj(List, burst_time):
    for i in range(len(List)):
        if float(List[i]['Arrival_Time']) <= burst_time:
            List[i].update({'Start': str(burst_time)})
        else:
            List[i].update({'Start': List[i]['Arrival_Time']})

    for i in range(len(List) - 1):
        for j in range(len(List) - 1 - i):
            if float(List[j]['Start']) > float(List[j + 1]['Start']):
                tmp = List[j]
                List[j] = List[j + 1]
                List[j + 1] = tmp
            elif float(List[j]['Start']) == float(List[j + 1]['Start']):
                if float(List[j]['Burst_Time']) > float(List[j + 1]['Burst_Time']):
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


def SJF_Non_Preemptive(Processes, Proc_Num, X, Y):
    global DECIMAL
    DECIMAL = X
    STEP = Y
    # arrange processes according to arrival time and if equal arrival time then arranged according to burst time
    Processes = SJF_Sort(Processes)
    Processes[0].update({'Start': Processes[0]['Arrival_Time']})

    b_ref = round(float(Processes[0]['Start']) + float(Processes[0]['Burst_Time']), DECIMAL)
    for i in range(1, Proc_Num):
        Processes[i:] = SJF_Adj(Processes[i:], b_ref)
        if b_ref >= float(Processes[i]['Start']):
            b_ref = round(b_ref + float(Processes[i]['Burst_Time']), DECIMAL)
        else:
            b_ref = round(float(Processes[i]['Start']) + float(Processes[i]['Burst_Time']), DECIMAL)

    Total_time = Get_Total_BurstTime(Processes)

    # adjust the start and finish of each process for the gantt chart
    P_Q = []
    for i in range(0, Proc_Num):
        P_Q.append(
            dict(Task=Processes[i]['Task'],
                 Time_Slots=[(round(float(Processes[i]['Start']), DECIMAL), round(float(Processes[i]['Burst_Time']), DECIMAL))]))

    # average waiting time
    wait_time = 0
    for i in range(0, Proc_Num):
        wait_time += round(float(Processes[i]['Start']), DECIMAL) - round(float(Processes[i]['Arrival_Time']), DECIMAL)
    Av_wait_time = round(float(wait_time), DECIMAL*2) / Proc_Num

    return [P_Q, Total_time, Av_wait_time]


def SJF_Preemptive(Processes, Proc_Num, X, Y):
    global DECIMAL
    DECIMAL = X
    STEP = Y
    # arrange processes according to arrival time and if equal arrival time then arranged according to burst time
    Processes = SJF_Sort(Processes)
    Remove_Zero_Burst(Processes)
    P_cpy = deepcopy(Processes)
    timer = round(float(Processes[0]['Arrival_Time']) + float(STEP), DECIMAL)
    Q = [dict(Task=Processes[0]['Task'], Start=Processes[0]['Arrival_Time'], Burst_Time=str(STEP))]
    Processes[0]['Burst_Time'] = str(round(float(Processes[0]['Burst_Time']) - STEP, DECIMAL))
    Remove_Zero_Burst(Processes)
    while len(Processes) > 0:
        Processes = SJF_Adj(Processes, round(timer, DECIMAL))
        if round(float(Processes[0]['Start']), DECIMAL) == round(timer, DECIMAL):
            if Processes[0]['Task'] == Q[-1]['Task']:
                Q[-1]['Burst_Time'] = str(round(float(Q[-1]['Burst_Time']) + STEP, DECIMAL))
            else:
                Q.append(dict(Task=Processes[0]['Task'], Start=str(timer), Burst_Time=str(STEP)))
            Processes[0]['Burst_Time'] = str(round(float(Processes[0]['Burst_Time']) - STEP, DECIMAL))

        timer += STEP
        Remove_Zero_Burst(Processes)
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
            P_Q.append(dict(Task=Q[i]['Task'], Time_Slots=[(round(float(Q[i]['Start']), DECIMAL), round(float(Q[i]['Burst_Time']), DECIMAL))]))
        else:
            P_Q[Indx]['Time_Slots'].append((round(float(Q[i]['Start']), DECIMAL), round(float(Q[i]['Burst_Time']), DECIMAL)))
            Indx = -1

    wait_time = 0
    for i in range(0, len(P_cpy)):
        for j in range(0, len(P_Q)):
            if P_Q[j]['Task'] == P_cpy[i]['Task']:
                wait_time += round(float(P_Q[j]['Time_Slots'][-1][0]) + float(P_Q[j]['Time_Slots'][-1][1]) - float(
                    P_cpy[i]['Arrival_Time']) - float(P_cpy[i]['Burst_Time']), DECIMAL)
                break

    Av_wait_time = round(float(wait_time), DECIMAL * 2) / Proc_Num

    return [P_Q, Total_time, Av_wait_time]
