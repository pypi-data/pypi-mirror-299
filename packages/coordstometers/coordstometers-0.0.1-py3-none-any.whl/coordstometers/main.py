import numpy as np

# NOTE: GPS coords go lat lon, meters cords go lon lat, because lon is the horizontal
# Don't get confused by the flip


def get_scale(center_coord):
    # get conversion factor for lat lon to meters at a certain point on earth
    earth_circum = 40030174  # circumference of the earth in meters
    lat_scale = earth_circum / 360  # math
    lon_scale = float(lat_scale * np.cos(np.deg2rad(center_coord[0])))
    scale = np.array([lat_scale, lon_scale])
    return scale


def coords_to_meters(pts_lat_lon, center_coord):
    pts_inter = pts_lat_lon.copy()  #  copy the input
    pts_inter -= center_coord  # translate the points (center)
    pts_inter = pts_inter * get_scale(center_coord)  # scale ()
    pts_inter = pts_inter[:, ::-1]  # switch x and y
    pts_meters = pts_inter  # rename var
    return pts_meters


def meters_to_coords(pts_meters, center_coord):
    pts_inter = pts_meters.copy()  # copy the input
    pts_inter = pts_inter[:, ::-1]  # switch x and y
    pts_inter = pts_inter / get_scale(center_coord)  # scale
    pts_inter += center_coord  # translate the points (uncenter)
    pts_lat_lon = pts_inter  # rename var
    return pts_lat_lon
