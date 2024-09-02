import subprocess
import os
import signal
import threading
import logging
import argparse
import check_requirements


# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def run_server_script(args):
    # Start the server.py script as a new process group
    process = subprocess.Popen(
        ['python3', 'server.py', '--rpc-port', args.rpc_port],
        preexec_fn=os.setsid,  # Create a new session and set the process group ID
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT  # Capture stderr and redirect it to stdout
    )
    return process

def run_start_script(args):
    # Start the start.sh script in its own directory as a new process group
    process = subprocess.Popen(
        ['bash', 'start.sh', '-t', args.team_name, '--rpc-port', args.rpc_port],
        cwd='scripts/proxy',  # Corrected directory to where start.sh is located
        preexec_fn=os.setsid,  # Create a new session and set the process group ID
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT  # Capture stderr and redirect it to stdout
    )
    return process

def stream_output(process, prefix):
    # Stream output from the process and log it with a prefix
    for line in iter(process.stdout.readline, b''):
        logging.debug(f'{prefix} {line.decode().strip()}')
    process.stdout.close()

def kill_process_group(process):
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Send SIGTERM to the process group
    except ProcessLookupError:
        pass  # The process might have already exited

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run server and team scripts.')
    parser.add_argument('-t', '--team_name', required=False, help='The name of the team', default='CLS')
    parser.add_argument('--rpc-port', required=False, help='The port of the server', default='50051')
    args = parser.parse_args()

    try:
        # Check Python requirements
        logging.debug("Checking Python requirements...")
        check_requirements.check_requirements()
        
        # Run the server.py script first
        server_process = run_server_script(args)
        logging.debug(f"Started server.py process with PID: {server_process.pid}")

        # Run the start.sh script after server.py with the given arguments
        start_process = run_start_script(args)
        logging.debug(f"Started start.sh process with PID: {start_process.pid} with team name {args=}")

        # Monitor both processes and log their outputs
        server_thread = threading.Thread(target=stream_output, args=(server_process, 'server:'))
        start_thread = threading.Thread(target=stream_output, args=(start_process, 'team:'))

        server_thread.start()
        start_thread.start()

        # Wait for both threads to finish
        server_thread.join()
        start_thread.join()

    except KeyboardInterrupt:
        logging.debug("Interrupted! Killing all processes.")
        kill_process_group(server_process)
        kill_process_group(start_process)

    finally:
        # Ensure all processes are killed on exit
        kill_process_group(server_process)
        kill_process_group(start_process)
