from skimage import data, filters, util
from scipy import ndimage
import matplotlib.pyplot as plt

img = data.camera()
noisy = util.random_noise(img, mode='s&p', amount=0.05)

median = ndimage.median_filter(noisy, size=3)
laplace = ndimage.laplace(img.astype(float))
sharpened = img - 0.7 * laplace   # Laplacian sharpening

fig, ax = plt.subplots(1, 4, figsize=(14, 4))
for a, im, t in zip(ax, [noisy, median, laplace, sharpened],
                    ['Noisy', 'Median', 'Laplacian', 'Sharpened']):
    a.imshow(im, cmap='gray'); a.set_title(t); a.axis('off')
plt.show()