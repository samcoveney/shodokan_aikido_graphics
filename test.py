import cairo, urllib.request, io
from PIL import Image

paper_width = 210
paper_height = 297
margin = 20

point_to_millimeter = 72/25.4

pdfname = "out.pdf" 
pdf = cairo.PDFSurface( pdfname, 
                        paper_width*point_to_millimeter, 
                        paper_height*point_to_millimeter
                        )

cr = cairo.Context(pdf)
cr.scale(point_to_millimeter, point_to_millimeter)

# load image
#f = urllib.request.urlopen("Shodokan_Star.png")
#i = io.BytesIO(f.read())
im = Image.open("Shodokan_Symbol.png")
imagebuffer = io.BytesIO()  
im.save(imagebuffer, format="PNG")
imagebuffer.seek(0)
imagesurface = cairo.ImageSurface.create_from_png(imagebuffer)

cr.save()
cr.scale(0.1, 0.1)
cr.set_source_surface(imagesurface, margin, margin)
cr.paint()
cr.restore()

pdf.show_page()
