"""Prepare the full v2 narration with the same takes as the approved screen sample."""
import argparse
import asyncio
from pathlib import Path

from review_voice import narrate


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('media', type=Path)
    asyncio.run(narrate(parser.parse_args().media, full=True))
