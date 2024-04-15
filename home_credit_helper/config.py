from pathlib import Path

from pydantic_settings import BaseSettings


class HomeCreditRunnerConfigs(BaseSettings):
    test_mode: bool = True
    load_data_row_nums: int | None = None
    data_path: Path = Path(__file__).parent.parent / ".cache" / "data"
    pk: str | None = "SK_ID_CURR"
    relevant_pks: tuple | None = None


cfg = HomeCreditRunnerConfigs()
cfg_small_dataset = HomeCreditRunnerConfigs(load_data_row_nums=10000)
