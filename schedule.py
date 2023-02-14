
def getNumProcs(fname):
    i = 0
    with open(fname, 'r') as file:
        for line in file:
            i += 1
    return i


def getSchedule():
    alg = input("Which algorithm (fcfs, stcf, sjf, rr)? ")
    if alg == "fcfs":
        class FCFS:
            def processData(self, fname):
                process_data = []
                with open(fname, 'r') as data:
                    for line in data:
                        line = line.split(",")
                        temporary = []
                        process_id = int(line[0])

                        arrival_time = int(line[2])

                        burst_time = int(line[3])

                        temporary.extend([process_id, arrival_time, burst_time])
                        process_data.append(temporary)
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
                FCFS.printData(self, process_data, t_time, w_time)

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

            def printData(self, process_data, average_turnaround_time, average_waiting_time):

                print("Process_ID  Arrival_Time  Burst_Time  Completion_Time  Turnaround_Time  Waiting_Time")

                for i in range(len(process_data)):
                    for j in range(len(process_data[i])):
                        print(process_data[i][j], end="				")
                    print()

                print(f'Average Turnaround Time: {average_turnaround_time}')

                print(f'Average Waiting Time: {average_waiting_time}')

        if __name__ == "__main__":
            fcfs = FCFS()
            fcfs.processData("procs")


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
        sjf.processData("procs")

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
                print(f'Sequence of Process: {sequence_of_process}')

        if __name__ == "__main__":
            stcf = STCF()
            stcf.processData("procs")

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
                RoundRobin.printData(self, process_data, t_time, w_time, executed_process)

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

            def printData(self, process_data, average_turnaround_time, average_waiting_time, executed_process):
                process_data.sort(key=lambda x: x[0])
                '''
                Sort processes according to the Process ID
                '''
                print(
                    "Process_ID  Arrival_Time  Rem_Burst_Time   Completed  Original_Burst_Time  Completion_Time  Turnaround_Time  Waiting_Time")
                for i in range(len(process_data)):
                    for j in range(len(process_data[i])):
                        print(process_data[i][j], end="				")
                    print()

                print(f'Average Turnaround Time: {average_turnaround_time}')

                print(f'Average Waiting Time: {average_waiting_time}')

                print(f'Sequence of Processes: {executed_process}')

        if __name__ == "__main__":
            rr = RoundRobin()
            rr.processData("procs")

        rr = RoundRobin()
        rr.processData("procs")


getSchedule()