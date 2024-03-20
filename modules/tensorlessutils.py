from AppOpener import open,close
import gesture


def whatsapp():
    open("whatsapp")
    
def close_whatsapp():
    close("whatsapp")
    
def open_spotify():
    open("spotify")

def close_app(app):
    close(app)

def open_app(app):
    open(app)

def gesture_mode():
    gesture.show_tabs()

def main():
    # gesture_mode()
    # whatsapp()
    open_spotify()

if __name__ == "__main__":
    main()