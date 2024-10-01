import sys
sys.path.append("../mqi-api")
from mqi.v1.api import MQI

m = MQI("ws://localhost", "8080", "username", "password")
m.connect()

# Will set current of channel 5 to 1.1
m.set_current(1,[5],1.1)
print(m.get_ADC_current(1, []))
