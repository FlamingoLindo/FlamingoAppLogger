"""
Scripts to start logger stuff
"""
import subprocess
import threading


class Logger():
    """
    Logger Stuff
    """

    def start_adb(self):
        """
        Start ADB
        """
        try:
            result = subprocess.run(["adb", 'devices'],
                                    capture_output=True,
                                    text=True,
                                    check=True, shell=True)
            return result
        except subprocess.CalledProcessError as e:
            print(e)

    def start_logcat(self, callback):
        """
        Start Logcat in real-time with a callback function
        callback: function that takes a string (log line) as parameter
        """
        self.is_running = True

        def read_output():
            try:
                self.logcat_process = subprocess.Popen(
                    ["adb", "logcat"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    shell=True
                )

                for line in iter(self.logcat_process.stdout.readline, ''):
                    if not self.is_running:
                        break
                    if line:
                        callback(line)

            except Exception as e:
                callback(f"Error: {str(e)}\n")

        thread = threading.Thread(target=read_output, daemon=True)
        thread.start()

    def stop_logcat(self):
        """
        Stop the logcat process
        """
        self.is_running = False
        if self.logcat_process:
            self.logcat_process.terminate()
            self.logcat_process.wait()
            self.logcat_process = None
