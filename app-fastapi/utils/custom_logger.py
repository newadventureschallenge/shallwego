"""
커스텀 로그 포매터
"""
import logging
from datetime import datetime
import pytz

class KSTFormatter(logging.Formatter):
    """한국 시간대(KST)를 사용하는 로그 포매터"""
    
    def formatTime(self, record, datefmt=None):
        kst = pytz.timezone('Asia/Seoul')
        dt = datetime.fromtimestamp(record.created)
        dt = kst.localize(dt)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

def setup_logger(name: str) -> logging.Logger:
    """로거 설정
    
    Args:
        name (str): 로거 이름
        
    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 이미 핸들러가 있다면 추가하지 않음
    if logger.handlers:
        return logger
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 포매터 설정
    formatter = KSTFormatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(console_handler)
    
    return logger
