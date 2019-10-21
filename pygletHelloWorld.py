import pyglet
from pyglet import clock
from pyglet.window import mouse
from pyglet.gl import *

width = 640
height = 480
YELLOW = 255, 255, 0, 255
MIN_VECY = 200
MAX_VECY = 400
COORDS_PER_SECOND = 100


ZOOM_IN_FACTOR = 1.2
ZOOM_OUT_FACTOR = 1/ZOOM_IN_FACTOR
#print(pyglet.gl.gl_info.get_version())
conf = Config(sample_buffers=1,
                      samples=4,
                      depth_size=16,
                      double_buffer=True)
window = pyglet.window.Window(width=width, height=height, config=conf)

left   = 0
right  = width
bottom = 0
top    = height
zoom_level = 1
zoomed_width  = width
zoomed_height = height
#vecx = 20
#vecy = 200
#mousex = 0
#mousey = 0
#movementTotalX = 0
#movementTotalY = 0
#worldx = 0
#worldy = 0
#last_worldx = 0
#last_worldy = 0

main_batch = pyglet.graphics.Batch()   
wireOff_image = pyglet.image.load('wireOff.png')
wireOff = pyglet.sprite.Sprite(wireOff_image, batch=main_batch)
wireOff1 = pyglet.sprite.Sprite(wireOff_image, x=100, y=0 ,batch=main_batch)

fps_display = pyglet.window.FPSDisplay(window=window)
fps_display.label.font_size = 20
fps_display.label.color = YELLOW
fps_display.label.x = 5
fps_display.label.y = window.height - 30
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

#vertex_list0 = pyglet.graphics.vertex_list(4, 'v2i', 'c3B') #how to declare empty vertex list
#vertex_list1 = pyglet.graphics.vertex_list(4, 'v2i', 'c3B')


#quad = pyglet.graphics.vertex_list(4,
#    ('v2i', (0, 0,  50, 0, 50, 50, 0, 50)),
#    ('c3B', (55, 0, 0, 55, 0, 0, 55, 0, 0, 55, 0, 0)))
   #('v2i', (0, 0,  100, 0, 100, 100, 10, 100)),
           # b left  b right  t right   t left
   #('c3B', (0, 0, 255, 0, 0, 255, 0, 255, 0,  255, 140, 55)))

@window.event
def init_gl(width, height):
    # Set clear color
    glClearColor(0/255, 0/255, 0/255, 0/255)

    # Set antialiasing
    glEnable( GL_LINE_SMOOTH )
    glEnable( GL_POLYGON_SMOOTH )
    glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )

    # Set alpha blending
    glEnable( GL_BLEND )
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

    # Set viewport
    glViewport( 0, 0, width, height )

@window.event
def on_resize(w, h):
    global width, height
    # Set window values
    width  = w
    height = h
    # Initialize OpenGL context
    init_gl(w, h)

@window.event
def on_mouse_motion(x, y, dx, dy):
    #global mousex, mousey
    label.text = str(x) + " " + str(y) + " " + str(dx) + " " + str(dy)
    
@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    global left, right, bottom, top
    #global worldx, worldy
    #global last_worldx, last_worldy
    #global movementTotalX, movementTotalY
    if button & mouse.LEFT: 
        label.text = str(x) + " " + str(y) + " " + str(dx) + " " + str(dy)
        #movementTotalX += dx
        #movementTotalY += dy
        #print(movementTotalX)
        #print(movementTotalY)
        #glTranslatef(dx*f, dy*f, 0)
        left   -= dx
        right  -= dx
        bottom -= dy
        top    -= dy

@window.event
def on_mouse_press(x, y, button, modifiers):
    #global movementTotalX, movementTotalY
    if button & mouse.LEFT:
        pass
        #movementTotalX = 0
        #movementTotalY = 0

@window.event
def on_mouse_scroll(x, y, dx, dy):
    global zoom_level, ZOOM_IN_FACTOR, ZOOM_OUT_FACTOR, width, height
    global left, right, bottom, top, zoomed_width, zoomed_height
    # Get scale factor
    f = ZOOM_IN_FACTOR if dy > 0 else ZOOM_OUT_FACTOR if dy < 0 else 1
        # If zoom_level is in the proper range
    if .2 < zoom_level*f < 5:
        zoom_level *= f

        mouse_x = x/width
        mouse_y = y/height

        mouse_x_in_world = left   + mouse_x*zoomed_width
        mouse_y_in_world = bottom + mouse_y*zoomed_height

        zoomed_width  *= f
        zoomed_height *= f

        left   = mouse_x_in_world - mouse_x*zoomed_width
        right  = mouse_x_in_world + (1 - mouse_x)*zoomed_width
        bottom = mouse_y_in_world - mouse_y*zoomed_height
        top    = mouse_y_in_world + (1 - mouse_y)*zoomed_height

    print(zoom_level)
        
    


@window.event
def on_draw():
    global scale, left, right, bottom, top
     # Initialize Projection matrix
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()

    # Initialize Modelview matrix
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    # Save the default modelview matrix
    glPushMatrix()
    #global worldx, worldy
    #window.clear()    
    #glScalef(scale, scale, 0)
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    
    glOrtho( left, right, bottom, top, 1, -1 )

    #main_batch.add(4, pyglet.gl.GL_QUADS, None,
    #                        ('v2i', (0+vecx, 0+vecy,  50+vecx, 0+vecy, 50+vecx, 50+vecy, 0+vecx, 50+vecy)),
    #                        ('c3B', (55, 0, 0, 55, 0, 0, 55, 0, 0, 55, 0, 0)))
    #main_batch.add(4, pyglet.gl.GL_QUADS, None,
    #                        ('v2i', (mousex, mousey,  50+mousex, mousey, 50+mousex, 50+mousey, mousex, 50+mousey)),
    #                        ('c3B', (55, 0, 0, 55, 0, 0, 55, 0, 0, 55, 0, 0)))
    
    #wireOff.scale = 0.50
      
    #vertex_list0.delete()
    main_batch.draw()
    label.draw()   
    fps_display.draw()


    # Remove default modelview matrix
    glPopMatrix()
#ycoord = vecy

def update(dt):
    pass
    #global vecy
    #global ycoord  
    #ycoord += COORDS_PER_SECOND * dt
    #vecy = int(ycoord)
    #if vecy > MAX_VECY:
    #    vecy = ycoord = MIN_VECY

clock.schedule_interval(update, 1/60)

pyglet.app.run()

#class CustomGroup(pyglet.graphics.Group):
#    def pos(self):
#        glEnable(texture.target)
#        glBindTexture(texture.target, texture.id)
