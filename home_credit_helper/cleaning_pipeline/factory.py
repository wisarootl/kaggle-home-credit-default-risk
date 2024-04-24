from home_credit_helper.constant import APPLICATIONS
import structlog
from ml_assemblr.main_components.transformer import Serializer

from .df import applications


cleaning_pipelines = {APPLICATIONS: applications.cleaning_pipeline}


def get_cleaning_pipeline(df_names: list[str]):
    pipeline = []
    for df_name in df_names:
        if df_name in cleaning_pipelines:
            pipeline.extend(cleaning_pipelines[df_name])
        else:
            structlog.get_logger().warning(
                f"There is no predefined cleaning pipeline for {df_name} table"
            )

    return Serializer(transformers=pipeline)
