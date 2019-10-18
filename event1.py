import pyglet

e = pyglet.event.EventDispatcher()
e.register_event_type('end_of_the_world')

#def foo(minutesLeftToLive):
#@e.event
@e.push_handlers #push is used for events with the same name
def end_of_the_world(minutesLeftToLive):
        print('Welcome to Hell!')
@e.push_handlers
def end_of_the_world(minutesLeftToLive):
    if minutesLeftToLive < 10:
        print('AAAAAAAAAAAAAAGGGGGGHHHHHH!')
    else:
        print('oh no!')


#e.set_handler('end_of_the_world', foo)
#e.event(end_of_the_world)

e.dispatch_event('end_of_the_world', 5) #invokes foo
