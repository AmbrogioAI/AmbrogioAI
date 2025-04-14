class Logger:
    
    @staticmethod     
    def logTagged(tag, message):
        print(f"[{tag}] {message}")
        # check if the log file exists, if not create it
        try:
            with open("log.txt", "a") as f:
                f.write(f"[{tag}] {message}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

    @staticmethod
    def log(message):
        print(f"{message}")
        # check if the log file exists, if not create it
        try:
            with open("log.txt", "a") as f:
                f.write(f"{message}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

    @staticmethod
    def resetFile():
        try:
            with open("log.txt", "w") as f:
                f.write("")
        except Exception as e:
            print(f"Error writing to log file: {e}")