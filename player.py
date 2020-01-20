import prompt_toolkit as pt
import json
from pygments.lexers import python
from time import sleep


def player():
    document = pt.document.Document(text = 'Press enter to start')
    buffer = pt.buffer.Buffer(document = document, name = 'player')
    Header = pt.buffer.Buffer()
    foot = pt.layout.controls.FormattedTextControl(text='press crtl-q to exit')
    kb = pt.key_binding.KeyBindings()

    def printText(app):
        buffer.insert_text('h')
        app.invalidate()
        sleep(1)
    @kb.add('c-q')
    def exit_(event):
        event.app.exit()

    @kb.add('c-m')
    def start_(event):
        event.app.layout.focus(buffer)
        event.app.current_buffer.set_document(pt.document.Document())

    layout = pt.layout.Layout(pt.layout.containers.HSplit([
        pt.layout.containers.Window(content=pt.layout.controls.BufferControl(buffer=Header), height= 2),
        pt.layout.containers.Window(content=pt.layout.controls.BufferControl(buffer=buffer, lexer = pt.lexers.PygmentsLexer(python.Python3Lexer))),
        pt.layout.containers.Window(content=foot, height=1)
    ]))
    app = pt.application.Application(layout=layout, key_bindings = kb, full_screen = True, after_render = printText)
    app.run()


if __name__ == '__main__':
    player()
