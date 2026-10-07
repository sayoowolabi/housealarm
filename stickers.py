"""
stickers.py - the image-processing side of the project.

The interface (app.py) only calls extract_stickers(). Everything that turns a
video into sticker cutouts lives here, so this file can be developed, tested
and submitted independently of the interface.

CURRENT STATE: placeholder. It just samples frames and returns them whole
(fully opaque), so the interface can be built and tested end to end today.
Replace the body of make_sticker() with the team's own pipeline as each
part of the research is finished.
"""

import cv2
import numpy as np


def make_sticker(frame, prev_gray):
    """
    Turn one frame into a sticker (BGRA image, transparent background),
    or return None if nothing is moving.

    TODO - our pipeline, built up from the research:
      1. Preprocess: greyscale, blur, night-frame check,
         CLAHE on night frames.
      2. Motion mask: compare with the previous frame or a
         running-average background, then threshold.
      3. Clean the mask: morphological opening/closing,
         keep the largest contour, fill it in.
      4. Enhance the object: contrast (CLAHE) and sharpening (unsharp mask).
      5. Cut it out: use the mask as the alpha channel, crop to the
         bounding box, add a white outline by dilating the mask.
    """

    gray = preprocess_frame(frame)

    # Placeholder: whole frame, fully opaque (alpha = 255 everywhere).
    sticker = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return sticker

def preprocess_frame(frame):
    """
    Preprocess a video frame before motion detection.

    Converts the frame to greyscale and applies Gaussian blur to reduce
    noise. The average brightness is then checked to determine whether
    the frame is dark. If it is a night frame, CLAHE is applied to
    improve the contrast and make objects easier to distinguish from
    the background.

    Parameters:
        frame: The original colour video frame.

    Returns:
        The preprocessed greyscale frame.
    """
    #Converts each video frame from colour to greyscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Applies a small Gaussian blur to remove tiny pixel-level changes 
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    #Calculates the average brightness of the frame.
    if np.mean(gray) < 70:
        #increases the contrast of dark footage to better distinguish between objects
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

    return gray

def extract_stickers(video_path, every_n_frames=15, progress_callback=None):
    """
    Read a video and return a chronological list of (time_in_seconds, sticker).

    every_n_frames: only process every Nth frame, so the output isn't
                    hundreds of near-identical stickers.
    progress_callback: optional function(fraction) used by the interface
                       to update a progress bar.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open the video file.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25          # fall back if unknown
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1

    stickers = []
    prev_gray = None
    index = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break                                   # end of video

        if index % every_n_frames == 0:
            sticker = make_sticker(frame, prev_gray)
            if sticker is not None:
                stickers.append((index / fps, sticker))

        #compare preprocessed previous frame VS preprocessed current frame
        prev_gray = preprocess_frame(frame)
        index += 1
        if progress_callback:
            progress_callback(min(index / total, 1.0))

    cap.release()
    return stickers