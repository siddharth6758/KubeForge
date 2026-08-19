                    ┌─────────────────┐
                    │     GitHub      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ GitHub Actions  │
                    │                 │
                    │ Tests           │
                    │ Docker          │
                    │ Trivy           │
                    │ Kyverno CLI     │
                    │ Helm validation │
                    └────────┬────────┘
                             │
                             ▼
                       Container Registry
                             │
                             ▼
                    ┌─────────────────┐
                    │     Argo CD     │
                    └────────┬────────┘
                             │
                             ▼
              ╔══════════════════════════════╗
              ║        Kubernetes            ║
              ║                              ║
              ║ Gateway API                  ║
              ║      │                       ║
              ║ HTTPRoute                    ║
              ║      │                       ║
              ║ FastAPI ─────── Worker       ║
              ║   │              │           ║
              ║   ├── PostgreSQL             ║
              ║   └── Redis                  ║
              ║                              ║
              ║ HPA │ PDB │ RBAC             ║
              ║ NetworkPolicy                ║
              ║                              ║
              ║ Kyverno                      ║
              ╚══════════════╤═══════════════╝
                             │
                     ┌───────┴────────┐
                     │                │
                 Prometheus         Grafana