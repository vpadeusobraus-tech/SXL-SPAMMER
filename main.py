import threading
import time
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Cores Temáticas SXL (Egito/Urbano)
RED = get_color_from_hex('#CE1126')
WHITE = get_color_from_hex('#FFFFFF')
BLACK = get_color_from_hex('#000000')
GOLD = get_color_from_hex('#C09304')

class SXLApp(App):
    def build(self):
        self.total_sent = 0
        self.running = False
        self.message_index = 0
        self.lock = threading.Lock()

        Window.clearcolor = BLACK

        # Layout Principal
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Cabeçalho Ajustado (Sem bug de sobreposição)
        header = Label(
            text="[b][color=ff0000]S[/color][color=ffffff]X[/color][color=ff0000]L[/color][/b]",
            markup=True, font_size='60sp', size_hint_y=None, height=80
        )
        sub_header = Label(
            text="EGYPTIAN SPAMMER v2",
            color=GOLD, font_size='14sp', size_hint_y=None, height=20
        )
        main_layout.add_widget(header)
        main_layout.add_widget(sub_header)

        # Inputs
        main_layout.add_widget(Label(text="TOKENS:", color=RED, bold=True, size_hint_y=None, height=25))
        self.token_input = TextInput(hint_text="Lista de tokens...", background_color=(0.1, 0.1, 0.1, 1), foreground_color=WHITE)
        main_layout.add_widget(self.token_input)

        main_layout.add_widget(Label(text="MENSAGENS:", color=WHITE, bold=True, size_hint_y=None, height=25))
        self.msg_input = TextInput(hint_text="Textos para spam...", background_color=(0.1, 0.1, 0.1, 1), foreground_color=WHITE)
        main_layout.add_widget(self.msg_input)

        # ID e Delay
        config_box = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.channel_input = TextInput(hint_text="ID do Canal", multiline=False)
        self.delay_input = TextInput(hint_text="Delay", multiline=False, text="1.0")
        config_box.add_widget(self.channel_input)
        config_box.add_widget(self.delay_input)
        main_layout.add_widget(config_box)

        # Botão
        self.btn_start = Button(
            text="INICIAR ATAQUE SXL", font_size='20sp', bold=True,
            background_normal='', background_color=RED, color=WHITE,
            size_hint_y=None, height=70
        )
        self.btn_start.bind(on_press=self.toggle_spam)
        main_layout.add_widget(self.btn_start)

        # Console de Logs (Onde a mágica aparece)
        self.log_label = Label(
            text="[SXL] Aguardando comando...",
            color=GOLD, font_size='12sp', size_hint_y=None, height=40, markup=True
        )
        main_layout.add_widget(self.log_label)

        return main_layout

    def toggle_spam(self, instance):
        if not self.running:
            self.running = True
            self.btn_start.text = "PARAR ATAQUE"
            self.btn_start.background_color = (0.2, 0.2, 0.2, 1)
            threading.Thread(target=self.start_process, daemon=True).start()
        else:
            self.running = False
            self.btn_start.text = "INICIAR ATAQUE SXL"
            self.btn_start.background_color = RED

    def start_process(self):
        tokens = [t.strip() for t in self.token_input.text.split('\n') if t.strip()]
        messages = [m.strip() for m in self.msg_input.text.split('\n') if m.strip()]
        channel_id = self.channel_input.text.strip()
        try: delay = float(self.delay_input.text)
        except: delay = 1.0

        if not tokens or not messages or not channel_id:
            Clock.schedule_once(lambda dt: self.update_log("ERRO: CAMPOS VAZIOS"))
            return

        for token in tokens:
            threading.Thread(target=self.worker, args=(token, messages, channel_id, delay), daemon=True).start()

    def update_log(self, text):
        self.log_label.text = f"[SXL] {text}"

    def worker(self, token, messages, channel_id, delay):
        session = requests.Session()
        while self.running:
            with self.lock:
                if self.message_index >= len(messages): self.message_index = 0
                msg = messages[self.message_index]
                self.message_index += 1

            try:
                r = session.post(
                    f'https://discord.com/api/v9/channels/{channel_id}/messages',
                    headers={'Authorization': token},
                    json={'content': msg}, timeout=5
                )
                if r.status_code == 200:
                    self.total_sent += 1
                    Clock.schedule_once(lambda dt: self.update_log(f"ENVIADOS: [color=ffffff]{self.total_sent}[/color]"))
                elif r.status_code == 429:
                    Clock.schedule_once(lambda dt: self.update_log("[color=ff0000]RATE LIMIT (LENTO)[/color]"))
            except Exception as e:
                pass
            time.sleep(delay)

if __name__ == '__main__':
    SXLApp().run()
