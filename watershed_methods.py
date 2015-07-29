from skimage.filters import threshold_otsu
from skimage.util import img_as_float
from skimage.color import rgb2grey
from skimage import io
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import numpy as np
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage.measure import regionprops


def watershed_counter(path_image):
    # load the image and convert it to a floating point data type
    rgb_image = img_as_float(io.imread(path_image))
    image = rgb2grey(rgb_image)

    bin_image = image > threshold_otsu(image)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 2.5))
    ax1.imshow(image, cmap=plt.cm.gray)
    ax1.set_title('Original Image')
    ax1.axis('off')

    ax2.hist(image)
    ax2.set_title('Otsu Thresholded Histogram')
    ax2.axvline(threshold_otsu(image), color='r')

    ax3.imshow(bin_image, cmap=plt.cm.gray)
    ax3.set_title('Thresholded Image')
    ax3.axis('off')

    # Now we want to separate the two objects in image
    # Generate the markers as local maxima of the distance to the background

    distance = ndi.distance_transform_edt(bin_image)
    local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=bin_image)
    markers = ndi.label(local_maxi)[0]
    labels = watershed(distance, markers, mask=bin_image)

    regions = regionprops(labels)
    regions = [r for r in regions if r.area > 50]
    num = len(regions)

    fig, axes = plt.subplots(ncols=4, figsize=(8, 2.7))
    ax0, ax1, ax2, ax3 = axes

    ax0.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
    ax0.set_title('Overlapping objects')
    ax1.imshow(-distance, cmap=plt.cm.jet, interpolation='nearest')
    ax1.set_title('Distances')
    ax2.imshow(labels, cmap=plt.cm.spectral, interpolation='nearest')
    ax2.set_title(str(num) + ' Total Objects')
    ax3.imshow(rgb_image, cmap=plt.cm.gray, interpolation='nearest')
    ax3.contour(labels, [0.5], linewidths=1.2, colors='y')
    ax3.axis('off')

    for ax in axes:
        ax.axis('off')

    fig.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,
                        right=1)

    print num

    plt.show()

watershed_counter('temp_crop.png')