#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
import json
import os
import subprocess
from _testcapi import fatal_error

def get_docker_status(docker_file: str) -> str:
    """
    Obtain the current running dockers per the provided docker compose file.

    :param docker_file: The path to the docker compose file
    :type docker_file: str

    :return: A string containing the status of the docker containers
    :rtype docker_file: str
    """
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", docker_file, "ps", "-a"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"


def color_for_status(status_: str) -> str:
    """
    Determine the color code based on the status of the docker container.

    :param status_: The status of the docker container
    :type status_: str

    :return: The color code as a string
    :rtype: str
    """
    if status_.startswith("Up"):
        return "#6FCF97"
    elif status_.startswith("Exited"):
        return "#FF4B4B"
    else:
        return "#FFD700"


def parse_columns(header_line: str) -> list:
    """
    Parse the header line of the docker ps output to determine the positions of each column.

    :param header_line: The header line from the docker ps output
    :type header_line: str

    :return: A list of tuples containing the column name and its starting position
    :rtype: list
    """
    columns = ["NAME", "IMAGE", "COMMAND", "SERVICE", "CREATED", "STATUS", "PORTS"]
    positions = []
    for col in columns:
        idx = header_line.find(col)
        if idx != -1:
            positions.append((col, idx))
    positions.sort(key=lambda x: x[1])
    return positions


def extract_fields(line_: str, columns_: list) -> dict:
    """
    Extract fields from a line of docker ps output into a dictionary object

    :param line_: A line from the docker ps output
    :type line_: str

    :return: A dictionary with the fields extracted
    :rtype: dict
    """
    fields_ = {}
    for i, (col, start) in enumerate(columns_):
        end = columns_[i+1][1] if i+1 < len(columns_) else None
        fields_[col] = line_[start:end].strip()
    return fields_


def print_container(line_: str, docker_file: str, columns_: list):
    fields = extract_fields(line_, columns_)
    service = fields.get("SERVICE", "")
    status_str = fields.get("STATUS", "")
    ports = fields.get("PORTS", "")
    print(f"{service} | color={color_for_status(status_str)}")
    # Submenu header
    print(f"--Status: {status_str} | color=#B0B8C1")
    print(f"--Ports: {ports or '--'} | color=#B0B8C1")
    print(f"--Start | bash='docker' param1=compose param2=-f param3={docker_file} param4=start param5={service} "
          f"terminal=false refresh=true")
    print(f"--Stop | bash='docker' param1=compose param2=-f param3={docker_file} param4=stop param5={service} "
          f"terminal=false refresh=true")
    print(f"--Restart | bash='docker' param1=compose param2=-f param3={docker_file} param4=restart param5={service} "
          f"terminal=false refresh=true")
    print(f"--Logs | bash='docker' param1=compose param2=-f param3={docker_file} param4=logs param5={service} "
          f"terminal=true")


if __name__ == '__main__':
    print('Docker | color=#39DB2B')
    print('---')
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as json_data_file:
            data = json.load(json_data_file)
            docker_compose_file = data['DOCKER_COMPOSE_FILE']
    except Exception as e:
        fatal_error(f"Couldn't read [config.json] config file - {e}")

    status = get_docker_status(docker_compose_file)
    if status.startswith("Error:"):
        print(f"Status: {status} | color=red")
    else:
        lines = status.splitlines()
        if not lines or len(lines) < 2:
            print("No containers running.")
        else:
            columns = parse_columns(lines[0])
            for line in lines[1:]:
                if not line.strip():
                    continue
                print_container(line, docker_compose_file, columns)

    print('---')
    print(f"Build containers | bash='docker' param1=compose param2=-f param3={docker_compose_file} param4=build terminal=true refresh=true")
    print(f"Run all containers | bash='docker' param1=compose param2=-f param3={docker_compose_file} param4=up param5=-d terminal=false refresh=true")
    print(f"Stop all containers | bash='docker' param1=compose param2=-f param3={docker_compose_file} param4=stop terminal=false refresh=true")
