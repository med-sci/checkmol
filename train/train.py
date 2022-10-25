import os
from random import random, randint
import mlflow
from mlflow import  log_metric, log_param, log_artifacts

os.environ['MLFLOW_TRACKING_URI'] = 'http://mlflow-svc:5000/'

if __name__ == "__main__":
    
    with mlflow.start_run() as run:
        print("Running mlflow_tracking.py")
        for _ in range(10):
            with mlflow.start_run(nested=True) as run:
                log_param("param1", randint(0, 100))
                
                log_metric("foo", random())

        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        with open("outputs/test.txt", "w") as f:
            f.write("hello world!")

        log_artifacts("outputs")

