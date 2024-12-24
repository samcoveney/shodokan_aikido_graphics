import math
import cairo
from gi.repository import Pango
from gi.repository import PangoCairo 
import numpy as np

from collections import namedtuple

def warp_path(ctx, function):
    first = True

    for type, points in ctx.copy_path():
        if type == cairo.PATH_MOVE_TO:
            if first:
                ctx.new_path()
                first = False
            x, y = function(*points)
            ctx.move_to(x, y)

        elif type == cairo.PATH_LINE_TO:
            x, y = function(*points)
            ctx.line_to(x, y)

        elif type == cairo.PATH_CURVE_TO:
            x1, y1, x2, y2, x3, y3 = points
            x1, y1 = function(x1, y1)
            x2, y2 = function(x2, y2)
            x3, y3 = function(x3, y3)
            ctx.curve_to(x1, y1, x2, y2, x3, y3)

        elif type == cairo.PATH_CLOSE_PATH:
            ctx.close_path()

             
def make_arc_method(capture_radius, capture_angle):
    assert(capture_radius != 0)
    if capture_radius < 0.:
        capture_angle = capture_angle + math.pi
    
    
    def arc(x, y):
        r = -y
        theta = (x) / capture_radius
        xnew = r * math.cos(-theta - capture_angle)
        ynew = r * math.sin(theta + capture_angle)
        return xnew, ynew
    
    return arc

Sector = namedtuple('Sector',['inside_radius','outside_radius','angle1','angle2','negative'])

def text_arc_dimensions(context, text, radius, angle):
    """
    Get dimensions of a text arc
    :param context  The cairo `context`
    :param text     The text
    :param radius   Radius of the baseline of the arc. If positive, text 
          will ascend away from the origin. If negative, text will 
          ascend towards the origin
    :param angle    The angle of the text origin
    :returns a Sector
    
    returns (baseline_radius, ascender_radius, left_angle, right_angle)
    """
    extents = context.text_extents(text)
    assert(radius != 0)
    width = extents.width / radius
    height = math.copysign(extents.height, radius)
    baseline_radius = abs(radius)
    
    negative = False
    outside = 0.
    inside = 0.
    th1 = 0.
    th2 = 0.
    
    if radius > 0.:
        outside = baseline_radius + extents.height
        inside = baseline_radius
        th1 = angle
        th2 = angle + width
    else:
        negative = True
        outside = baseline_radius
        inside = baseline_radius - extents.height
        th1 = angle + width
        th2 = angle
    
    return Sector(inside_radius=inside , outside_radius=outside, angle1=th1, angle2=th2, negative= negative )

def text_arc_path(context, x, y, text, radius, angle):
    """
    Creates a text path along an arc
    x and y : the position of the arc center
    radius : the radius of the arc. If positive, text will ascend away from the origin. 
      If negative, text will ascend towards the origin
      
    angle : The angle of the text origin.
    
    """
    context.save()
    context.translate(x,y)
    
    arc_function = make_arc_method(capture_radius=radius, 
                                   capture_angle=angle)
    
    context.new_path()
    context.move_to(0.,-radius)
    context.text_path(text)
    warp_path(context,arc_function)
    context.restore()

def sector(context,x, y, sector):
    context.new_path()
    context.arc(x, y, sector.inside_radius, sector.angle1, sector.angle2)
    context.arc_negative(x, y, sector.outside_radius, sector.angle2, sector.angle1)
    context.close_path() 




def circle(ctx, x,y, radius, fill=True):
    ctx.arc(x, y, radius, 0, 2*math.pi)
    if fill:
        ctx.fill()
    else:
        ctx.stroke()



