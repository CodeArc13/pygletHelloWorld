import pyglet
from pyglet import clock
from pyglet.gl import *

# Zooming constants
ZOOM_IN_FACTOR = 1.2
ZOOM_OUT_FACTOR = 1/ZOOM_IN_FACTOR
YELLOW_ALPHA = 255, 255, 0, 255
RED          = 255,   0, 0
DARK_RED     =  55,   0, 0

class CustomGroup(pyglet.graphics.Group):
    def set_colour(self):
        pass


class App(pyglet.window.Window):
    
    def __init__(self, width, height, *args, **kwargs):


        conf = Config(sample_buffers=1,
                      samples=4,
                      depth_size=16,
                      double_buffer=True)
        super().__init__(width, height, config=conf, *args, **kwargs)

        self.fps_display = pyglet.window.FPSDisplay(window=self)
        self.fps_display.label.font_size = 20
        self.fps_display.label.color = YELLOW_ALPHA
        self.fps_display.label.x = 5
        self.fps_display.label.y = self.height - 30



        self.main_batch = pyglet.graphics.Batch()   
        self.vertex_list = pyglet.graphics.vertex_list(1024, 'v2i/static', 'c3B/stream')
        #### >>>SPRITE METHOD<<< #####

        pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
        pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self.wireOff_image = pyglet.image.load('wireOffw.png')
        self.wireOff = pyglet.sprite.Sprite(self.wireOff_image, batch=self.main_batch, subpixel=True) 
        self.wireOff1 = pyglet.sprite.Sprite(self.wireOff_image, x=60, y=0, batch=self.main_batch, subpixel=True)
                
        #### >>>QUAD METHOD<<< #####

        #self.custom_group = CustomGroup()
        #self.draw_block( 0,   0, self.vertex_list, DARK_RED)
        #self.draw_block(60,   0, self.vertex_list, DARK_RED)
        #self.draw_block( 0,  60, self.vertex_list, DARK_RED)
        #self.draw_block( 0, -60, self.vertex_list, DARK_RED)
        
        #Initialize camera values
        self.left   = 0
        self.right  = width
        self.bottom = 0
        self.top    = height
        self.zoom_level = 1
        self.zoomed_width  = width
        self.zoomed_height = height
        clock.schedule_interval(self.update, 1/60)

    def draw_block(self, x, y, v_list, color):
        self.vertex_list = self.main_batch.add(4, pyglet.gl.GL_QUADS, None,
                                ('v2i/static', (x, y, x+60, y, x+60, y+60, x, y+60)),
        #                               xbl ybl xbr ybr xtr   ytr  xtl  ytl
                                ('c3B/stream', (color)*4))



    def init_gl(self, width, height):

        # Set clear color
        glClearColor(0/255, 0/255, 0/255, 0/255)

        # Set antialiasing
        #glEnable( GL_LINE_SMOOTH )
        #glEnable( GL_POLYGON_SMOOTH )
        #glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )

        ## Set alpha blending
        #glEnable( GL_BLEND )
        #glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

        # Set viewport
        glViewport( 0, 0, width, height )


    def on_resize(self, _width, _height):
        # Set window values
        if self.width != _width:
            self.width = _width
        if self.height != _height:
            self.height = _height
        # Initialize OpenGL context
        self.init_gl(_width, _height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # Move camera
        self.left   -= dx*self.zoom_level
        self.right  -= dx*self.zoom_level
        self.bottom -= dy*self.zoom_level
        self.top    -= dy*self.zoom_level

    def on_mouse_scroll(self, x, y, dx, dy):
        # Get scale factor
        f = ZOOM_IN_FACTOR if dy > 0 else ZOOM_OUT_FACTOR if dy < 0 else 1
        # If zoom_level is in the proper range
        if 1 <= self.zoom_level*f < 12:

            self.zoom_level *= f
            print("z " +  str(self.zoom_level))
            print("f " +  str(f))
            print("* " +  str(self.zoom_level*f))
            mouse_x = x/self.width
            mouse_y = y/self.height

            mouse_x_in_world = self.left   + mouse_x*self.zoomed_width
            mouse_y_in_world = self.bottom + mouse_y*self.zoomed_height

            self.zoomed_width  *= f
            self.zoomed_height *= f

            self.left   = mouse_x_in_world - mouse_x*self.zoomed_width
            self.right  = mouse_x_in_world + (1 - mouse_x)*self.zoomed_width
            self.bottom = mouse_y_in_world - mouse_y*self.zoomed_height
            self.top    = mouse_y_in_world + (1 - mouse_y)*self.zoomed_height

    def on_draw(self):
        # Initialize Projection matrix
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()

        # Initialize Modelview matrix
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        # Save the default modelview matrix
        glPushMatrix()

        # Clear window with ClearColor
        glClear( GL_COLOR_BUFFER_BIT )

        # Set orthographic projection matrix
        glOrtho( self.left, self.right, self.bottom, self.top, 1, -1 )
        self.vertex_list.colors[:3] = RED
        self.main_batch.draw()
        self.fps_display.draw()
        # Remove default modelview matrix
        glPopMatrix()

    def update(self, dt):
        pass

    def run(self):
        pyglet.app.run()


App(1024, 768).run()

