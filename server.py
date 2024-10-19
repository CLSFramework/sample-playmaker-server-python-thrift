from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from soccer import Game
from soccer.ttypes import Body_GoToPoint, DoChangeMode, DoMovePlayer, State, Empty, PlayerActions, CoachActions, TrainerActions, PlayerAction, GameModeType
from soccer.ttypes import ServerParam, PlayerParam, PlayerType, InitMessage, RegisterRequest, RegisterResponse, AgentType , RpcActionState, BestPlannerActionRequest , BestPlannerActionResponse
from soccer.ttypes import HeliosOffensivePlanner, HeliosBasicMove, HeliosGoalie, HeliosSetPlay, HeliosShoot
from soccer.ttypes import DoMoveBall, RpcVector2D, TrainerAction
from soccer.ttypes import DoHeliosSubstitute, CoachAction
import os
from utils.PFProcessServer import PFProcessServer
from thrift.server.TServer import TThreadedServer
from typing import Union
from threading import Semaphore
from multiprocessing import Manager, Lock
import logging
from pyrusgeom.vector_2d import Vector2D
import argparse
from utils.logger_utils import setup_logger
import datetime


console_logging_level = logging.INFO
file_logging_level = logging.DEBUG

main_logger = None
log_dir = None


class GameHandler:
    def __init__(self, shared_lock, shared_number_of_connections):
        self.server_params: Union[ServerParam, None] = None
        self.player_params: Union[PlayerParam, None] = None
        self.player_types: dict[int, PlayerType] = {}
        self.debug_mode: bool = False
        self.shared_lock = shared_lock
        self.shared_number_of_connections = shared_number_of_connections
        self.logger: logging.Logger = setup_logger("Agent", log_dir, console_level=console_logging_level, file_level=file_logging_level)

    def GetPlayerActions(self, state: State):
        self.logger.debug(f"================================= cycle={state.world_model.cycle}.{state.world_model.stoped_cycle} =================================")
        self.logger.debug(f"GetPlayerActions unum {state.register_response.uniform_number} at {state.world_model.cycle}")
        actions = []
        if state.world_model.game_mode_type == GameModeType.PlayOn:
            if state.world_model.myself.is_goalie:
                actions.append(PlayerAction(helios_goalie=HeliosGoalie()))
            elif state.world_model.myself.is_kickable:
                actions.append(PlayerAction(helios_offensive_planner=HeliosOffensivePlanner(lead_pass=True,
                                                                                            direct_pass=True,
                                                                                            through_pass=True,
                                                                                            simple_pass=True,
                                                                                            short_dribble=True,
                                                                                            long_dribble=True,
                                                                                            simple_shoot=True,
                                                                                            simple_dribble=True,
                                                                                            cross=True,
                                                                                            server_side_decision=True)))
                actions.append(PlayerAction(helios_shoot=HeliosShoot()))
            else:
                actions.append(PlayerAction(helios_basic_move=HeliosBasicMove()))
        else:
            actions.append(PlayerAction(helios_set_play=HeliosSetPlay()))

        res = PlayerActions(actions=actions)
        self.logger.debug(f"Actions: {res}")
        return res

    def GetCoachActions(self, state: State):
        self.logger.debug(f"================================= cycle={state.world_model.cycle}.{state.world_model.stoped_cycle} =================================")
        self.logger.debug(f"GetCoachActions coach at {state.world_model.cycle}")
        actions = []
        actions.append(CoachAction(do_helios_substitute=DoHeliosSubstitute()))
        res = CoachActions(actions=actions)
        self.logger.debug(f"Actions: {res}")
        return res

    def GetTrainerActions(self, state: State):
        self.logger.debug(f"================================= cycle={state.world_model.cycle}.{state.world_model.stoped_cycle} =================================")
        self.logger.debug(f"GetTrainerActions trainer at {state.world_model.cycle}")
        actions = []
        if state.world_model.cycle % 100 == 99:
            self.logger.debug(f"Trainer at cycle {state.world_model.cycle}")
            if len(state.world_model.teammates) == 0:
                return TrainerActions()
            player = state.world_model.teammates[0]
            p = Vector2D(player.position.x, player.position.y)
            p = p + Vector2D(10, 10)
            actions = [
                TrainerAction(
                    do_move_ball=DoMoveBall(
                        position=RpcVector2D(
                            x=p.x(),
                            y=p.y()
                        ),
                        velocity=RpcVector2D(
                            x=0,
                            y=0
                        ),
                    )
                ),
                TrainerAction(do_move_player=DoMovePlayer(
                    our_side=True,
                    uniform_number=player.uniform_number,
                    position=RpcVector2D(
                        x=p.x(),
                        y=p.y()
                    ),
                    body_direction=0.,
                )),
                TrainerAction(do_change_mode=DoChangeMode(game_mode_type=GameModeType.PlayOn))
            ]
        res = TrainerActions(actions=actions)
        self.logger.debug(f"Actions: {res}")
        return res

    def SendServerParams(self, serverParams: ServerParam):
        self.logger.debug(f"Server params received unum {serverParams.register_response.uniform_number}")
        self.server_params = serverParams
        res = Empty()
        return res

    def SendPlayerParams(self, playerParams: PlayerParam):
        self.logger.debug(f"Player params received unum {playerParams.register_response.uniform_number}")
        self.player_params = playerParams
        res = Empty()
        return res

    def SendPlayerType(self, playerType: PlayerType):
        self.logger.debug(f"Player type received unum {playerType.register_response.uniform_number}")
        self.player_types[playerType.id] = playerType
        res = Empty()
        return res

    def SendInitMessage(self, initMessage: InitMessage):
        self.logger.debug(f"Init message received unum {initMessage.register_response.uniform_number}")
        self.debug_mode = initMessage.debug_mode
        res = Empty()
        return res

    def Register(self, register_request: RegisterRequest):
        self.logger.debug(f"received register request from team_name: {register_request.team_name} "
                      f"unum: {register_request.uniform_number} "
                      f"agent_type: {register_request.agent_type}")
        with self.shared_lock:
            self.shared_number_of_connections.value += 1
            self.logger.debug(f"Number of connections {self.shared_number_of_connections.value}")
            team_name = register_request.team_name
            uniform_number = register_request.uniform_number
            agent_type = register_request.agent_type
            self.logger: logging.Logger = setup_logger(f"Agent{register_request.uniform_number}-{self.shared_number_of_connections.value}", 
                                                       log_dir, 
                                                       console_level=console_logging_level, file_level=file_logging_level)
            res = RegisterResponse(client_id=self.shared_number_of_connections.value,
                                   team_name=team_name,
                                   uniform_number=uniform_number,
                                   agent_type=agent_type)
            return res

    def SendByeCommand(self, register_response: RegisterResponse):
        self.logger.debug(f"Bye command received unum {register_response.uniform_number}")
        with self.shared_lock:
            pass
        res = Empty()
        return res
    def GetBestPlannerAction(self, pairs: BestPlannerActionRequest):
        self.logger.debug(f"GetBestPlannerAction cycle:{pairs.state.world_model.cycle} pairs:{len(pairs.pairs)} unum:{pairs.state.register_response.uniform_number}")
        pairs_list: list[int, RpcActionState] = [(k, v) for k, v in pairs.pairs.items()]
        pairs_list.sort(key=lambda x: x[0])
        best_action = max(pairs_list, key=lambda x: -1000 if x[1].action.parent_index != -1 else x[1].predict_state.ball_position.x)
        self.logger.debug(f"Best action: {best_action[0]} {best_action[1].action.description} to {best_action[1].action.target_unum} in ({round(best_action[1].action.target_point.x, 2)},{round(best_action[1].action.target_point.y, 2)}) e:{round(best_action[1].evaluation,2)}")
        res = BestPlannerActionResponse(index=best_action[0])
        return res

