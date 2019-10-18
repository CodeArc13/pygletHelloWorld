import pyglet

window = pyglet.window.Window(640, 480)


MIN_LABEL_Y = 200
MAX_LABEL_Y = 400
COORDS_PER_SECOND = 100

label = pyglet.text.Label('Hello, world!', font_size=14, x=0, y=MIN_LABEL_Y)

@window.event
def on_draw():
    window.clear()
    label.draw()

ycoord = MIN_LABEL_Y

def update(dt):
    global ycoord
    ycoord += COORDS_PER_SECOND * dt
    label.y = int(ycoord)  
    if label.y > MAX_LABEL_Y:
        label.y = ycoord = MIN_LABEL_Y

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
