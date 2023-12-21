import logging
from pathlib import Path
import hydra
import pandas as pd

from src.conf import TrainConfig
from src.metric import score

LOGGER = logging.getLogger(Path(__file__).name)
PROJECT_NAME = "Santa-2023"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s:%(name)s - %(message)s",
)


@hydra.main(config_path="conf", config_name="train", version_base="1.2")
def main(cfg: TrainConfig):
    LOGGER.info(f"Project name: {PROJECT_NAME}")
    submission = pd.read_csv(Path(cfg.dir.sub_dir) / "submission.csv")
    solution = pd.read_csv(Path(cfg.dir.data_dir) / "puzzles.csv")

    score_val = score(
        solution,
        submission,
        series_id_column_name="id",
        moves_column_name="moves",
        puzzle_info_path=Path(cfg.dir.data_dir) / "puzzle_info.csv",
    )
    LOGGER.info(f"Score: {score_val}")

    return


if __name__ == "__main__":
    main()
