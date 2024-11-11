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


# ------------------- Server Section -------------------
def start_server(config):
    log = logging.getLogger(__name__)
    server_ip = config['project 2']['serverHost']
    server_port = int(config['project 2']['serverPort'])
    log.info('Starting server at %s:%s', server_ip, server_port)

    # Create a socket, bind, and listen for connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    log.info("Server is listening...")


    log.info('Waiting for client connection...')
    client_socket, addr = server_socket.accept()
    log.info('Connection accepted from %s', addr)
    handle_client(client_socket, log)


def handle_client(client_socket, log):
    still_running = True
    while still_running:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break

        # Parse the received request
        request_json = json.loads(request)
        command = request_json['command']
        param = request_json['parameter']

        log.info(f'Received command: {command} with parameter: {param}')

        # Handle QUIT command
        if command == "QUIT":
            response = {
                "response": "QUITTING",
                "parameter": ""
            }
            client_socket.send(json.dumps(response).encode('utf-8'))
            log.info("Shutting down server...")
            still_running = False
        else:
            response = {
                "response": command,
                "parameter": f"Server received: {param}"
            }
            client_socket.send(json.dumps(response).encode('utf-8'))
    log.info("Disconnecting")
    client_socket.close()



# ------------------- Main Section -------------------
def main():
    config_file = 'configserver.ini'
    config = read_config(config_file)

    # Set up logging
    log_file = config['logger']['logFile']
    log_level = config['logger']['logLevel']
    log_mode = config['logger']['logFileMode']
    setup_logging(log_file, log_level, log_mode)

    log = logging.getLogger(__name__)
    log.info('Starting the server')

    # Start server
    start_server(config)


if __name__ == "__main__":
    main()
