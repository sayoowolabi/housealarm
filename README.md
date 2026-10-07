# [House Alarm!] — Motion Sticker Extraction

An image-processing project for IDSP 1701 (Image Processing) at TU Dublin.

Upload fixed-camera footage, such as indoor CCTV, and the system detects
whatever is moving and cuts it out as a "sticker", like the iPhone sticker
feature, producing a timeline of cutouts in the order they appeared.

The project uses classical image-processing techniques only (no machine learning).

## Team
- Patrycja Palka
- Folasayo Owolabi
- Chloe Vegiga


## How it's supposed to work
1. **Preprocessing:** greyscale, blur, contrast enhancement for night footage
2. **Motion detection:** compare frames to find what changed
3. **Mask cleanup:** thresholding and morphology
4. **Cutout:** keep the moving object, make the background transparent,
   add a white sticker outline

## Setup
Requires Python 3.14.

```
git clone [repo URL]
cd housealarm
py -3.14 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running
```
streamlit run app.py
```
Upload a video in the browser window that opens, then click **Make stickers**.

## Test footage
Videos are not stored in this repo because of their size. Upload them into a `footage/` folder in the
project root.

## Project structure
- `app.py`: Streamlit interface (upload, display, download)
- `stickers.py`: the image-processing pipeline
- `requirements.txt`: libraries to install

## Status
- [x] Project setup and interface starter
- [ ] Motion detection
- [ ] Mask cleanup and cutouts
- [ ] Night-time footage handling
- [ ] Evaluation

## References
- Streamlit 
- OpenCV