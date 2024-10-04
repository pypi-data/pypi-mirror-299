"""
Model Engineering Module
--------------------------------------
해당 모듈은 모델링을 수행하는 모듈입니다.
AutoML 및 MLFlow를 활용하여 모형을 만드는 함수를 구현하였으며, 해당 함수를 활용하여 진행하시면 됩니다.
"""

def init_mlflow():
    """
    MLFlow 실행
    """
    pass

def pycaret_automl():
    """
    AutoML을 위해 Pycaret 실행
    """
    pass

def save_best_model():
    """
    평가 메트릭에 따라 가장 성능이 좋은 모델을 .pkl 파일로 저장
    """
    pass

def save_experiment_parameters():
    """
    Kedro에 사용할 실험 매개변수 저장
    """
    pass

def output_scored_predictions():
    """
    저장된 최고의 모델을 사용하여 각 행에 대한 예측 점수 출력
    """
    pass

def save_scored_predictions():
    """
    향후 사용을 위해 예측 점수를 .json 파일로 저장
    """
    pass

def load_oot_dataset():
    """
    훈련 검증 테스트 데이터셋 로드
    """
    pass

def automl_pipeline():
    """
    Pycaret을 사용하여 자동화된 모델 선택 및 튜닝 수행
    """
    pass

def mlflow_pipeline():
    """
    실험 추적 및 모델 라이프사이클 관리를 위해 MLFlow 사용
    """
    pass

def cross_validation():
    """
    강력한 모델 평가를 위해 교차 검증 기법 적용 (e.g. k-fold stratified k-fold)
    """
    pass

def hyperparameter_optimization():
    """
    그리드 서치 랜덤 서치 베이지안 최적화와 같은 방법을 사용하여 모델 성능 미세 조정
    """
    pass

def model_versioning_pipeline():
    """
    모델의 버전 관리하고 추적 가능성 보장
    """
    pass

def load_best_model():
    """
    Load best model from previously built model
    """
    pass