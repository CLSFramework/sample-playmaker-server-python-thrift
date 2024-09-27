import os
import shutil
from datetime import datetime
from soccer.ttypes import State

class DebugPrint:
    def __init__(self, state_player_num, custom_log_file_name=None):
        """
        Initializes the DebugPrint class with a player number.
        A separate log file is created for each player unless a custom log file is specified.
        
        :param state_player_num: The unique number identifying the player
        :param custom_log_file_path: Optional custom log file path
        """
        global player_num
        player_num = state_player_num

        if custom_log_file_name:
            log_dir = "debug/player_logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            self.log_file_path = os.path.join(log_dir, f"{custom_log_file_name}.log")
        else:
            # Use default log directory and file name
            log_dir = "debug/player_logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            self.log_file_path = os.path.join(log_dir, f"player_{state_player_num}.log")

    def debugprint(self, data, state: State):
        """
        Logs debug information to the player's log file.
        
        :param data: The data to log (object, dictionary, etc.)
        :param state: The state object to get the worldmodel
        """
        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"Cycle {state.world_model.cycle} : {data}\n")
            log_file.write("\n")

    @staticmethod
    def initialize_debug_printers():
        """
        Initializes the global debug_printers instances and renames the existing log directory
        instead of deleting the log files.
        """
        log_dir = os.path.join("debug", "player_logs")
        
        # If the directory exists, rename it with a timestamp
        if os.path.exists(log_dir):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_log_dir = f"debug/player_logs_{timestamp}"
            shutil.move(log_dir, new_log_dir)
        
        # Create a new player_logs directory
        os.makedirs(log_dir)

        # Initialize a DebugPrint instance for each player
        for player_num in range(1, 12):
            DebugPrint(player_num)

def dprint(state: State, data, custom_log_file_name=None):
    """
    Logs debug information to the player's log file without creating an instance.
    Supports custom file name and file path.
    
    :param state: The state object to get the cycle number
    :param data: The data to log (object, dictionary, etc.)
    :param custom_log_file_name: Optional custom log file name
    :param custom_log_file_path: Optional custom log file path
    """
    global player_num
    player_num = state.register_response.uniform_number

    if player_num is None:
        print("player_num is not set. Initialize DebugPrint with a player number first.")
        return

    debug_printer = DebugPrint(player_num, custom_log_file_name)
    debug_printer.debugprint(data, state)
