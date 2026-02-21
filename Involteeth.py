
import cadquery as cq
from cadquery.vis import show
import numpy as np


#All Declarations Here. Change of Variables Permitted

Helical_Angle = 6
Thickness = 3
Mod = 2
Inner_Hole_Diameter = 3
Z_int = 15 # Number of teeth as Integer value, no other value is permissible
try:
    Z_int = int(Z_int)
except:
    ValueError("Z_int must be an integer.")


#All Constants Necessary. DO NOT CHANGE

pres_angle = 20 #deg
pi = np.pi

##INVOLUTE PROFILE GENERATOR##

D_Pitch = Mod*Z_int
D_Add = D_Pitch + Mod*2
D_Ded = D_Pitch - Mod*2.5 #root or dedendum circle
D_Base = D_Pitch*np.cos(np.deg2rad(pres_angle))


#DEFINE RANGE FOR INVOLUTE

def x_involute(theta):
    return D_Base * (np.cos(theta) + theta * np.sin(theta))/2

def y_involute(theta):
    return D_Base * (np.sin(theta) - theta * np.cos(theta)) / 2

def radius(t):
    return np.sqrt(pow(x_involute(t),2) + pow(y_involute(t),2))

def rotatetuple(x, y, angle):
    angle = np.deg2rad(angle)
    return [x*np.cos(angle) - y*np.sin(angle), x*np.sin(angle) + y*np.cos(angle)]

i= 0 ## 'i' can start with a more reasonable guess
     ## to decrease compute time
while radius(i) < D_Add/2:
    i += 0.01

turn_by = 90.0/Z_int*-1

list_of_x = x_involute(np.linspace(0, i, 10))
list_of_y = y_involute(np.linspace(0, i, 10))

[list_of_x, list_of_y] = rotatetuple(list_of_x, list_of_y, turn_by)

list_of_z = np.zeros(len(list_of_x))
tuple_xy = np.array((list_of_x, list_of_y)).T
tuple_xy_inv = np.array((list_of_x, -1*list_of_y))



half_profile = (cq.Workplane()
                    .spline(tuple_xy)
                    .vLineTo(0)
                    .hLineTo(0.1)
                    .close()
)

profile_solid = half_profile.twistExtrude(Thickness, Helical_Angle, combine=True)
mirror_profile = half_profile.mirrorX().twistExtrude(Thickness, Helical_Angle, combine="a")
profile_solid = profile_solid.union(toUnion=mirror_profile).clean()

rotate_iter = 360.0/Z_int

iterate_profile = profile_solid.rotate((0, 0, 0), (0, 0 ,1), 360/Z_int)
for i in range(Z_int):
    placeholder = iterate_profile
    iterate_profile = iterate_profile.rotate((0, 0, 0), (0, 0 ,1), 360/Z_int)
    iterate_profile = iterate_profile.union(toUnion=placeholder).clean()

base_shape = cq.Workplane().circle(D_Ded/2).extrude(Thickness)

hole_shape = cq.Workplane().circle(Inner_Hole_Diameter/2).extrude(Thickness)

no_hole_final_shape = iterate_profile.union(toUnion=base_shape).clean()
final_shape = no_hole_final_shape.cut(hole_shape)
show(final_shape)