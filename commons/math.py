import math
import numpy as np

from scipy.signal import savgol_filter

def _fix_angle(theta_1, theta_2):
    rate_theta = (theta_2 - theta_1)
  
    if (rate_theta > math.pi ):
        rate_theta -= 2 * math.pi
    elif (rate_theta < -math.pi):
        rate_theta += 2 * math.pi

    return rate_theta


def angular_speed(_list, _fps):
    if len(_list) <= 1:
        return 0
    
    speed_fbf = [
        _fix_angle(t0, t1) for t0, t1 
        in zip(
            _list, 
            list(_list)[1:]
        )
    ]

    return _fps * (sum(speed_fbf)/len(speed_fbf))


def speed(_list, _fps):
    if len(_list) <= 1:
        return 0
    
    speed_fbf = [
        (t1 - t0) for t0, t1 
        in zip(
            _list, 
            list(_list)[1:]
        ) if abs((t1 - t0)) < 0.1
        # considerando que o jogo funciona a 60 fps
        # limitar 0.1 m/f aqui é dizer que é impossivel
        # o robo fazer 6 m/s (0.1 [m][f⁻¹] * 60 [f][s⁻¹] = 6[m][s⁻¹])
    ]

    return _fps * (sum(speed_fbf)/len(speed_fbf))


def unit_vector(vector):
    """ Returns the unit vector of the vector."""
    if np.linalg.norm(vector) == 0:
        return np.array([0, 0])
    return vector / np.linalg.norm(vector)

def rotate_via_numpy(xy, radians):
    """Use numpy to build a rotation matrix and take the dot product."""
    x, y = xy
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [x, y])

    return float(m.T[0]), float(m.T[1])

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle_between(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

from numpy import arccos, array, dot, pi, cross
from numpy.linalg import det, norm

def distance(A, B, P):
    """ segment line AB, point P, where each one is an array([x, y]) """
    A = np.array(A)
    B = np.array(B)
    P = np.array(P)
    if all(A == P) or all(B == P) or all(A == B):
        return 0
    if arccos(dot((P - A) / norm(P - A), (B - A) / norm(B - A))) > pi / 2:
        return norm(P - A)
    if arccos(dot((P - B) / norm(P - B), (A - B) / norm(A - B))) > pi / 2:
        return norm(P - B)
    return norm(cross(A-B, A-P))/norm(B-A)