# Docker SwiftBar Plugin

This SwiftBar plugin provides a convenient menu bar interface for managing a project's Docker Compose services. 
It allows you to view container status, see exposed ports, and run common Docker Compose commands directly from your macOS menu bar.

## Features

- **List all services** defined in your Docker Compose file.
- **View status and ports** for each service.
- **Start, stop, restart, or view logs** for individual services.
- **Build containers**, **run all**, **stop all**, and **migrate database** with one click.

## Menu Commands

- **Service Name**: Shows the name of each service, color-coded by status.
  - **Status**: Shows the current status (e.g., Up, Exited).
  - **Ports**: Displays mapped ports.
  - **Start**: Starts the selected service.
  - **Stop**: Stops the selected service.
  - **Restart**: Restarts the selected service.
  - **Logs**: Opens logs for the selected service in a terminal.
- **Build containers**: Runs `docker compose build` for all services.
- **Run all containers**: Runs `docker compose up -d` to start all services.
- **Stop all containers**: Runs `docker compose down` to stop all services.

## Setup

1. **Install [SwiftBar](https://swiftbar.app/)** if you haven't already.
2. **Create a symlink of the plugin script** (`swiftbar/docker.5m.py`) to your SwiftBar plugins directory.
   * You can adjust the name of the symlink to change the refresh interval (e.g., `docker.1m.py` for 1 minute).
3. **Create a `config.json`** in the root directory of this project with the following content:
   ```json
   {
     "DOCKER_COMPOSE_FILE": "/path/to/your/docker-compose.yml"
   }