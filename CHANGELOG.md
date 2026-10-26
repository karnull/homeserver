# Changelog

## added/modified:

* feature/skeleton: Unix socket server with token auth, audit log, config file, health check and a systemd user service.
* feature/system-stats: read-only routes for CPU temperature and load, RAM, swap, disk and uptime.
* feature/container-routes: list every container, and start, stop or restart those belonging to a project, never protected ones.
* feature/project-routes: list the projects in ~/Blackwall and bring them up and down through the host's d script.
* feature/protected-projects: Judy's own project in ~/Blackwall/Judy and its containers are off-limits to every action.
* feature/fork-endpoint: POST /projects/fork validates a folder name and GitHub URL; forking itself is not built yet.
* fix/install-python: install.sh follows the project's Python version instead of pinning 3.13, including on hosts first set up with it, and every version reported comes from VERSION.
* docs/agent-skill: skills.md, a guide for agents on calling Uplink's routes and handling its errors.
