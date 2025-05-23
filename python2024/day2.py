from pathlib import PosixPath
import sys


def check_safety( report: list ) -> bool:
    # Sliding window to check values are all monotonically increasing or decreasing
    increasing = (report[0] - report[1]) < 0
    for i in range(0, len(report) - 1):
        diff = report[i] - report[i+1]

        if( diff == 0 or abs(diff) > 3 ): return False
        if( (diff < 0) != increasing ): return False

    return True


def count_safe_reports( reports: list, apply_dampner: bool ):
    safe_reports = 0
    for report in reports:
        int_report = [int(n) for n in report.split()]
        if check_safety(int_report):
            safe_reports += 1
        elif apply_dampner: 
            for i in range(len(int_report)):
                excluded_report = int_report.copy()
                excluded_report.pop(i)
                if check_safety(excluded_report):
                    safe_reports += 1
                    break

    return safe_reports


test_array = "7 6 4 2 1 \n\
1 2 7 8 9 \n\
9 7 6 2 1 \n\
1 3 2 4 5 \n\
8 6 4 4 1 \n\
1 3 6 7 9"

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        input_arr = test_array
    else:
        input_arr = open(PosixPath("inputs/day2.txt")).read()

    reports = input_arr.splitlines()

    safe_reports = count_safe_reports(reports, False)
    print(f'There are {safe_reports} safe reports')

    safe_damped_reports = count_safe_reports(reports, True)
    print(f'There are {safe_damped_reports} safe reports with the dampner')
