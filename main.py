import time
from filesharer import FileSharer
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import webbrowser

Builder.load_file('frontend.kv')

start_camera_text = "Start Camera"


class CameraScreen(Screen):
    def start(self):
        """Starts camera and changes Button text and sets the camera texture to default"""
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops camera and changes Button text and sets the camera texture to none"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = start_camera_text
        self.ids.camera.texture = None

    def capture(self):
        """Creates a filename with the current time and captures and saves a photo
        image under the filename and changes the current screen to the image screen
        and displays the captured image on the image screen"""
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filepath = f"photos/{current_time}.png"
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    link_message = "Create a link first"

    def create_link(self):
        """
        Accesses the photo filepath, uploads it to the web, and inserts
        the link in the Label widget
        :return:
        """
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        file_sharer = FileSharer(filepath=file_path)
        self.url = file_sharer.share()
        self.ids.img_link.text = self.url

    def copy_link(self):
        """Copy link to the clipboard available for pasting"""
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.img_link.text = self.link_message

    def open_link(self):
        """Open link with default browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.img_link.text = self.link_message

    def back_to_home(self):
        self.manager.current = 'camera_screen'
        self.manager.current_screen.ids.camera.opacity = 0
        self.manager.current_screen.ids.camera.play = False
        self.manager.current_screen.ids.camera_button.text = start_camera_text
        self.manager.current_screen.ids.camera.texture = None


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
