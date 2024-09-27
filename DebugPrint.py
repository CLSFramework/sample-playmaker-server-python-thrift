import os
from datetime import datetime
from pprint import pprint
import sys
from soccer.ttypes import State , RegisterResponse , WorldModel
player_num = None

class DebugPrint:
    def __init__(self, state_player_num):
        """
        Initializes the DebugPrint class with a player number.
        A separate log file is created for each player.
        
        :param state_player_num: The unique number identifying the player
        """
        global player_num
        player_num = state_player_num

        log_dir = "debug/player_logs"
        # Ensure the log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.log_file_path = os.path.join(log_dir, f"player_{state_player_num}.log")
        

    
    def debugprint(self, data , state :State):
        """
        Logs debug information to the player's log file.
        
        :param data: The data to log (object, dictionary, etc.)
        :param state: The state object to get the worldmodel
        """
        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"Cycle {state.world_model.cycle} : {data}\n")
            log_file.write("\n")
    
    def initialize_debug_printers():
        """
        Initializes the global debug_printers instances and removes the existing log files if they exist.
        """
        for player_num in range(1, 12):
            log_file_path = os.path.join("debug", "player_logs", f"player_{player_num}.log")
            
            # Remove the existing log file if it exists
            if os.path.exists(log_file_path):
                os.remove(log_file_path)
            
            DebugPrint(player_num)



def dprint(state :State , data):
    """
    Logs debug information to the player's log file without creating an instance.
    
    :param data: The data to log (object, dictionary, etc.)
    state :State: The state object to get the cycle number
    """
    global player_num
    player_num = state.register_response.uniform_number

    if player_num is None:
        print("player_num is not set. Initialize DebugPrint with a player number first.")
        return

    debug_printer = DebugPrint(player_num)
    debug_printer.debugprint(data,state)

