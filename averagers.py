class OneByOne:
    def __init__(self, keys):
        self.keys = keys
        self.data = {}
        self.sims = 0
        for key in self.keys:
            self.data[key] = None

    def add_data(self, new_data):  # assume all data has same times and size
        for key in self.keys:
            if self.data[key] is None:
                self.data[key] = new_data[key]
            else:
                for point in range(len(self.data[key])):
                    self.data[point] = ((self.data[key][point] * self.sims) + new_data[key][point]) / (self.sims + 1)
        self.sims += 1


def averager(data):  # takes a list of lists of comparable data as input
    size = len(data[0])
    reps = len(data)
    total = [0 for _ in range(size)]
    for sim in data:
        for i in range(size):
            total[i] += sim[i]
    for i in range(size):
        total[i] /= reps