def main(TEST, FEATURE, OUTLINE, PDFNAME):

    # set the canvas
    # ==============
    paper_width = 450
    paper_height = 450
    margin = 20

    point_to_millimeter = 72/25.4

    pdfname = PDFNAME 
    pdf = cairo.PDFSurface( pdfname, 
                            paper_width*point_to_millimeter, 
                            paper_height*point_to_millimeter
                            )

    ctx = cairo.Context(pdf)
    ctx.scale(point_to_millimeter, point_to_millimeter)


    # line cap options - not consistent...
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)


    # Open image to an ARGB32 ImageSurface
    if TEST:
        filename = 'Shodokan_Symbol_original.png'
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


    ox, oy = paper_width/2.0, paper_height/2.0


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
        GRAY = [0, 1, 1]



    # ==== outer flower ====
    if not TEST or FEATURE == "flower":
        A, B, C = 0.95, 1.065, 0.96 #0.9750
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

    if not TEST or FEATURE == "star":

        for FILL in [True, False]:
            A, B, C = 0.44, 0.6, 0.47
            DIV = 10.0
            BUF = 0.00
            #BUF = -0.002
            ax, ay = ox, oy + radius
            ax = ox + radius* np.sin(BUF)
            ay = oy + radius* np.cos(BUF)
            ctx.move_to(ax, ay) # starting point
            for arc in range(1, 9):

                if FILL == False or arc < 9:  # NOTE: extra gray outline to work with BUF
                    # bezier to half-way
                    ang = arc * sang - sang/2.0
                    # NOTE: factor of 0.5 to determine finishing posiiton
                    dx = ox + radius*A * np.sin(ang)
                    dy = oy + radius*A * np.cos(ang)
                    print(dx, dy)

                    # TODO: move the spline control points inwards

                    bx = ox + radius * np.sin(ang - sang * 4.2/DIV) * B 
                    by = oy + radius * np.cos(ang - sang * 4.2/DIV) * B

                    a2 = 4.5
                    cx = ox + radius * np.sin(ang - sang * a2/DIV) * C
                    cy = oy + radius * np.cos(ang - sang * a2/DIV) * C

                    ctx.curve_to(bx, by, cx, cy, dx, dy)
                    #ctx.set_source_rgb(0, 0, 1)
                    if FILL == False:
                        if OUTLINE:
                            ctx.set_source_rgb(*GRAY)
                        else:
                            ctx.set_source_rgb(*BLUE)
                        ctx.stroke()
                        ctx.move_to(dx, dy) # starting point


                    # rest of the way
                    ang = arc * sang
                    dx = ox + radius * np.sin(ang - BUF)
                    dy = oy + radius * np.cos(ang - BUF)

                    # TODO: move the spline control points inwards

                    a2 = 4.5
                    bx = ox + radius * np.sin(ang - 0.5*sang + sang * a2/DIV) * C 
                    by = oy + radius * np.cos(ang - 0.5*sang + sang * a2/DIV) * C

                    cx = ox + radius * np.sin(ang - 0.5*sang + sang * 4.2/DIV) * B
                    cy = oy + radius * np.cos(ang - 0.5*sang + sang * 4.2/DIV) * B

                    ctx.curve_to(bx, by, cx, cy, dx, dy)
                    #ctx.set_source_rgb(0, 1, 0)
                    if FILL == False:
                        if OUTLINE:
                            ctx.set_source_rgb(*GRAY)
                        else:
                            ctx.set_source_rgb(*BLUE)
                        ctx.stroke()
                    dx = ox + radius * np.sin(ang + BUF)
                    dy = oy + radius * np.cos(ang + BUF)
                    ctx.line_to(dx, dy) # starting point


            if FILL:
                ctx.set_source_rgb(*BLUE)
                if not TEST:
                    ctx.fill()
            else:
                ctx.set_line_width(1.5) 
                if OUTLINE:
                    ctx.set_source_rgb(*GRAY)
                else:
                    ctx.set_source_rgb(*BLUE)
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
    if not TEST or FEATURE == "circle":
        if OUTLINE:
            ctx.set_source_rgb(*GRAY)
        else:
            ctx.set_source_rgb(*RED)
        #ctx.set_source_rgb(*RED)
        circle(ctx, ox, oy, 21.5)
        ctx.set_source_rgb(*RED)
        circle(ctx, ox, oy, 20)


    # === medal border ===
    if True:  # FIXME: add appropriate switch
        ctx.set_source_rgb(*BLUE)
        ctx.set_line_width(3.0) 
        circle(ctx, ox, oy, 200, fill=False)

    
    # === medal text ===
    if 0:
        ctx.set_source_rgb(*BLUE)
        ctx.set_font_size(48.0) 
        text_arc_path(ctx, ox, oy, "SHODOKAN", 150, 360)
        ctx.stroke()


    layout = PangoCairo.create_layout(ctx)
    #font_description = Pango.font_description_from_string('Arial, Ultra-Bold, 40')
    font_description = Pango.font_description_from_string('Times New Roman, Ultra-Bold, 40')
    layout.set_font_description(font_description)

    arc = 30
    sang = math.pi / 9.0
    for ldx, letter in enumerate("SHODOKAN"):

        ctx.set_source_rgb(*RED)
        ang = ldx * sang
        print(ang)

        #ANG = ang - 0.87*math.pi/2.
        ANG = ang - 0.78*math.pi/2.
        RAD = 1.4

        dx = ox + RAD*radius * np.sin(ANG) #- 20
        dy = oy - RAD*radius * np.cos(ANG) #- 20
        print(dx, dy)

        # shift box back in this direction, so line from centre of letter goes through origin
        vector = np.array([dx - ox, dy - oy])
        vector = vector / np.linalg.norm(vector)
        vector = np.array([[np.cos(-math.pi/2), -np.sin(-math.pi/2)],\
                            [-np.sin(-math.pi/2), np.cos(-math.pi/2)]]) @ vector 

        
        ctx.move_to(dx + vector[0]*18, dy-vector[1]*18)
        ctx.rotate(ANG)
        #ctx.translate(+50, 0)
        layout.set_text(letter)

        print(ldx, letter)

