import math
import cairo
import numpy as np


def circle(x,y, radius):
    ctx.arc(x, y, radius, 0, 2*math.pi)
    ctx.fill()

def star(x,y,radius):
    angle = 2*math.pi/8
    ctx.arc(x, y, radius, 0, 2*math.pi)
    ctx.fill()


# Open image to an ARGB32 ImageSurface
filename = 'Shodokan_Symbol.png'

# set the canvas
# ==============
paper_width = 300
paper_height = 300
margin = 20

point_to_millimeter = 72/25.4

pdfname = "star.pdf" 
pdf = cairo.PDFSurface( pdfname, 
                        paper_width*point_to_millimeter, 
                        paper_height*point_to_millimeter
                        )

ctx = cairo.Context(pdf)
ctx.scale(point_to_millimeter, point_to_millimeter)

ox, oy = 150, 150


sang = 2*math.pi/8.0

radius = 100 

A, B, C = 0.93, 1.01, 1.01 #0.9750
ctx.set_source_rgb(0, 0, 1)
radius = radius * A# NOTE: here, for the outer flower, we have a multiply A
ax, ay = ox, oy + radius 
ctx.move_to(ax, ay) # starting point
for arc in range(1, 9):

    # bezier to half-way
    ang = arc * sang - sang/2.0
    # NOTE: factor of 0.5 to determine finishing posiiton
    dx = ox + radius*A * np.sin(ang)
    dy = oy + radius*A * np.cos(ang)
    print(dx, dy)

    # TODO: move the spline control points inwards

    bx = ox + radius * np.sin(ang - sang * 1/24) * B 
    by = oy + radius * np.cos(ang - sang * 1/24) * B

    cx = ox + radius * np.sin(ang - sang * 2/24.) * C
    cy = oy + radius * np.cos(ang - sang * 2/24.) * C

    ctx.curve_to(bx, by, cx, cy, dx, dy)
    #ctx.set_source_rgb(0, 0, 1)
    #ctx.stroke()
    #ctx.move_to(dx, dy) # starting point


    # rest of the way
    ang = arc * sang
    dx = ox + radius * np.sin(ang)
    dy = oy + radius * np.cos(ang)

    # TODO: move the spline control points inwards

    bx = ox + radius * np.sin(ang - 0.5*sang + sang * 2/24) * C 
    by = oy + radius * np.cos(ang - 0.5*sang + sang * 2/24) * C

    cx = ox + radius * np.sin(ang - 0.5*sang + sang * 1/24.) * B
    cy = oy + radius * np.cos(ang - 0.5*sang + sang * 1/24.) * B

    ctx.curve_to(bx, by, cx, cy, dx, dy)
    #ctx.set_source_rgb(0, 1, 0)
    #ctx.stroke()
    #ctx.move_to(dx, dy) # starting point


ctx.set_line_width(1.5) 
ctx.set_source_rgb(135/255.,141/255.,145/255.)
ctx.stroke()

radius = radius / A # NOTE: here, for the outer flower, we have a multiply A

for FILL in [True, False]:
    A, B, C = 0.50, 0.62, 0.52
    ctx.set_source_rgb(0, 0, 1)
    ax, ay = ox, oy + radius
    ctx.move_to(ax, ay) # starting point
    for arc in range(1, 9):

        # bezier to half-way
        ang = arc * sang - sang/2.0
        # NOTE: factor of 0.5 to determine finishing posiiton
        dx = ox + radius*A * np.sin(ang)
        dy = oy + radius*A * np.cos(ang)
        print(dx, dy)

        # TODO: move the spline control points inwards

        bx = ox + radius * np.sin(ang - sang * 4/8) * B 
        by = oy + radius * np.cos(ang - sang * 4/8) * B

        cx = ox + radius * np.sin(ang - sang * 3/8.) * C
        cy = oy + radius * np.cos(ang - sang * 3/8.) * C

        ctx.curve_to(bx, by, cx, cy, dx, dy)
        #ctx.set_source_rgb(0, 0, 1)
        #ctx.stroke()
        #ctx.move_to(dx, dy) # starting point


        # rest of the way
        ang = arc * sang
        dx = ox + radius * np.sin(ang)
        dy = oy + radius * np.cos(ang)

        # TODO: move the spline control points inwards

        bx = ox + radius * np.sin(ang - 0.5*sang + sang * 3/8) * C 
        by = oy + radius * np.cos(ang - 0.5*sang + sang * 3/8) * C

        cx = ox + radius * np.sin(ang - 0.5*sang + sang * 4/8.) * B
        cy = oy + radius * np.cos(ang - 0.5*sang + sang * 4/8.) * B

        ctx.curve_to(bx, by, cx, cy, dx, dy)
        #ctx.set_source_rgb(0, 1, 0)
        #ctx.stroke()
        #ctx.move_to(dx, dy) # starting point


    if FILL:
        ctx.set_source_rgb(16/255.,63/255.,188/255.)
        ctx.fill()
    else:
        ctx.set_line_width(1.5) 
        ctx.set_source_rgb(135/255.,141/255.,145/255.)
        ctx.stroke()

