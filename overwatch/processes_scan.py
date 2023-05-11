import psutil
import reports.report as report

def get_running_processes(ip):
    if ip == "localhost" or ip == "127.0.0.1":
        list_of_running_processes = get_list_of_processes_by_memory()
        if len(list_of_running_processes) > 0:
            report.storeMessage("title", "Running processes")
            report.storeMessage("processes", list_of_running_processes[:5])
            print('Running processes:')
            for process in list_of_running_processes[:5]:
                print(process)
    else:
        print('TODO')


def get_list_of_processes_by_memory():
    list_of_processes = []
    for process in psutil.process_iter():
        try:
            pinfo = process.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = process.memory_info().vms / (1024 * 1024)
            list_of_processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    list_of_processes = sorted(
        list_of_processes, key=lambda procObj: procObj['vms'], reverse=True)
    return list_of_processes
