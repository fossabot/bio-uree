import locale
import logging
import time

from modules import button, flowmeter, lv_sensor, ph_meter, relais
from server import app_server

locale.setlocale(locale.LC_TIME, "")

FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s] <%(name)s> - %(message)s", "%x %X"
)

LOGGER = logging.getLogger("Bio-Urée")
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.FileHandler(filename="logs/biouree.log", encoding="utf-8", mode="w+")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

LOGGER.info("Lancement de Bio-Urée ...")

MODULE_CODE = "EZ42GLHF69"

# BCM gpio pin
PIN_BUTTON = 21  # Bouton chasse d'eau
PIN_FLOWMETER = 20  # Débit-mètre
PIN_LV_SENSOR = 27  # Capteur de niveau (cuve principale)
PIN_RELAIS_1 = 5  # Relais pompe chasse d'eau
PIN_RELAIS_2 = 6  # Relais électrovanne (cuve principal)
PIN_RELAIS_3 = 13  # Relais électrovanne (cuve secondaire)
PIN_PH_METER = 14  # PH-mètre (cuve principale)

FLOWMETER = flowmeter.Flowmeter(PIN_FLOWMETER)
LOGGER.debug("Débit-mètre initialisé")
RELAIS_1 = relais.Relais(PIN_RELAIS_1)
LOGGER.debug("Pompe initialisé")
RELAIS_2 = relais.Relais(PIN_RELAIS_2)
LOGGER.debug("Électrovanne cuve principale initialisé")
RELAIS_3 = relais.Relais(PIN_RELAIS_3)
LOGGER.debug("Électrovanne cuve secondaire initialisé")
PH_METER = ph_meter.PhMeter(PIN_PH_METER)
LOGGER.debug("PH-mètre initialisé")


APP_SERVER = app_server.AppServer(PIN_LV_SENSOR, PH_METER, MODULE_CODE)


class Main:
    def __init__(self):
        LOGGER.info("Activation ...")
        # Sortie cuve principale de base
        self.activated_cuve = RELAIS_2
        self.running = True
        self.button = False

    def lv_sensor_callback(self, channel):
        # Si cuve principale pleine redirection vers la 2e
        if self.activated_cuve == RELAIS_2:
            self.activated_cuve = RELAIS_3
            LOGGER.info("La cuve principale est pleine.")
        else:
            self.activated_cuve = RELAIS_2
            LOGGER.info("La cuve principale a été vidée.")

    def button_callback(self, channel):
        self.button = True

    def run(self):
        while self.running:
            if self.button:
                # Chasse d'eau enclenché -> Active sortie buffer
                relais = self.activated_cuve
                relais.activate()
                # Volume d'urine en millilitres
                v_urine = round((FLOWMETER.measure(2) * 1000, 2))
                if v_urine != 0:
                    # Active la pompe
                    RELAIS_1.activate()
                    time.sleep(v_urine / 50)
                    RELAIS_1.desactivate()
                    time.sleep(4)
                relais.desactivate()
                LOGGER.info(
                    f"{str(v_urine)} mL d'urine avec : {str(v_urine * 20)} mL d'eau vers la cuve {'principale' if relais == RELAIS_2 else 'secondaire'}."
                )
                self.button = False


try:
    MAIN = Main()
    # Définition des functions de retour du bouton et du capteur
    LV_SENSOR = lv_sensor.Lv_sensor(PIN_LV_SENSOR, MAIN.lv_sensor_callback)
    LOGGER.debug("Capteur de niveau initialisé")
    BUTTON = button.Button(PIN_BUTTON, MAIN.button_callback)
    LOGGER.debug("Bouton chasse d'eau initialisé")
    APP_SERVER.start()
    MAIN.run()
except KeyboardInterrupt:
    LOGGER.info("Arrêt de Bio-Urée ...")
    MAIN.running = False
    RELAIS_1.desactivate()
    RELAIS_2.desactivate()
    RELAIS_3.desactivate()
    # Fin du programme on nettoie les ports
    BUTTON.clean()
    LOGGER.debug("Bouton chasse d'eau arrêté")
    FLOWMETER.clean()
    LOGGER.debug("Débit-mètre arrêté")
    LV_SENSOR.clean()
    LOGGER.debug("Capteur de niveau arrêté")
    RELAIS_1.clean()
    LOGGER.debug("Pompe arrêté")
    RELAIS_2.clean()
    LOGGER.debug("Électrovanne cuve principale arrêté")
    RELAIS_3.clean()
    LOGGER.debug("Électrovanne cuve secondaire arrêté")
    LOGGER.debug("PH-mètre arrêté")
    APP_SERVER.server.server_close()
    APP_SERVER.join()
