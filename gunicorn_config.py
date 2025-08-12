bind = "0.0.0.0:8000"
workers = 4
timeout = 30


def post_fork(server, worker):
    from application.jobs import JobRegistry
    JobRegistry.start_all()


def worker_exit(server, worker):
    from application.jobs import JobRegistry
    print(f"Stopping jobs in worker PID {worker.pid}")
    JobRegistry.stop_all()
