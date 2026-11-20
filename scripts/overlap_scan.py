"""글자 겹침 검사 — ytflow/stages/overlapqa.py 를 부름 (hybrid 렌더 끝에 자동으로도 돎)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ytflow.stages.overlapqa import main  # noqa: E402

if __name__ == "__main__":
    main()
