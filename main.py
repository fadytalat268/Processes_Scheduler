from Round_Robin import RoundRobin
from SJF import SJF_Preemptive, SJF_Non_Preemptive
from FCFS import First_Come_First_Serve
from Priority import Priority_Preemptive, Priority_Non_Preemptive
from Gantt_Chart import *
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk


def Set_Decimal_Step(x):
    global DECIMAL
    global STEP
    DECIMAL = x
    if DECIMAL == 0:
        STEP = 1
    else:
        STEP = 1.0 / (10 ** DECIMAL)


def Capture_inputs(List):
    Input = []
    for i in range(0, len(List[0])):
        if List[0][i]['text'] == "Task":
            continue
        else:
            if len(List) == 4:
                Input.append(dict(Task=List[0][i]['text'], Arrival_Time=str(float(List[1][i].get())),
                                  Burst_Time=str(float(List[2][i].get())), Priority=str(int(List[3][i].get()))))
            elif len(List) == 3:
                Input.append(
                    dict(Task=List[0][i]['text'], Arrival_Time=str(float(List[1][i].get())),
                         Burst_Time=str(float(List[2][i].get()))))

    return Input


def Output_Window(x, Sched_type, List, Proc_num, quantum_time):
    out_list = []
    if Sched_type == "FCFS":
        out_list = First_Come_First_Serve(List, Proc_num, DECIMAL, STEP)

    elif Sched_type == "SJF Preemptive":
        out_list = SJF_Preemptive(List, Proc_num, DECIMAL, STEP)

    elif Sched_type == "SJF Non-Preemptive":
        out_list = SJF_Non_Preemptive(List, Proc_num, DECIMAL, STEP)

    elif Sched_type == "Priority Preemptive":
        out_list = Priority_Preemptive(List, Proc_num, DECIMAL, STEP)

    elif Sched_type == "Priority Non-Preemptive":
        out_list = Priority_Non_Preemptive(List, Proc_num, DECIMAL, STEP)

    elif Sched_type == "Round Robin":
        out_list = RoundRobin(List, Proc_num, float(quantum_time), DECIMAL, STEP)

    Draw_GanttChart(out_list[0], float(out_list[1]))

    x.destroy()
    output = Toplevel()
    output.title('RESULTS')
    photo = PhotoImage(file="fig1.png")
    photo_label = Label(output, image=photo)
    photo_label.grid(row=0, padx=10, pady=10)
    average_wait = Label(output, text=str("Average Wait Time : " + str(out_list[2])))
    average_wait.grid(row=10, column=0, columnspan=3, padx=10, pady=10)
    done = Button(output, text="DONE",
                  command=lambda: [output.destroy(), root.deiconify()])

    done.grid(row=11, column=0, columnspan=2, pady=15)
    canvas = Canvas(output, width=1500, height=600)
    canvas.pack()
    canvas.create_image(20, 20, anchor=NW, image=photo)


def Input_Window(Sched_type, Proc_num):
    global types
    if (Sched_type in types) and (Proc_num > 0):
        inputs = Tk()
        inputs.title('INPUTS')
        Components = []
        labels = []
        arrival_time = []
        burst_time = []
        priority = []
        for i in range(0, Proc_num):
            if (i % 15) == 0:
                labels.append(Label(inputs, text="Task"))
                arrival_time.append(Label(inputs, text="Arrival Time"))
                burst_time.append(Label(inputs, text="Burst Time"))
                if "Priority" in Sched_type:
                    priority.append(Label(inputs, text=" Priority "))
            labels.append(Label(inputs, text=str('P' + str(i))))
            arrival_time.append(
                Spinbox(inputs, justify='center', increment=STEP, from_=0, to=1000, wrap=True, state='readonly',
                        width=10))
            burst_time.append(
                Spinbox(inputs, justify='center', increment=STEP, from_=STEP, to=1000, wrap=True, state='readonly',
                        width=10))
            if "Priority" in Sched_type:
                priority.append(
                    Spinbox(inputs, justify='center', from_=1, to=1000, wrap=True, state='readonly',
                            width=10))

        Components.append(labels)
        Components.append(arrival_time)
        Components.append(burst_time)
        if "Priority" in Sched_type:
            Components.append(priority)

        for j in range(0, len(labels)):
            Components[0][j].grid(row=int(j % 16), column=0 + (int(j / 16) * len(Components)), padx=5, pady=10)
            Components[1][j].grid(row=int(j % 16), column=1 + (int(j / 16) * len(Components)), padx=5, pady=5)
            Components[2][j].grid(row=int(j % 16), column=2 + (int(j / 16) * len(Components)), padx=5, pady=5)
            if "Priority" in Sched_type:
                Components[3][j].grid(row=int(j % 16), column=3 + (int(j / 16) * len(Components)), padx=5, pady=5)

        Q_t_label = Label(inputs, text="Quantum Time")
        Q_t = Spinbox(inputs, justify='center', increment=STEP, from_=STEP, to=1000, wrap=True, state='readonly',
                      width=10)
        if Sched_type == "Round Robin":
            Q_t_label.grid(row=16, column=0, columnspan=2, pady=15)
            Q_t.grid(row=16, column=2, columnspan=2, pady=15)

        done = Button(inputs, text="DONE",
                      command=lambda: [
                          Output_Window(inputs, Sched_type, Capture_inputs(Components), Proc_num, Q_t.get())])

        done.grid(row=17, column=0, columnspan=2, pady=15)

        back = Button(inputs, text="BACK", command=lambda: [inputs.destroy(), root.deiconify()])
        back.grid(row=17, column=2, columnspan=2, pady=15)
    else:
        root.deiconify()


root = Tk()
root.title('MAIN MENU')
types = ["FCFS", "SJF Preemptive", "SJF Non-Preemptive", "Priority Preemptive",
         "Priority Non-Preemptive", "Round Robin"]
DECIMAL = int()
STEP = float()
wlc = Label(root, text="WELCOME")
scheduler = Label(root, text="Scheduler :")
scheduler_list = Combobox(root, justify='center', value=types, state='readonly')
scheduler_list.current(0)
num_label = Label(root, text="Number of Processes :")
num_entry = Spinbox(root, justify='center', from_=1, to=1000, wrap=True, state='readonly')
dec_label = Label(root, text="Number of Decimals :")
dec_entry = Spinbox(root, justify='center', from_=0, to=8, wrap=True, state='readonly')
Next = Button(root, text="NEXT",
              command=lambda: [root.withdraw(), Set_Decimal_Step(int(dec_entry.get())),
                               Input_Window(scheduler_list.get(), int(num_entry.get()))])
wlc.grid(row=0, columnspan=2, pady=15)

scheduler.grid(row=1, padx=10, sticky=W, pady=10)
scheduler_list.grid(row=1, column=1, padx=10, sticky=W, pady=10)

num_label.grid(row=2, padx=10, sticky=W, pady=10)
num_entry.grid(row=2, column=1, padx=10, sticky=W, pady=10)

dec_label.grid(row=3, padx=10, sticky=W, pady=10)
dec_entry.grid(row=3, column=1, padx=10, sticky=W, pady=10)

Next.grid(row=4, columnspan=2, pady=15)

root.mainloop()
