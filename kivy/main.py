import cv2, threading
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from api_service import analyze_frame_bytes

class CameraWidget(BoxLayout):
    def __init__(self, fps=10, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.img_widget = Image(size_hint=(1,0.9))
        self.add_widget(self.img_widget)
        self.status_lbl = Label(text='LOADING', size_hint=(1,0.1), font_size='20sp')
        self.add_widget(self.status_lbl)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        Clock.schedule_interval(self.update, 1.0/fps)
    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret: return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        h,w,_ = frame.shape
        tex = Texture.create(size=(w,h))
        tex.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        tex.flip_vertical()
        self.img_widget.texture = tex
        # every 2s
        if not hasattr(self,'_t0') or Clock.get_time()-self._t0>=2.0:
            self._t0=Clock.get_time()
            img_bytes = cv2.imencode('.jpg',frame)[1].tobytes()
            threading.Thread(target=self._analyze, args=(img_bytes,), daemon=True).start()
    def _analyze(self, img_bytes):
        status = analyze_frame_bytes(img_bytes)
        Clock.schedule_once(lambda dt: setattr(self.status_lbl,'text',status.upper()))
    def on_stop(self):
        self.cap.release()

class DrowsinessApp(App):
    def build(self):
        return CameraWidget()
    def on_stop(self):
        self.root.on_stop()

if __name__=='__main__':
    DrowsinessApp().run()
