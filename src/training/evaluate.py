# Evaluate on the validation set (by creating a data_val.yaml)

from src.models import model
model_ = model.model
model_.val(data="data_val.yaml")  # data_val.yaml points to val/
