from collections import defaultdict
from pathlib import Path
# assign log file to python's TEXT I/O
file_path = Path("/tmp/application.log")

if file_path.exists():
    log_file = open(file_path, "r", encoding="utf-8")
else:
    raise "File does not exist. Check FilePath or filename."

class LogMessage:
    def __init__(self, level, component, message):
        self.level = level
        self.component = component
        self.message = message

logMessageList = [] # this list will hold all the LogMessage objects
component_errors = defaultdict(int) # this list will hold the different components and their counts
error_counts = defaultdict(int)

for line in log_file:
    line_list = line.split()

    log_level = line_list[2]
    log_component = line_list[3].replace("[", "").replace("]", "")
    my_strings = line_list[4:]
    seperator = ","
    this_message = seperator.join(my_strings).replace(",", " ")
    log_mesg = LogMessage(log_level, log_component, this_message)
    logMessageList.append(log_mesg)

error = 0
info = 0
warn = 0

for log in logMessageList:
    if log.level == "ERROR":
        error += 1
        component_errors[log.component] += 1
        sub = "-"
        error_message = log.message.split(sub)[0]
        error_counts[error_message] += 1
    elif log.level == "WARN":
        warn += 1
    elif log.level == "INFO":
        info += 1

sorted_errors = sorted(error_counts.items(), key=lambda item: item[1], reverse=True)

print(" === Log Analysis Report ===/")
print("")

print ("Log Level Summary:")
print(f"   INFO: {info}")
print(f"   WARN: {warn}")
print(f"   ERROR: {error}")
print("\n Top 3 Error Messages:")
print(f"1. {sorted_errors[0]}")
print(f"2. {sorted_errors[1]}")
print(f"3. {sorted_errors[2]}")

print("\nComponents with Errors: ")
for comp in component_errors:
    print(f"{comp}: {component_errors[comp]} errors")
