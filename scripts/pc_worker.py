"""PC 자동 일꾼 — 뺐습니다 (2026-11-21 사용자: "자동일꾼 그냥 빼 나 그냥 로컬에서 전부 영상작업 할테니까").
호기심 그림·렌더는 Claude 앱의 호기심 예약 작업(config/local_routines/curiosity.md)이 이 PC 에서 직접 합니다.
예전에 등록된 Windows 예약(ytflow-pc-worker)이 이 파일을 실행하면, 아무 일도 하지 않고 그 예약을 지웁니다.
"""
import os
import subprocess
import sys

if __name__ == "__main__":
    if os.name == "nt":
        subprocess.run(["schtasks", "/Delete", "/TN", "ytflow-pc-worker", "/F"], capture_output=True)
    sys.exit(0)
