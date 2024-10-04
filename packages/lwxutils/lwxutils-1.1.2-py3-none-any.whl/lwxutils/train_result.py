import json
import os
from datetime import datetime


class TrainingResult:

    def __init__(self, rootPath, epoch, train_loss, val_map):
        self.rootPath = rootPath
        self.resultPath = os.path.join(rootPath, "results.json")
        self.epoch = epoch
        self.train_loss = train_loss
        self.val_map = val_map
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        txt = json.dumps(self.__dict__)

        with open(self.resultPath, "w") as f:
            # print(txt)
            f.write(txt)
