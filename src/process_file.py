import os
from log_analyser.log_analyser import LogAnalyser

for file in os.listdir("logs"):
    if file.endswith(".txt"):
        la = LogAnalyser('logs', file, "test")
        la.run()
        print("a")