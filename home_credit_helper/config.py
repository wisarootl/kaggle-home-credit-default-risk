from pathlib import Path

from pydantic_settings import BaseSettings

root_dir = Path(__file__).parent.parent


class HomeCreditRunnerConfigs(BaseSettings):
    test_mode: bool = True
    load_data_row_nums: int | None = None
    data_path: Path = root_dir / ".cache" / "data"
    research_cache_path: Path = root_dir / "research" / ".cache" / "state"
    submission_path: Path = root_dir / "submission" / "submission.csv"
    pk: str | None = "SK_ID_CURR"
    relevant_pks: tuple | None = None


cfg = HomeCreditRunnerConfigs()
cfg_small_dataset = HomeCreditRunnerConfigs(
    load_data_row_nums=10000, research_cache_path=root_dir / "research" / ".cache" / "small"
)

# cfg = cfg_small_dataset
