"""
scbk_mlops package initialization.
"""

__version__ = "0.1.0"
__author__ = "Jong Hwa Lee, Jin Young Kim"
__all__ = ["eda", "ingestion", "reporting", "data_engineering", "model_engineering", "model_evaluation", "model_monitoring"]

# Logging initialization
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"SCBK-MLOps 라이브러리 로딩중, authors 데이터분석부 {__author__} version {__version__}")