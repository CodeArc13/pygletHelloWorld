import pyglet
#import pyglet.gl
import random

window = pyglet.window.Window()

@window.event
def on_draw():
    main_batch = pyglet.graphics.Batch()
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

    # for is less likely to get stuck than while
    for i in range(2):
        x = random.randint(0,window.width)
        y = random.randint(0,window.height)
        dest_x = random.randint(0,window.width)
        dest_y = random.randint(0,window.height)

        main_batch.add(2, pyglet.gl.GL_LINES, None,
                            ('v2f', (x, y, dest_x, dest_y)),
                            ('c3B', (255, 0, 0, 0, 255, 0))) #c3B is a gradient (0,0,0, 255,255,255) combo
                                                            # this gradient will be per line, not end to end.
                        
    main_batch.draw()

pyglet.app.run()