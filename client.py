import configparser
import logging
import socket
import json


# ------------------- Configuration Section -------------------
def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def setup_logging(log_file, log_level, log_mode):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')

    logging.basicConfig(filename=log_file,
                        level=numeric_level,
                        filemode=log_mode,
                        format='%(asctime)s: %(levelname)s - %(message)s')


# ------------------- Client Section -------------------
def start_client(config):
    log = logging.getLogger(__name__)
    server_ip = config['project 2']['serverHost']
    server_port = int(config['project 2']['serverPort'])

    log.info('Connecting to server at %s:%s', server_ip, server_port)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            server_address = (server_ip, server_port)
            sock.connect(server_address)
            log.info("Connected to the server")

            still_running = True
            while still_running:
                command_string = input("Project 2> ")
                if not command_string:
                    print("No command entered")
                    log.info("No command entered")
                    continue

                log.info('Entered string = %s', command_string)

                # Parse the command string
                command_string = command_string.replace(' ', '§', 1)
                command_array = command_string.split('§')

                # Isolate command and parameters
                if len(command_array) and command_array[0]:
                    token_one = command_array[0].upper()
                    command_entered = True
                else:
                    log.info("No command entered")
                    command_entered = False
                    continue

                token_two = command_array[1] if len(command_array) > 1 else ''

                if command_entered:
                    request = json.dumps({
                        "command": token_one,
                        "parameter": token_two
                    })
                    log.info('Processed string = %s', request)

                    # Send request to the server
                    sock.send(request.encode('utf-8'))

                    # Receive response from the server
                    response = sock.recv(1024).decode('utf-8')
                    response_json = json.loads(response)
                    log.info('Received server response: %s', response)

                    # Handle response
                    print(response_json['parameter'])
                    if response_json['response'] == "QUITTING":
                        log.info("Shutting down client...")
                        print("Shutting down...")
                        still_running = False

        sock.close()
    except socket.error as e:
        logging.error("Failed to connect to server")
        print("Could not connect to server")
        print(e)


# ------------------- Main Section -------------------
def main():
    config_file = 'configclient.ini'
    config = read_config(config_file)

    # Set up logging
    log_file = config['logger']['logFile']
    log_level = config['logger']['logLevel']
    log_mode = config['logger']['logFileMode']
    setup_logging(log_file, log_level, log_mode)

    log = logging.getLogger(__name__)
    log.info('Starting the client')

    # Start client
    start_client(config)


if __name__ == "__main__":
    main()
