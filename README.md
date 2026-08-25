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