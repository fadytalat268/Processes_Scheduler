DECIMAL = int()


def First_Come_First_Serve(Processes, Proc_Num, X, Y):
    global DECIMAL
    DECIMAL = X
    STEP = Y
    # arrange processes according to arrival time
    for i in range(0, Proc_Num - 1):
        for j in range(Proc_Num - i - 1):
            if float(Processes[j]['Arrival_Time']) > float(Processes[j + 1]['Arrival_Time']):
                tmp = Processes[j]
                Processes[j] = Processes[j + 1]
                Processes[j + 1] = tmp

    # adjust the start and finish of each process for the gantt chart
    start = float(Processes[0]['Arrival_Time'])
    P_Q = [dict(Task=Processes[0]['Task'], Time_Slots=[(start, float(Processes[0]['Burst_Time']))])]
    for i in range(1, Proc_Num):
        if (float(P_Q[i - 1]['Time_Slots'][0][0]) + float(P_Q[i - 1]['Time_Slots'][0][1])) >= float(
                Processes[i]['Arrival_Time']):
            start = float(P_Q[i - 1]['Time_Slots'][0][0]) + float(P_Q[i - 1]['Time_Slots'][0][1])
            P_Q.append(
                dict(Task=Processes[i]['Task'], Time_Slots=[(start, float(Processes[i]['Burst_Time']))]))
        else:
            start = float(Processes[i]['Arrival_Time'])
            P_Q.append(
                dict(Task=Processes[i]['Task'], Start=str(start),
                     Time_Slots=[(start, float(Processes[i]['Burst_Time']))]))

    Total_time = round(float(P_Q[0]['Time_Slots'][0][0]) + float(P_Q[0]['Time_Slots'][0][1]), DECIMAL)
    for i in range(1, len(P_Q)):
        Total_time = round(
            Total_time + (float(P_Q[i]['Time_Slots'][0][0]) - Total_time) + float(P_Q[i]['Time_Slots'][0][1]), DECIMAL)

    wait_time = float(0)
    for i in range(0, Proc_Num):
        wait_time += round((float(P_Q[i]['Time_Slots'][0][0]) - float(Processes[i]['Arrival_Time'])), DECIMAL)

    Av_wait_time = round(float(wait_time), DECIMAL*2) / Proc_Num

    return [P_Q, Total_time, Av_wait_time]