def serve(port, shared_lock, shared_number_of_connections):
    handler = GameHandler(shared_lock, shared_number_of_connections)
    processor = Game.Processor(handler)
    transport = TSocket.TServerSocket(host='0.0.0.0', port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = PFProcessServer(processor, transport, tfactory, pfactory)
    # server = TThreadedServer(processor, transport, tfactory, pfactory)

    main_logger.info(f"Starting server on port {port}")
    try:
        server.serve()
    except KeyboardInterrupt:
        server.stop()
        print("Stopping server")


def main():
    global main_logger, log_dir
    manager = Manager()
    shared_lock = Lock()  # Create a Lock for synchronization
    shared_number_of_connections = manager.Value('i', 0)
    parser = argparse.ArgumentParser(description='Run play maker server')
    parser.add_argument('-p', '--rpc-port', required=False, help='The port of the server', default=50051)
    parser.add_argument('-l', '--log-dir', required=False, help='The directory of the log file', 
                    default=f'logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
    args = parser.parse_args()
    log_dir = args.log_dir
    main_logger = setup_logger("pmservice", log_dir, console_level=console_logging_level, file_level=file_logging_level)

    serve(args.rpc_port, shared_lock, shared_number_of_connections)
    
    
if __name__ == '__main__':
    main()
    
