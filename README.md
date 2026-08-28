# KubeForge
<b>Goal:</b> Build and operate a production-style Kubernetes platform that runs a containerized FastAPI application across multiple environments, with Helm-based deployments, Kyverno policy enforcement, Gateway API routing, RBAC, autoscaling, observability, CI/CD/GitOps, and a deliberately broken environment where you diagnose and recover Kubernetes failures.

# Day 1
- Initialize github repository: <strong>KubeForge</strong>
- Plan out the structure of the project

# Day 2
- Setup PostgresDB and Redis using docker containers
- Plan the structure of Backend Architecture
- Add database engine and Tables for User and Notification (Postgre and Redis are containerized, so this app cannot run as a standalone backend)

# Day 3
- Containerize the Backend application and connect with database and redis

# Day 4
- Write the remaining read/write logic and endpoints for FastAPI
- Figure out how to implement <b>Redis PUB/SUB</b> to provide real-time event notification

# Day 5
- Set up <b>Redis sorted set</b> for notification queue (<b>Pub/Sub declined as the scenario didn't fit and would increase the containers</b>) [Sorted set because the notifications would automatically get sorted according to unix time and one worker node would constantly monitor the date-time and fetch from the set]
- Choose python notification module and implement its application <b>(does not work)</b>

# Day 6
- Create a worker script to monitor the datetime and fetch notification from <b>Redis sorted set</b>
- Containerize the worker script and connect it with api-backend and redis
- Try different module for notification - still failed

# Day 7
- Convert the worker script to a seperate FastAPI application for healtcheck and docker-compose.yaml dependency purpose
- Create Frontend (HTML, CSS and JS) for the FastAPI Application (used AI for this as main goal is to learn k8s)
- Fix timezone issue: converted all time-inputs to IST and also accepts only IST timezone

# Day 8
- 