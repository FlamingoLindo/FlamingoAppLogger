"""
Scripts to start logger stuff
"""
import subprocess


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
