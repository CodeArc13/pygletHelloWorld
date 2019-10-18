import pyglet

window = pyglet.window.Window(640, 480)

helloLabel = pyglet.text.Label('Hello, world!', font_size=14, x=0, y=10)
goodbyeLabel = pyglet.text.Label('Goodbye, cruel world!', font_size=14, x=0, y=10)
label = helloLabel

@window.event
def on_key_press(symbol, modifiers):
    global label
    if symbol == pyglet.window.key.SPACE:
        if label == helloLabel:
            label = goodbyeLabel
        else:
            label = helloLabel

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()

