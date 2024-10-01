import logging
import mlflow
import onnx
import json
import os

from mlflow.models.signature import infer_signature, ModelSignature
from mlflow.models.utils import ModelInputExample
from .base_mlflow_client import BaseMLflowClient
from .schema import Schema

"""
ModelInputExample
    mlflow 1.x 버전에서는 from mlflow.models.utils import ModelInputExample
    mlflow 2.x 버전에서는 from mlflow.models.signature import ModelInputExample
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OnnxClient(BaseMLflowClient):
    def __init__(self):
        super().__init__()

    def upload(
        self,
        model,
        input_example: Schema,
        output_example: Schema,
    ):
        onnx.checker.check_model(model)
        self._log_tensor(model)

        signature = infer_signature(
            model_input=input_example,
            model_output=output_example,
        )

        path = self._log_model(
            model=model,
            signature=signature,
            input_example=input_example,
        )

        if self.isProduction is False:
            logging.warn(
                """
                You are trying to upload a model in a development environment.
                If this is a mistake, please set the PROFILE environment variable to 'prod' or 'production'.
                Otherwise, you can ignore this message. The model will not be uploaded.
                """
            )
            return

        missing_envs = [
            var
            for var in [
                "AWS_ACCESS_KEY_ID",
                "AWS_SECRET_ACCESS_KEY",
                "RABBIT_ENDPOINT_URL",
                "RABBIT_MODEL_UPLOAD_TOPIC",
                "TRAIN_ID",
            ]
            if not os.environ.get(var)
        ]
        if missing_envs:
            error_message = (
                f"다음 환경 변수들이 설정되지 않았습니다: {', '.join(missing_envs)}"
            )
            raise EnvironmentError(error_message)

        message = json.dumps({"train_id": os.environ["TRAIN_ID"], "full_path": path})

        try:
            self._channel.basic_publish(
                exchange=self._uploadModelExchange,
                routing_key=self._uploadModelExchange,
                body=message,
            )
            logger.info("Model uploaded to RabbitMQ: %s", message)
        except Exception as e:
            logger.error("Failed to upload model to RabbitMQ: %s", e)

    def _log_tensor(self, onnx_model):
        """
        onnx.load 로 로드된 모델을 통해 input tensor와 output tensor의 정보를 출력합니다.
        """
        for input_tensor in onnx_model.graph.input:
            input_name = input_tensor.name

            input_type = self.get_triton_compatible_type(input_tensor.type.tensor_type)
            input_shape = [
                dim.dim_value for dim in input_tensor.type.tensor_type.shape.dim
            ]

            print(f"Input tensor name: {input_name}")
            print(f"Data type: {input_type}")
            print(f"Shape: {input_shape}")

        for output_tensor in onnx_model.graph.output:
            output_name = output_tensor.name
            output_type = self.get_triton_compatible_type(
                output_tensor.type.tensor_type
            )
            output_shape = [
                dim.dim_value for dim in output_tensor.type.tensor_type.shape.dim
            ]

            print(f"Output tensor name: {output_name}")
            print(f"Data type: {output_type}")
            print(f"Shape: {output_shape}")

    def _log_model(
        self,
        model,
        signature: ModelSignature,
        input_example: ModelInputExample,
    ) -> str:
        model_name = os.environ["MODEL_NAME"]

        with mlflow.start_run():
            mlflow.onnx.log_model(
                onnx_model=model,
                artifact_path=model_name,
                signature=signature,
                input_example=input_example,
            )

            artifact_uri = mlflow.get_artifact_uri()
            model_full_path = f"{artifact_uri}/{model_name}"

            logger.info("Full path of the logged model: %s", model_full_path)
            return model_full_path
