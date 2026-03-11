#!/usr/bin/env python3
"""Screen AI: capture a chosen screen region and run AI vision analysis.

Modes:
  - caption: generate a natural-language description of what is on screen.
  - detect: detect common objects on screen.

Example:
  python screen_ai.py --mode caption --interval 2
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

import mss
from PIL import Image


@dataclass
class CaptureRegion:
    left: int
    top: int
    width: int
    height: int


class ScreenAI:
    def __init__(self, mode: str, threshold: float) -> None:
        self.mode = mode
        self.threshold = threshold
        self._pipeline = None

    def _load_pipeline(self):
        if self._pipeline is not None:
            return self._pipeline

        from transformers import pipeline

        if self.mode == "caption":
            self._pipeline = pipeline(
                "image-to-text",
                model="Salesforce/blip-image-captioning-base",
            )
        elif self.mode == "detect":
            self._pipeline = pipeline(
                "object-detection",
                model="facebook/detr-resnet-50",
            )
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

        return self._pipeline

    def analyze(self, image: Image.Image) -> str:
        pipe = self._load_pipeline()

        if self.mode == "caption":
            result = pipe(image)
            if not result:
                return "No caption generated."
            caption = result[0].get("generated_text", "")
            return f"Caption: {caption.strip()}"

        detections = pipe(image)
        filtered: List[str] = []
        for item in detections:
            score = float(item.get("score", 0.0))
            if score >= self.threshold:
                label = item.get("label", "unknown")
                filtered.append(f"{label} ({score:.2f})")

        if not filtered:
            return f"No objects found over confidence {self.threshold:.2f}."

        return "Detected: " + ", ".join(filtered)


def choose_monitor(monitors: List[Dict[str, int]]) -> int:
    print("Available monitors:")
    for idx, mon in enumerate(monitors, start=1):
        print(
            f"  {idx}. left={mon['left']} top={mon['top']} "
            f"width={mon['width']} height={mon['height']}"
        )

    while True:
        raw = input("Choose monitor number: ").strip()
        if raw.isdigit():
            selected = int(raw)
            if 1 <= selected <= len(monitors):
                return selected
        print("Invalid monitor selection.")


def choose_region(default: Dict[str, int]) -> CaptureRegion:
    print("Optional region crop inside selected monitor.")
    print("Press Enter to keep monitor bounds for any field.")

    def ask(name: str, fallback: int) -> int:
        raw = input(f"{name} [{fallback}]: ").strip()
        if not raw:
            return fallback
        return int(raw)

    left = ask("left", default["left"])
    top = ask("top", default["top"])
    width = ask("width", default["width"])
    height = ask("height", default["height"])

    if width <= 0 or height <= 0:
        raise ValueError("width and height must be > 0")

    return CaptureRegion(left=left, top=top, width=width, height=height)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI vision for a chosen screen region")
    parser.add_argument(
        "--mode",
        choices=["caption", "detect"],
        default="caption",
        help="caption = describe scene, detect = detect common objects",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="seconds between captures",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="confidence threshold for --mode detect",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="analyze one frame and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ai = ScreenAI(mode=args.mode, threshold=args.threshold)

    with mss.mss() as sct:
        monitors = sct.monitors[1:]
        if not monitors:
            raise RuntimeError("No monitors found.")

        monitor_idx = choose_monitor(monitors)
        selected = monitors[monitor_idx - 1]
        region = choose_region(selected)
        region_dict = {
            "left": region.left,
            "top": region.top,
            "width": region.width,
            "height": region.height,
        }

        print("Starting capture. Press Ctrl+C to stop.")
        while True:
            raw = sct.grab(region_dict)
            frame = Image.frombytes("RGB", raw.size, raw.rgb)
            ts = time.strftime("%H:%M:%S")
            print(f"[{ts}] {ai.analyze(frame)}")

            if args.once:
                break
            time.sleep(max(0.1, args.interval))


if __name__ == "__main__":
    main()
