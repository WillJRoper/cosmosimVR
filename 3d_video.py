import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cm


def cartesian_to_equirectangular(pos, observer_pos):

    # Centre on the observer position
    pos -= observer_pos

    # Extract coordinates
    x = pos[:, 0]
    y = pos[:, 1]
    z = pos[:, 2]

    # Calculate radii
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)

    # First calculate angular coordinates
    theta = np.arctan2(y, x)
    phi = np.arccos(z / r)
    
    # Convert spherical coordinates to equirectangular coordinates
    longitude = theta
    latitude = np.pi / 2 - phi
    
    # Normalize longitude to the range [-pi, pi]
    longitude = (longitude + np.pi) % (2 * np.pi) - np.pi
    
    return longitude, latitude


# Define where we are getting the data from
path = "/Users/willroper/Documents/University/Animations/aXa_animations/" \
    "ani_hydro_1379.hdf5"

# Define the resolution of the image
res = (4320 * 2, 7680 * 2)

# Open the data file
hdf = h5py.File(path, "r")

# Get metadata
boxsize = hdf["Header"].attrs["BoxSize"]

# Get the particle positions
pos = hdf["PartType1/Coordinates"][:]

hdf.close()

longitude, latitude = cartesian_to_equirectangular(pos, boxsize / 2)

H, _, _ = np.histogram2d(longitude, latitude, bins=res)

plt.imshow(np.arcsinh(H), cmap="plasma")
plt.show()



