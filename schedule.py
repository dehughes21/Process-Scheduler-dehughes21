import random


def getNumProcs(fname):
    i = 0
    with open(fname, 'r') as file:
        for line in file:
            i += 1
    return i


def getSchedule(file):
    alg = input("Which algorithm (fcfs, stcf, sjf, rr)? ")
    if alg == "fcfs":
        class FCFS:
            def processData(self, fname):
                process_data = []
                bursts = {}
                with open(fname, 'r') as data:
                    for line in data:
                        line = line.split(",")
                        temporary = []
                        process_id = int(line[0])

                        arrival_time = int(line[2])

                        burst_time = int(line[3])
                        noStop = int(line[-1])

                        bursts["pid" + str(process_id)] = [int(x) for x in line[4:]]
                        if noStop == -1:
                            maxCPUbursts = int(input("Max # of CPU bursts: "))
                            bursts["pid" + str(process_id)] = [int(x) for x in line[3:]]

                        temporary.extend([process_id, arrival_time, burst_time])
                        process_data.append(temporary)
                print("BURSTS: " + str(bursts))
                print("PROCESS DATA: " + str(process_data))
                FCFS.schedulingProcess(self, process_data)

            def schedulingProcess(self, process_data):
                process_data.sort(key=lambda x: x[1])
                start_time = []
                exit_time = []
                s_time = 0
                for i in range(len(process_data)):
                    if s_time < process_data[i][1]:
                        s_time = process_data[i][1]
                    start_time.append(s_time)
                    s_time = s_time + process_data[i][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    process_data[i].append(e_time)
                t_time = FCFS.calculateTurnaroundTime(self, process_data)
                w_time = FCFS.calculateWaitingTime(self, process_data)
                FCFS.printData(self, process_data, t_time, w_time, s_time, e_time)

            def calculateTurnaroundTime(self, process_data):
                total_turnaround_time = 0
                for i in range(len(process_data)):
                    turnaround_time = process_data[i][3] - process_data[i][1]
                    '''
                    turnaround_time = completion_time - arrival_time
                    '''
                    total_turnaround_time = total_turnaround_time + turnaround_time
                    process_data[i].append(turnaround_time)
                average_turnaround_time = total_turnaround_time / len(process_data)
                '''
                average_turnaround_time = total_turnaround_time / no_of_processes
                '''
                return average_turnaround_time

            def calculateWaitingTime(self, process_data):
                total_waiting_time = 0
                for i in range(len(process_data)):
                    waiting_time = process_data[i][4] - process_data[i][2]
                    '''
                    waiting_time = turnaround_time - burst_time
                    '''
                    total_waiting_time = total_waiting_time + waiting_time
                    process_data[i].append(waiting_time)
                average_waiting_time = total_waiting_time / len(process_data)
                '''
                average_waiting_time = total_waiting_time / no_of_processes
                '''
                return average_waiting_time

            def printData(self, process_data, average_turnaround_time, average_waiting_time, start_time, end_time):

                print("Process_ID  Arrival_Time  Burst_Time  Completion_Time  Turnaround_Time  Waiting_Time")

                print(process_data)
                resSum = 0
                for x in range(len(process_data)):
                    resSum += process_data[x][5]
                resTime = resSum / len(process_data)
                print(f'Average Turnaround Time: {average_turnaround_time}')
                print("Average Response Time: " + str(resTime))
                print(f'Average Waiting Time: {average_waiting_time}')
                for i in range(len(process_data)):
                    tEnd = process_data[i][3]
                    tStart = tEnd - process_data[i][2]
                    print(str(tStart) + ":" + "pid" + str(process_data[i][0]), end=" ")
                print(" ")

        fcfs = FCFS()
        fcfs.processData(file)

    elif alg == "sjf":

        class SJF:

            def processData(self, fname):
                process_data = []
                with open(fname, 'r') as data:
                    for line in data:
                        line = line.split(",")
                        temporary = []
                        process_id = int(line[0])

                        arrival_time = int(line[2])

                        burst_time = int(line[3])
                        temporary.extend([process_id, arrival_time, burst_time, 0])
                        '''
                        '0' is the state of the process. 0 means not executed and 1 means execution complete
                        '''
                        process_data.append(temporary)
                SJF.schedulingProcess(self, process_data)

            def schedulingProcess(self, process_data):
                start_time = []
                exit_time = []
                s_time = 0
                process_data.sort(key=lambda x: x[1])
                '''
                Sort processes according to the Arrival Time
                '''
                for i in range(len(process_data)):
                    ready_queue = []
                    temp = []
                    normal_queue = []

                    for j in range(len(process_data)):
                        if (process_data[j][1] <= s_time) and (process_data[j][3] == 0):
                            temp.extend([process_data[j][0], process_data[j][1], process_data[j][2]])
                            ready_queue.append(temp)
                            temp = []
                        elif process_data[j][3] == 0:
                            temp.extend([process_data[j][0], process_data[j][1], process_data[j][2]])
                            normal_queue.append(temp)
                            temp = []

                    if len(ready_queue) != 0:
                        ready_queue.sort(key=lambda x: x[2])
                        '''
                        Sort the processes according to the Burst Time
                        '''
                        start_time.append(s_time)
                        s_time = s_time + ready_queue[0][2]
                        e_time = s_time
                        exit_time.append(e_time)
                        for k in range(len(process_data)):
                            if process_data[k][0] == ready_queue[0][0]:
                                break
                        process_data[k][3] = 1
                        process_data[k].append(e_time)

                    elif len(ready_queue) == 0:
                        if s_time < normal_queue[0][1]:
                            s_time = normal_queue[0][1]
                        start_time.append(s_time)
                        s_time = s_time + normal_queue[0][2]
                        e_time = s_time
                        exit_time.append(e_time)
                        for k in range(len(process_data)):
                            if process_data[k][0] == normal_queue[0][0]:
                                break
                        process_data[k][3] = 1
                        process_data[k].append(e_time)

                t_time = SJF.calculateTurnaroundTime(self, process_data)
                w_time = SJF.calculateWaitingTime(self, process_data)
                SJF.printData(self, process_data, t_time, w_time)

            def calculateTurnaroundTime(self, process_data):
                total_turnaround_time = 0
                for i in range(len(process_data)):
                    turnaround_time = process_data[i][4] - process_data[i][1]
                    '''
                    turnaround_time = completion_time - arrival_time
                    '''
                    total_turnaround_time = total_turnaround_time + turnaround_time
                    process_data[i].append(turnaround_time)
                average_turnaround_time = total_turnaround_time / len(process_data)
                '''
                average_turnaround_time = total_turnaround_time / no_of_processes
                '''
                return average_turnaround_time

            def calculateWaitingTime(self, process_data):
                total_waiting_time = 0
                for i in range(len(process_data)):
                    waiting_time = process_data[i][5] - process_data[i][2]
                    '''
                    waiting_time = turnaround_time - burst_time
                    '''
                    total_waiting_time = total_waiting_time + waiting_time
                    process_data[i].append(waiting_time)
                average_waiting_time = total_waiting_time / len(process_data)
                '''
                average_waiting_time = total_waiting_time / no_of_processes
                '''
                return average_waiting_time

            def printData(self, process_data, average_turnaround_time, average_waiting_time):
                process_data.sort(key=lambda x: x[4])
                for i in range(len(process_data)):
                    pid = str(process_data[i][0])

                    tArr = str(process_data[i][1])
                    if i == 0:
                        print((tArr + ":" + "pid" + pid), end=" ")
                    else:
                        tComp = str(process_data[i - 1][4])  # Gives completion time of PREVIOUS process
                        print((tComp + ":pid" + pid), end=" ")
                print(" ")
                process_data.sort(key=lambda x: x[0])
                '''
                Sort processes according to the Process ID
                '''
                print(
                    "Process_ID  Arrival_Time  Burst_Time      Completed  Completion_Time  Turnaround_Time  Waiting_Time")

                for i in range(len(process_data)):
                    for j in range(len(process_data[i])):
                        print(process_data[i][j], end="				")
                    print()

                print(f'Average Turnaround Time: {average_turnaround_time}')

                print(f'Average Waiting Time: {average_waiting_time}')

        sjf = SJF()
        sjf.processData(file)

    elif alg == "stcf":
        class STCF:

            def processData(self, fname):
                process_data = []
                with open(fname, 'r') as data:
                    for line in data:
                        line = line.split(",")
                        temporary = []
                        process_id = int(line[0])
                        arrival_time = int(line[2])
                        burst_time = int(line[3])
                        temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])
                        '''
                        '0' is the state of the process. 0 means not executed and 1 means execution complete
                        '''
                        process_data.append(temporary)
                STCF.schedulingProcess(self, process_data)

            def schedulingProcess(self, process_data):
                start_time = []
                exit_time = []
                s_time = 0
                sequence_of_process = []
                process_data.sort(key=lambda x: x[1])
                '''
                Sort processes according to the Arrival Time
                '''
                while 1:
                    ready_queue = []
                    normal_queue = []
                    temp = []
                    for i in range(len(process_data)):
                        if process_data[i][1] <= s_time and process_data[i][3] == 0:
                            temp.extend(
                                [process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                            ready_queue.append(temp)
                            temp = []
                        elif process_data[i][3] == 0:
                            temp.extend(
                                [process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                            normal_queue.append(temp)
                            temp = []
                    if len(ready_queue) == 0 and len(normal_queue) == 0:
                        break
                    if len(ready_queue) != 0:
                        ready_queue.sort(key=lambda x: x[2])
                        '''
                        Sort processes according to Burst Time
                        '''
                        start_time.append(s_time)
                        s_time = s_time + 1
                        e_time = s_time
                        exit_time.append(e_time)
                        sequence_of_process.append(ready_queue[0][0])
                        for k in range(len(process_data)):
                            if process_data[k][0] == ready_queue[0][0]:
                                break
                        process_data[k][2] = process_data[k][2] - 1
                        if process_data[k][
                            2] == 0:  # If Burst Time of a process is 0, it means the process is completed
                            process_data[k][3] = 1
                            process_data[k].append(e_time)
                    if len(ready_queue) == 0:
                        if s_time < normal_queue[0][1]:
                            s_time = normal_queue[0][1]
                        start_time.append(s_time)
                        s_time = s_time + 1
                        e_time = s_time
                        exit_time.append(e_time)
                        sequence_of_process.append(normal_queue[0][0])
                        for k in range(len(process_data)):
                            if process_data[k][0] == normal_queue[0][0]:
                                break
                        process_data[k][2] = process_data[k][2] - 1
                        if process_data[k][
                            2] == 0:  # If Burst Time of a process is 0, it means the process is completed
                            process_data[k][3] = 1
                            process_data[k].append(e_time)

                t_time = STCF.calculateTurnaroundTime(self, process_data)
                w_time = STCF.calculateWaitingTime(self, process_data)
                print(process_data)
                STCF.printData(self, process_data, t_time, w_time, sequence_of_process)

            def calculateTurnaroundTime(self, process_data):
                total_turnaround_time = 0
                for i in range(len(process_data)):
                    turnaround_time = process_data[i][5] - process_data[i][1]
                    '''
                    turnaround_time = completion_time - arrival_time
                    '''
                    total_turnaround_time = total_turnaround_time + turnaround_time
                    process_data[i].append(turnaround_time)
                average_turnaround_time = total_turnaround_time / len(process_data)
                '''
                average_turnaround_time = total_turnaround_time / no_of_processes
                '''
                return average_turnaround_time

            def calculateWaitingTime(self, process_data):
                total_waiting_time = 0
                for i in range(len(process_data)):
                    waiting_time = process_data[i][6] - process_data[i][4]
                    '''
                    waiting_time = turnaround_time - burst_time
                    '''
                    total_waiting_time = total_waiting_time + waiting_time
                    process_data[i].append(waiting_time)
                average_waiting_time = total_waiting_time / len(process_data)
                '''
                average_waiting_time = total_waiting_time / no_of_processes
                '''
                return average_waiting_time

            def printData(self, process_data, average_turnaround_time, average_waiting_time, sequence_of_process):
                process_data.sort(key=lambda x: x[0])
                '''
                Sort processes according to the Process ID
                '''
                print(
                    "Process_ID  Arrival_Time  Rem_Burst_Time      Completed  Orig_Burst_Time Completion_Time  Turnaround_Time  Waiting_Time")
                for i in range(len(process_data)):
                    for j in range(len(process_data[i])):
                        print(process_data[i][j], end="\t\t\t\t")
                    print()
                print(f'Average Turnaround Time: {average_turnaround_time}')
                print(f'Average Waiting Time: {average_waiting_time}')
                rSum = 0
                for s in range(len(process_data)):
                    PID = process_data[s][0]
                    rSum += sequence_of_process.index(PID)
                rTime_avg = rSum / len(process_data)
                print("Average Response Time: " + str(rTime_avg))
                print(f'Sequence of Process: {sequence_of_process}')
                for i in range(len(sequence_of_process)):
                    if i == 0:
                        pid = str(sequence_of_process[0])
                        print(("0:pid" + pid), end=" ")
                    elif i != 0:
                        if sequence_of_process[i] != sequence_of_process[i - 1]:
                            tComp = str(i)
                            pid = str(sequence_of_process[i])
                            print((tComp + ":pid" + pid), end=" ")
                    if i == len(sequence_of_process) - 1:
                        print("END:" + str(i))

        stcf = STCF()
        stcf.processData(file)

    elif alg == "rr":
        class RoundRobin:

            def processData(self, fname):
                process_data = []
                with open(fname, 'r') as data:
                    for line in data:
                        line = line.split(",")
                        temporary = []
                        process_id = int(line[0])

                        arrival_time = int(line[2])

                        burst_time = int(line[3])

                        temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])
                        '''
                        '0' is the state of the process. 0 means not executed and 1 means execution complete

                        '''
                        process_data.append(temporary)

                time_slice = int(input("Enter Time Slice: "))

                RoundRobin.schedulingProcess(self, process_data, time_slice)

            def schedulingProcess(self, process_data, time_slice):
                start_time = []
                exit_time = []
                executed_process = []
                ready_queue = []
                s_time = 0
                process_data.sort(key=lambda x: x[1])
                '''
                Sort processes according to the Arrival Time
                '''
                while 1:
                    normal_queue = []
                    temp = []
                    for i in range(len(process_data)):
                        if process_data[i][1] <= s_time and process_data[i][3] == 0:
                            present = 0
                            if len(ready_queue) != 0:
                                for k in range(len(ready_queue)):
                                    if process_data[i][0] == ready_queue[k][0]:
                                        present = 1
                            '''
                            The above if loop checks that the next process is not a part of ready_queue
                            '''
                            if present == 0:
                                temp.extend(
                                    [process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                                ready_queue.append(temp)
                                temp = []
                            '''
                            The above if loop adds a process to the ready_queue only if it is not already present in it
                            '''
                            if len(ready_queue) != 0 and len(executed_process) != 0:
                                for k in range(len(ready_queue)):
                                    if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                                        ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                            '''
                            The above if loop makes sure that the recently executed process is appended at the end of ready_queue
                            '''
                        elif process_data[i][3] == 0:
                            temp.extend(
                                [process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                            normal_queue.append(temp)
                            temp = []
                    if len(ready_queue) == 0 and len(normal_queue) == 0:
                        break
                    if len(ready_queue) != 0:
                        if ready_queue[0][2] > time_slice:
                            '''
                            If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                            '''
                            start_time.append(s_time)
                            s_time = s_time + time_slice
                            e_time = s_time
                            exit_time.append(e_time)
                            executed_process.append(ready_queue[0][0])
                            for j in range(len(process_data)):
                                if process_data[j][0] == ready_queue[0][0]:
                                    break
                            process_data[j][2] = process_data[j][2] - time_slice
                            ready_queue.pop(0)
                        elif ready_queue[0][2] <= time_slice:
                            '''
                            If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                            '''
                            start_time.append(s_time)
                            s_time = s_time + ready_queue[0][2]
                            e_time = s_time
                            exit_time.append(e_time)
                            executed_process.append(ready_queue[0][0])
                            for j in range(len(process_data)):
                                if process_data[j][0] == ready_queue[0][0]:
                                    break
                            process_data[j][2] = 0
                            process_data[j][3] = 1
                            process_data[j].append(e_time)
                            ready_queue.pop(0)
                    elif len(ready_queue) == 0:
                        if s_time < normal_queue[0][1]:
                            s_time = normal_queue[0][1]
                        if normal_queue[0][2] > time_slice:
                            '''
                            If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                            '''
                            start_time.append(s_time)
                            s_time = s_time + time_slice
                            e_time = s_time
                            exit_time.append(e_time)
                            executed_process.append(normal_queue[0][0])
                            for j in range(len(process_data)):
                                if process_data[j][0] == normal_queue[0][0]:
                                    break
                            process_data[j][2] = process_data[j][2] - time_slice
                        elif normal_queue[0][2] <= time_slice:
                            '''
                            If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                            '''
                            start_time.append(s_time)
                            s_time = s_time + normal_queue[0][2]
                            e_time = s_time
                            exit_time.append(e_time)
                            executed_process.append(normal_queue[0][0])
                            for j in range(len(process_data)):
                                if process_data[j][0] == normal_queue[0][0]:
                                    break
                            process_data[j][2] = 0
                            process_data[j][3] = 1
                            process_data[j].append(e_time)
                t_time = RoundRobin.calculateTurnaroundTime(self, process_data)
                w_time = RoundRobin.calculateWaitingTime(self, process_data)
                RoundRobin.printData(self, process_data, t_time, w_time, executed_process, time_slice)

            def calculateTurnaroundTime(self, process_data):
                total_turnaround_time = 0
                for i in range(len(process_data)):
                    turnaround_time = process_data[i][5] - process_data[i][1]
                    '''
                    turnaround_time = completion_time - arrival_time
                    '''
                    total_turnaround_time = total_turnaround_time + turnaround_time
                    process_data[i].append(turnaround_time)
                average_turnaround_time = total_turnaround_time / len(process_data)
                '''
                average_turnaround_time = total_turnaround_time / no_of_processes
                '''
                return average_turnaround_time

            def calculateWaitingTime(self, process_data):
                total_waiting_time = 0
                for i in range(len(process_data)):
                    waiting_time = process_data[i][6] - process_data[i][4]
                    '''
                    waiting_time = turnaround_time - burst_time
                    '''
                    total_waiting_time = total_waiting_time + waiting_time
                    process_data[i].append(waiting_time)
                average_waiting_time = total_waiting_time / len(process_data)
                '''
                average_waiting_time = total_waiting_time / no_of_processes
                '''
                return average_waiting_time

            def printData(self, process_data, average_turnaround_time, average_waiting_time, executed_process, ts):
                process_data.sort(key=lambda x: x[0])
                '''
                Sort processes according to the Process ID
                '''
                print(
                    "Process_ID  Arrival_Time  Rem_Burst_Time   Completed  Original_Burst_Time  Completion_Time  Turnaround_Time  Waiting_Time")

                print(f'Average Turnaround Time: {average_turnaround_time}')

                print(f'Average Waiting Time: {average_waiting_time}')

                print(process_data)
                print(f'Sequence of Processes: {executed_process}')
                run = [0]
                for i in range(len(executed_process)):
                    pid = executed_process[i]
                    for k in range(len(process_data)):
                        if process_data[k][0] == pid:
                            tBurst = process_data[k][4]
                            if tBurst > ts:
                                process_data[k][4] -= ts
                                run.append(ts)
                            elif tBurst <= ts:
                                process_data[k][4] = 0
                                run.append(tBurst)
                    if i == len(executed_process) - 1:
                        finalBurst = tBurst
                    timeList = []
                    sum = 0
                    for r in range(len(run)):
                        if r != 0:
                            sum += run[r - 1]
                            timeList.append(sum)
                for u in range(len(timeList)):
                    pid = str(executed_process[u])
                    time = str(timeList[u])
                    print((time + ":pid" + pid), end=" ")
                print(str(finalBurst + timeList[len(timeList) - 1]) + ":END")
                print(timeList)
                rSum = 0
                for n in range(len(process_data)):
                    PID = process_data[n][0]
                    index = executed_process.index(PID)
                    res = timeList[index]
                    rSum += res
                resTime = rSum / len(process_data)
                print("Average Response Time: " + str(resTime))

        rr = RoundRobin()
        rr.processData(file)


def genProcs():
    numProcs = int(input("Enter number of processes: "))
    minPrior = int(input("Enter minimum priority: "))
    maxPrior = int(input("Enter maximum priority: "))
    maxArrive = int(input("Enter maximum arrival time: "))
    minDuration = int(input("Enter minimum duration: "))
    maxDuration = int(input("Enter maximum duration: "))
    outF = input("Enter output file name: ")
    with open(outF, 'w') as outFile:
        for i in range(numProcs):
            tBurst = random.randint(minDuration, maxDuration)
            priority = random.randint(minPrior, maxPrior)
            if i != 0:
                tArrive = random.randint(0, maxArrive)
                pid = i
            elif i == 0:
                tArrive = 0
                pid = i
            print((str(pid) + ',' + str(priority) + ',' + str(tArrive) + ',' + str(tBurst)), file=outFile)


run = True
while run:
    choice = int(input("Generate Processes (1) or Get Schedule (2) or Quit(0)? "))
    if choice == 0:
        run = False
        break
    elif choice == 1:
        genProcs()
    elif choice == 2:
        fileName = input("Input name of file containing jobs: ")
        getSchedule(fileName)
    else:
        'Invalid choice'
