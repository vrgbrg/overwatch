import psutil

def get_running_processes():
    list_of_running_processes = get_list_of_processes_by_memory()
    for process in list_of_running_processes[:5]:
        print(process)


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