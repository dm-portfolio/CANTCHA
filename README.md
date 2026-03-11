# CAN'TCHA

![STATIC BADGE](https://img.shields.io/badge/made_with-Python-blue)<br><br>
Testing the limits of a good old CAPTCHA, using the exact thing it prevents.

## What is a CAPTCHA? 

CAPTCHAs, or **C**ompletely **A**utomated **P**ublic **T**uring test to tell **C**omputers and **H**umans **A**part, are security tools used on websites to determine whether a user is a real human or an automated program (bot). They usually appear when signing up for accounts, submitting forms, or logging in. A CAPTCHA works by presenting a task that is easy for humans but difficult for automated scripts, such as identifying distorted letters, selecting images that contain a specific object (like traffic lights), or checking a box that triggers behavioral analysis. Modern systems often analyze mouse movements, typing patterns, and other subtle behaviors to decide if the user is likely human.

The concept of CAPTCHA was developed in the early 2000s by researchers at Carnegie Mellon University, including Luis von Ahn, Manuel Blum, and Nicholas Hopper. Early CAPTCHAs mostly required users to type distorted text from an image, which computers had difficulty recognizing at the time. Over time, as artificial intelligence improved at reading text, CAPTCHA systems evolved into more complex image-recognition and behavior-based tests. Today, systems like Google’s reCAPTCHA may even run in the background, silently analyzing user activity to verify that the interaction is coming from a human rather than a bot.

This project attempts to change that.

## Screen AI (new)

`screen_ai.py` is a Python program that can watch a chosen screen or region and run AI vision on each captured frame.

### Features

- Choose which monitor to analyze.
- Optionally crop to a custom region.
- `caption` mode: natural-language descriptions using BLIP.
- `detect` mode: common object detection using DETR.
- Run continuously or once.

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

```bash
python screen_ai.py --mode caption --interval 2
```

Or object detection mode:

```bash
python screen_ai.py --mode detect --threshold 0.85 --interval 1.5
```

Single frame only:

```bash
python screen_ai.py --mode caption --once
```

When started, the script asks you to choose a monitor, then optionally change the capture bounds.