if False:
    ctx.set_source_rgb(0, 0.5, 0.5)
    ax, ay = ox, oy + radius
    ctx.move_to(ax, ay) # starting point
    for arc in range(1, 9):
        ang = arc * sang
        print(ang)

        dx = ox + radius * np.sin(ang) 
        dy = oy + radius * np.cos(ang)
        print(dx, dy)

        # TODO: move the spline control points inwards

        bx = ox + radius * np.sin(ang - sang * 3/4.) * 0.25 
        by = oy + radius * np.cos(ang - sang * 3/4.) * 0.25

        cx = ox + radius * np.sin(ang - sang * 1/4.) * 0.25
        cy = oy + radius * np.cos(ang - sang * 1/4.) * 0.25

        ctx.curve_to(bx, by, cx, cy, dx, dy)

    #ctx.stroke()
    ctx.fill()

ctx.set_source_rgb(135/255.,141/255.,145/255.)
circle(ox, oy, 15)
ctx.set_source_rgb(256.0/256., 9.0/256., 0.0/256.)
circle(ox, oy, 13.5)



#ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

if False:
    ctx.select_font_face("Courier", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    img = cairo.ImageSurface.create_from_png(filename)
    ctx.save()
    ctx.scale(0.25, 0.25)
    margin=10
    ctx.set_source_surface(img, margin, margin)
    ctx.paint()
    ctx.restore()
    #ctx.set_source_surface(img, 100, 100)
    #ctx.paint()

pdf.show_page()


#ctx.set_source_rgb(0, 0, 1)
#ax, ay = ox, oy + radius
#ctx.move_to(ax, ay) # starting point
#for arc in range(1, 9):
#    ang = arc * sang
#    print(ang)
#
#    dx = ox + radius * np.sin(ang) 
#    dy = oy + radius * np.cos(ang)
#    print(dx, dy)
#
#    # TODO: move the spline control points inwards
#
#    bx = ox + radius * np.sin(ang - sang * 3/4.) * 0.25 
#    by = oy + radius * np.cos(ang - sang * 3/4.) * 0.25
#
#    cx = ox + radius * np.sin(ang - sang * 1/4.) * 0.25
#    cy = oy + radius * np.cos(ang - sang * 1/4.) * 0.25
#
#    ctx.curve_to(bx, by, cx, cy, dx, dy)
#
##ctx.stroke()
#ctx.fill()


#factor = 0.85
#ctx.set_source_rgb(0, 1, 0)
##ctx.set_source_rgb(0, 0, 1)
#ax, ay = ox, oy + radius*factor
#ctx.move_to(ax, ay) # starting point
#for arc in range(1, 9):
#    ang = arc * sang
#    print(ang)
#
#    dx = ox + radius*factor * np.sin(ang) 
#    dy = oy + radius*factor * np.cos(ang)
#    print(dx, dy)
#
#    # TODO: move the spline control points inwards
#
#    bx = ox + radius*factor * np.sin(ang - sang * 6/8.) * 0.4 
#    by = oy + radius*factor * np.cos(ang - sang * 6/8.) * 0.4
#
#    cx = ox + radius*factor * np.sin(ang - sang * 2/8.) * 0.4
#    cy = oy + radius*factor * np.cos(ang - sang * 2/8.) * 0.4
#
#    ctx.curve_to(bx, by, cx, cy, dx, dy)
#
#ctx.stroke()