#    PangoCairo.update_layout(ctx, layout)
        PangoCairo.show_layout(ctx, layout)
        #ctx.translate(-50, 0)
        ctx.rotate(-ANG)

    #layout.set_text("SHODOKAN")
    arc = 30
    sang = math.pi / 7.0
    for ldx, letter in enumerate("AIKIDO"):

        ctx.set_source_rgb(*RED)
        ang = - ldx * sang - 0.82 
        print(ang)

        #ANG = ang - 0.87*math.pi/2.
        ANG = ang - 0.78*math.pi/2.
        RAD = 0.95 

        dx = ox + RAD*radius * np.sin(ANG) #- 20
        dy = oy - RAD*radius * np.cos(ANG) #- 20
        print(dx, dy)

        # shift box back in this direction, so line from centre of letter goes through origin
        vector = np.array([dx - ox, dy - oy])
        vector = vector / np.linalg.norm(vector)
        vector = np.array([[np.cos(-math.pi/2), -np.sin(-math.pi/2)],\
                            [-np.sin(-math.pi/2), np.cos(-math.pi/2)]]) @ vector 

        if letter != "I": 
            ctx.move_to(dx - vector[0]*18, dy+vector[1]*18)
        else:
            ctx.move_to(dx - vector[0]*10, dy+vector[1]*10)

        ctx.rotate(ANG + math.pi)
        #ctx.translate(+50, 0)
        layout.set_text(letter)

        print(ldx, letter)

#    PangoCairo.update_layout(ctx, layout)
        PangoCairo.show_layout(ctx, layout)
        #ctx.translate(-50, 0)
        ctx.rotate(-ANG - math.pi)

    # === create PDF ===
    pdf.show_page()


if __name__ == "__main__":
    main(TEST=False, FEATURE=None, OUTLINE=True, PDFNAME="Shodokan_Symbol.pdf")
    main(TEST=False, FEATURE=None, OUTLINE=False, PDFNAME="Shodokan_Symbol_no_outline.pdf")

    main(TEST=True, FEATURE="flower", OUTLINE=True, PDFNAME="Shodokan_Symbol_test_flower.pdf")
    main(TEST=True, FEATURE="star", OUTLINE=True, PDFNAME="Shodokan_Symbol_test_star.pdf")
    main(TEST=True, FEATURE="circle", OUTLINE=True, PDFNAME="Shodokan_Symbol_test_circle.pdf")



