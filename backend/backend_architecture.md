                    ┌─────────────────┐
                    │     Client      │
                    │ Web / Mobile UI │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │   REST API      │
                    └───────┬─────────┘
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │ PostgreSQL   │          │    Redis     │
       │              │          │              │
       │ Users        │          │ Scheduled    │
       │ Notifications│          │ jobs / queue │
       │ Delivery log │          │              │
       └──────────────┘          └──────┬───────┘
                                        │
                                        ▼
                                ┌───────────────┐
                                │    Worker     │
                                │               │
                                │ Check jobs    │
                                │ Send notif.   │
                                └───────┬───────┘
                                        │
                                        ▼
                                  Notification