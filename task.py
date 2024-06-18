class Task:
    def __init__(self, id, time, status='not_completed'):
        self.time = time
        self.status = status
        self.id = id

    # def __repr__(self):
    #     return f"time={self.time} status={self.status} \n"

    # def __str__(self):
    #     return f"time={self.time} status={self.status} \n"

    def __repr__(self):
        return f"id={self.id}\n"

    def __str__(self):
        return f"id={self.id}\n"
