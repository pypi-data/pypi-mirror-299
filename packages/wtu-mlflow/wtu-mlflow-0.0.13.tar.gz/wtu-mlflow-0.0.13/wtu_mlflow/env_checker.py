import os
import logging

logger = logging.getLogger(__name__)


def check_env_vars():
    required_env_vars = [
        "MLFLOW_S3_ENDPOINT_URL",
        "MLFLOW_TRACKING_URI",
        "MODEL_NAME",
    ]

    missing_vars = [var for var in required_env_vars if not os.environ.get(var)]

    logger.info("Required environment variables: %s", required_env_vars)
    if missing_vars:
        error_message = (
            f"다음 환경 변수들이 설정되지 않았습니다: {', '.join(missing_vars)}"
        )
        raise EnvironmentError(error_message)
