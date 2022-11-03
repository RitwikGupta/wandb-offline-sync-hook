from __future__ import annotations

from os import PathLike
from pathlib import Path

from ray.tune.logger import LoggerCallback
from ray.tune.trial import Trial

from wandb_osh.util.log import logger

_comm_default_dir = Path("~/.wandb_osh_command_dir").expanduser()


class TriggerWandbSyncHook(LoggerCallback):
    def __init__(self, communication_dir: PathLike = _comm_default_dir):
        """Hook to be used when interfacing wandb with ray tune.

        Args:
            communication_dir: Directory used for communication with wandb-osh.
        """
        super().__init__()
        self.communication_dir = Path(communication_dir)
        self.communication_dir.mkdir(parents=True, exist_ok=True)

    def log_trial_result(self, iteration: int, trial: Trial, result: dict):
        trial_dir = Path(trial.logdir)
        command_file = self.communication_dir / f"{trial_dir.name}.command"
        if command_file.is_file():
            logger.warning(
                "Syncing not active or too slow: Command %s file still exists",
                command_file,
            )
        command_file.touch(exist_ok=True)
        command_file.write_text(trial_dir.resolve().as_posix())
        logger.debug("Wrote command file %s", command_file)
