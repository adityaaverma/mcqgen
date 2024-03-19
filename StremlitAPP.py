import logging
import os
from datetime import datetime


LOG_FILE=f"{datetime.now().strftime{'%m_%d_%y_%H_%M_%S'}}.log"
log_path=os.path.join(os.getcwd(),"logs")

LOG_FILEPATH=os.makedirs(log_path,exist_ok=True)\


logging(level=logging.INFO,
        filename=LOG_FILEPATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
        )
