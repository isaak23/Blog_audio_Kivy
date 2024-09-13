from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock  # Per aggiornare l'interfaccia in base a un timer
import serial
import serial.tools.list_ports

# Carica il file design.kv
Builder.load_file('design.kv')

class RootWidget(ScreenManager):
    pass

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serial_connection = None
        Clock.schedule_interval(self.read_from_serial, 1/10)  # Legge dalla seriale ogni 100ms

    def get_serial_ports(self):
        """Ottiene la lista delle porte seriali disponibili"""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]  # Restituisce solo i nomi delle porte

    def update_serial_port(self, port_name):
        """Aggiorna la porta seriale selezionata e stabilisce la connessione"""
        if self.serial_connection:
            self.serial_connection.close()  # Chiude la connessione precedente, se esiste
        try:
            self.serial_connection = serial.Serial(port_name, 9600, timeout=1)  # Timeout di 1 secondo
            print(f"Connesso a {port_name}")
        except serial.SerialException as e:
            print(f"Errore: {e}")

    def accendi_led(self):
        """Invia il comando per accendere il LED"""
        if self.serial_connection:
            self.serial_connection.write(b'1')  # Invia il comando '1' all'Arduino

    def spegni_led(self):
        """Invia il comando per spegnere il LED"""
        if self.serial_connection:
            self.serial_connection.write(b'0')  # Invia il comando '0' all'Arduino

    def read_from_serial(self, dt):
        """Legge i dati dall'Arduino e li visualizza nel TextInput"""
        if self.serial_connection and self.serial_connection.in_waiting > 0:
            try:
                line = self.serial_connection.readline().decode('utf-8').strip()  # Legge una linea dalla seriale
                self.ids.serial_monitor.text += line + '\n'  # Aggiunge la linea al monitor
                self.ids.serial_monitor.cursor = (0, len(self.ids.serial_monitor.text))  # Scorri in basso
            except Exception as e:
                print(f"Errore di lettura: {e}")

class ArduinoApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    ArduinoApp().run()



"""
#Snippet per leggere le seriali disponibili sul pc


def serial_ports():
    #Lists serial port names

        #:raises EnvironmentError:
            #On unsupported or unknown platforms
        #:returns:
            #A list of the serial ports available on the system

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

"""