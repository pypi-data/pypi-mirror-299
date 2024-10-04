"""
Data Ingestion Module
--------------------------------------
해당 모듈은 데이터를 불러오는 기능을 제공하는 모듈입니다.
데이터 추출단계에서부터 미리 정의된 데이터를 불러오는 것을 추천 드리며, 그렇지 않더라도 최대한 일반화하여 진행이 가능하도록 Function을 구성하였습니다.
"""

def convert_and_save_to_parquet():
    """
    txt, csv 등의 파일 형태를 pq 형태로 저장해주는 함수입니다.
    """
    pass

def capitalize_column():
    """
    dataframe 칼럼들을 모두 대문자로 변환
    """
    pass

def typecast():
    """
    string, int, float 등 각 칼럼을 인식해 typecast 해주는 함수. Null 값 같은 경우 coerce로 그대로 두는 형태를 선정
    """
    pass

def partition_data():
    """
    Scorecard (ex. 세그먼트) 별로 데이터를 개별 파일로 나눠주는 방식 - 이후 진행 시 Scorecard를 입력하는 등의 진행방법 접목 필요
    """
    pass