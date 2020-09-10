# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt

# %%
# read image, convert to RGB, and show
img = cv2.imread(
    filename='hands-on-machine-learning.jpg',
    flags=cv2.IMREAD_COLOR,
)

h, w, c = img.shape
print(f'Image shape: {h}H x {w}W x {c}C')

img.dtype

img = cv2.cvtColor(
    src=img,
    code=cv2.COLOR_BGR2RGB,
)


def show_image(img, **kwargs):
    """
    Show an RGB numpy array of an image without any interpolation
    """
    plt.subplot()
    plt.axis('off')
    plt.imshow(
        X=img,
        interpolation='none',
        **kwargs
    )


show_image(img)
# %%
# crop image and show
ymin, ymax = 200, 780
xmin, xmax = 100, 1000

img = img[
    int(ymin): int(ymax),
    int(xmin): int(xmax),
    :
]

h, w, c = img.shape
print(f'Image shape: {h}H x {w}W x {c}C')

show_image(img)

# %%
# add border to cropped image
img_border = cv2.copyMakeBorder(
    src=img,
    top=10,
    bottom=10,
    left=10,
    right=10,
    borderType=cv2.BORDER_CONSTANT,
    value=(255, 255, 255),
)

h, w, c = img_border.shape
print(f'Image shape: {h}H x {w}W x {c}C')

show_image(img_border)

# %%
MAX_PIX = 800


def resize_image(img, flag):
    """
    Resize an RGB numpy array of an image, either along the height or the width, and keep its aspect ratio. Show restult.
    """
    h, w, c = img.shape

    if flag == 'h':
        dsize = (int((MAX_PIX * w) / h), int(MAX_PIX))
    else:
        dsize = (int(MAX_PIX), int((MAX_PIX * h) / w))

    img_resized = cv2.resize(
        src=img,
        dsize=dsize,
        interpolation=cv2.INTER_CUBIC,
    )

    h, w, c = img_resized.shape
    print(f'Image shape: {h}H x {w}W x {c}C')

    show_image(img_resized)

    return img_resized


if h > MAX_PIX:
    img_resized = resize_image(img, 'h')

if w > MAX_PIX:
    img_resized = resize_image(img, 'w')


# %%
def apply_morphology(img, method):
    """
    Apply a morphological operation, either opening (i.e. erosion followed by dilation) or closing (i.e. dilation followed by erosion). Show result.

    Opening is useful for removing noise.
    Closing is useful for closing small holes.

    """
    if method == 'open':
        op = cv2.MORPH_OPEN
    elif method == 'close':
        op = cv2.MORPH_CLOSE

    img_morphology = cv2.morphologyEx(
        src=img,
        op=op,
        kernel=np.ones((5, 5), np.uint8),
    )

    show_image(img_morphology)

    return img_morphology


img_opened = apply_morphology(img, 'open')
img_close = apply_morphology(img, 'close')

# %%
"""
Apply Gaussian smoothing which is useful for removing high frequency content (e.g. noise).
"""
img_gaussian = cv2.GaussianBlur(
    src=img,
    ksize=(5, 5),
    sigmaX=0,
    sigmaY=0,
)

show_image(img_gaussian)


# %%
def apply_adaptive_threshold(img, method):
    """
    Apply adaptive thresholding, either Gaussian (threshold value is the weighted sum of neighbourhood values where weights are a Gaussian window) or mean (threshold value is the mean of neighbourhood area). Show result.

    Adaptive thresholding is useful when the image has different lighting conditions in different areas
    """
    img = cv2.cvtColor(
        src=img,
        code=cv2.COLOR_RGB2GRAY,
    )

    if method == 'gaussian':
        adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    elif method == 'mean':
        adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C

    img_adaptive = cv2.adaptiveThreshold(
        src=img,
        maxValue=255,
        adaptiveMethod=adaptive_method,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=11,
        C=2,
    )

    show_image(img_adaptive, cmap='gray')

    return img_adaptive


img_adaptive_gaussian = apply_adaptive_threshold(img, 'gaussian')
img_adaptive_mean = apply_adaptive_threshold(img, 'mean')


# %%
def apply_sobel(img, direction):
    """
    Apply Sobel filter of first order (i.e. 1st derivative), either along x (horizontally) or y (vertically).

    Sobel filters are useful to detect horizontal or vertical edges and are resistant to noise.
    """
    img = cv2.cvtColor(
        src=img,
        code=cv2.COLOR_RGB2GRAY,
    )

    if direction == 'h':
        dx, dy = 0, 1

    elif direction == 'v':
        dx, dy = 1, 0

    img_sobel = cv2.Sobel(
        src=img,
        ddepth=cv2.CV_64F,
        dx=dx,
        dy=dy,
        ksize=3,
    )

    return img_sobel


img_sobel_composit = apply_sobel(img, 'h') + apply_sobel(img, 'v')
show_image(img_sobel_composit, cmap='gray')


# %%
def apply_laplacian(img):
    """
    Apply Laplacian filter of second order (i.e. 2nd derivative), along x (horizontally) and y (vertically). Show result.

    Laplacian filters are useful to detect edges.
    """
    img = cv2.cvtColor(
        src=img,
        code=cv2.COLOR_RGB2GRAY,
    )

    img_laplacian = np.uint8(
        np.absolute(
            cv2.Laplacian(
                src=img,
                ddepth=cv2.CV_64F,
            )
        )
    )

    show_image(img_laplacian, cmap='gray')

    return img_laplacian


img_laplacian = apply_laplacian(img)


# %%
_, buf = cv2.imencode(
    ext=".PNG",
    img=img,
)

data = buf.tostring()

img = cv2.imdecode(
    buf=buf,
    flags=cv2.IMREAD_UNCHANGED,
)

# %%
