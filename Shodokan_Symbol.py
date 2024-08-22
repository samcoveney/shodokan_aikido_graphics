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

# Open image to an ARGB32 ImageSurface
TEST = False

if TEST:
    filename = 'Shodokan_Symbol.png'
    ctx.select_font_face("Courier", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    img = cairo.ImageSurface.create_from_png(filename)
    ctx.save()
    ctx.scale(0.25, 0.25)
    margin=10
    ctx.set_source_surface(img, margin, margin+15)
    ctx.paint()
    ctx.restore()
    #ctx.set_source_surface(img, 100, 100)
    #ctx.paint()


# ---- PDF drawing ----


ox, oy = 150, 150


sang = 2*math.pi/8.0

radius = 140 


if TEST == False:
    RED = [256.0/256., 9.0/256., 0.0/256.]
    BLUE = [16/255.,63/255.,188/255.]
    GRAY = [135/255.,141/255.,145/255.]
else: # for testing if my shape lines up with old image
    RED = [0, 1, 1]
    BLUE = [0, 1, 1]
    GRAY = [0, 1, 1]
    GRAY = [0, 0, 0]



# ==== outer flower ====
if True:
    A, B, C = 0.96, 1.07, 0.95 #0.9750
    DIV=128.
    ctx.set_source_rgb(0, 0, 1)
    radius = radius * 0.91 # NOTE: here, for the outer flower, we have a multiply A
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

        bx = ox + radius * np.sin(ang - sang * 1/DIV) * B 
        by = oy + radius * np.cos(ang - sang * 1/DIV) * B

        cx = ox + radius * np.sin(ang - sang * 2/DIV) * C
        cy = oy + radius * np.cos(ang - sang * 2/DIV) * C

        ctx.curve_to(bx, by, cx, cy, dx, dy)
        #ctx.set_source_rgb(0, 0, 1)
        #ctx.stroke()
        #ctx.move_to(dx, dy) # starting point


        # rest of the way
        ang = arc * sang
        dx = ox + radius * np.sin(ang)
        dy = oy + radius * np.cos(ang)

        # TODO: move the spline control points inwards

        bx = ox + radius * np.sin(ang - 0.5*sang + sang * 2/DIV) * C 
        by = oy + radius * np.cos(ang - 0.5*sang + sang * 2/DIV) * C

        cx = ox + radius * np.sin(ang - 0.5*sang + sang * 1/DIV) * B
        cy = oy + radius * np.cos(ang - 0.5*sang + sang * 1/DIV) * B

        ctx.curve_to(bx, by, cx, cy, dx, dy)
        #ctx.set_source_rgb(0, 1, 0)
        #ctx.stroke()
        #ctx.move_to(dx, dy) # starting point


    ctx.set_line_width(1.5) 
    ctx.set_source_rgb(*GRAY)
    ctx.stroke()

    radius = radius / 0.91 # NOTE: here, for the outer flower, we have a multiply A


# === blue star ===

radius *=1.03

if True:

    for FILL in [True, False]:
        A, B, C = 0.44, 0.57, 0.45
        DIV = 10.0
        BUF = 0.0045
        #BUF = 0.02
        ax, ay = ox, oy + radius
        ax = ox + radius* np.sin(BUF)
        ay = oy + radius* np.cos(BUF)
        ctx.move_to(ax, ay) # starting point
        for arc in range(1, 10):

            if FILL == False or arc < 9:  # NOTE: extra gray outline to work with BUF
                # bezier to half-way
                ang = arc * sang - sang/2.0
                # NOTE: factor of 0.5 to determine finishing posiiton
                dx = ox + radius*A * np.sin(ang)
                dy = oy + radius*A * np.cos(ang)
                print(dx, dy)

                # TODO: move the spline control points inwards

                bx = ox + radius * np.sin(ang - sang * 5/DIV) * B 
                by = oy + radius * np.cos(ang - sang * 5/DIV) * B

                cx = ox + radius * np.sin(ang - sang * 3/DIV) * C
                cy = oy + radius * np.cos(ang - sang * 3/DIV) * C

                ctx.curve_to(bx, by, cx, cy, dx, dy)
                #ctx.set_source_rgb(0, 0, 1)
                #ctx.stroke()
                #ctx.move_to(dx, dy) # starting point


                # rest of the way
                ang = arc * sang
                dx = ox + radius * np.sin(ang - BUF)
                dy = oy + radius * np.cos(ang - BUF)

                # TODO: move the spline control points inwards

                bx = ox + radius * np.sin(ang - 0.5*sang + sang * 3/DIV) * C 
                by = oy + radius * np.cos(ang - 0.5*sang + sang * 3/DIV) * C

                cx = ox + radius * np.sin(ang - 0.5*sang + sang * 5/DIV) * B
                cy = oy + radius * np.cos(ang - 0.5*sang + sang * 5/DIV) * B

                ctx.curve_to(bx, by, cx, cy, dx, dy)
                #ctx.set_source_rgb(0, 1, 0)
                #ctx.stroke()
                dx = ox + radius * np.sin(ang + BUF)
                dy = oy + radius * np.cos(ang + BUF)
                ctx.line_to(dx, dy) # starting point


        if FILL:
            ctx.set_source_rgb(*BLUE)
            ctx.fill()
        else:
            ctx.set_line_width(1.5) 
            ctx.set_source_rgb(*GRAY)
            #ctx.set_source_rgb(*BLUE)
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

# === red circle ===
if True:
    ctx.set_source_rgb(*GRAY)
    #ctx.set_source_rgb(*RED)
    circle(ox, oy, 21.5)
    ctx.set_source_rgb(*RED)
    circle(ox, oy, 20)



#ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas


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
