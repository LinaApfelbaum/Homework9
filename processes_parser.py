"""Processes parser"""

import subprocess
import re
from datetime import datetime


def get_processes_list():
    """Returns processes list"""
    return subprocess.run(
        ['ps', 'aux'], capture_output=True, check=True).stdout.decode('utf-8').splitlines()[1:]


def get_report_data(processes_list):
    """Generates report from processes list"""
    processes_per_user = {}
    total_cpu = 0.0
    total_memory = 0.0
    max_cpu_process = None
    max_cpu_value = None
    max_memory_process = None
    max_memory_value = None

    for process in processes_list:
        process_data = re.split(" +", process, maxsplit=10)
        total_cpu += float(process_data[2])
        total_memory += float(process_data[5])
        user = process_data[0]
        cpu = float(process_data[2])
        memory = float(process_data[5])

        if max_cpu_process is None:
            max_cpu_process = process_data
            max_cpu_value = cpu
            max_memory_process = process_data
            max_memory_value = memory

        if user not in processes_per_user:
            processes_per_user[user] = 1
        else:
            processes_per_user[user] += 1

        if cpu > max_cpu_value:
            max_cpu_value = cpu
            max_cpu_process = process_data

        if memory > max_memory_value:
            max_memory_value = memory
            max_memory_process = process_data

    return total_memory, total_cpu, processes_per_user, max_memory_process, max_cpu_process


def generate_report(total_memory, total_cpu, processes_per_user,
                    max_memory_process, max_cpu_process):
    """Generates report with provided data"""
    total_processes = 0
    total_memory_formatted = "{:.2f}".format(round(total_memory / 1024, 2))
    total_cpu_formatted = "{:.2f}".format(round(total_cpu, 2))
    report = "System users: \n"
    for user_name, processes_count in processes_per_user.items():
        report += user_name + "\n"
        total_processes += processes_count

    report += "\n"
    report += f"Total processes: {total_processes}\n\n"

    report += "Processes by user:\n"
    for user_name, processes_count in processes_per_user.items():
        report += user_name + ": " + str(processes_count) + "\n"

    report += "\n"
    report += f"Total memory: {total_memory_formatted}Mb\n"
    report += f"Total CPU: {total_cpu_formatted}%\n"
    report += f"Max memory usage: {max_memory_process[10][:20]}\n"
    report += f"Max CPU usage: {max_cpu_process[10][:20]}\n"

    return report


def main():
    """Parses processes and generates report to file and to stdout"""
    processes_list = get_processes_list()
    report = generate_report(*get_report_data(processes_list))
    with open(datetime.today().strftime('%Y-%m-%d_%H:%M:%S') + ".txt", "w") as file:
        file.write(report)

    print(report)


main()
