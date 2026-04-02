"""🟢 AI-GENERATED: TensorBoard logging utilities."""

from torch.utils.tensorboard import SummaryWriter


class TBLogger:
    """Lightweight wrapper around TensorBoard SummaryWriter."""

    def __init__(self, log_dir: str):
        self.writer = SummaryWriter(log_dir=log_dir)

    def log_scalar(self, tag: str, value: float, step: int):
        self.writer.add_scalar(tag, value, step)

    def log_scalars(self, main_tag: str, tag_value_dict: dict, step: int):
        self.writer.add_scalars(main_tag, tag_value_dict, step)

    def log_histogram(self, tag: str, values, step: int):
        self.writer.add_histogram(tag, values, step)

    def close(self):
        self.writer.close()
