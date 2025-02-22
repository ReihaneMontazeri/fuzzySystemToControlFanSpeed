# -*- coding: utf-8 -*-
"""weatherFuzzy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Pm5LqBaYF0lOTUS6n_MQ7_KXWASjHQtP

This code is written by Reihane Montazeri and Hanie Kiani
"""

!pip install scikit-fuzzy > /dev/null 2>&1

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

temperature = ctrl.Antecedent(np.arange(10,40,1), 'temperature')
humidity = ctrl.Antecedent(np.arange(20,101,1), 'humidity')
fanSpeed = ctrl.Consequent(np.arange(0,100,1), 'fanSpeed')

temperature['cold'] = fuzz.trimf(temperature.universe, [0,10,25])
temperature['medium'] = fuzz.trimf(temperature.universe, [15,25,35])
temperature['hot'] = fuzz.trimf(temperature.universe, [25,40,40])
temperature.view()

humidity['dry'] = fuzz.trimf(humidity.universe,[0,20,60])
humidity['normal'] = fuzz.trapmf(humidity.universe,[30,45,75,90])
humidity['wet'] = fuzz.trimf(humidity.universe,[60,100,100])
humidity.view()

fanSpeed['slow'] = fuzz.trimf(fanSpeed.universe, [0,0,50])
fanSpeed['moderate'] = fuzz.trimf(fanSpeed.universe, [10,50,90])
fanSpeed['fast'] = fuzz.trimf(fanSpeed.universe, [50,100,100])

fanSpeed.view()

rule1 = ctrl.Rule(temperature['cold'] & humidity['dry'], fanSpeed['slow'])
rule2 = ctrl.Rule(temperature['medium'] & humidity['dry'], fanSpeed['slow'])
rule3 = ctrl.Rule(temperature['cold'] & humidity['dry'], fanSpeed['slow'])
rule4 = ctrl.Rule(temperature['hot'] & humidity['dry'], fanSpeed['moderate'])
rule5 = ctrl.Rule(temperature['medium'] & humidity['normal'], fanSpeed['moderate'])
rule6 = ctrl.Rule(temperature['cold'] & humidity['wet'], fanSpeed['moderate'])
rule7 = ctrl.Rule(temperature['hot'] & humidity['normal'], fanSpeed['fast'])
rule8 = ctrl.Rule(temperature['hot'] & humidity['wet'], fanSpeed['fast'])
rule9 = ctrl.Rule(temperature['medium'] & humidity['wet'], fanSpeed['fast'])

fanSpeedCtrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
fan_speed = ctrl.ControlSystemSimulation(fanSpeedCtrl)

temperatureInput = float(input('Enter the temperature: '))
humidityInput = float(input('Enter the humidity: '))

fan_speed.input['temperature'] = temperatureInput
fan_speed.input['humidity'] = humidityInput

fan_speed.compute()

outputFanSpeed = fan_speed.output['fanSpeed']

print("Fan Speed:", round(outputFanSpeed, 2))

# Plot membership functions for temperature
temperature.view()
plt.axvline(x=temperatureInput, color='r', linestyle='--')
plt.text(temperatureInput, 0.5, f'Temperature: {temperatureInput}', rotation=90, ha='right', va='center')

# Plot membership functions for humidity
humidity.view()
plt.axvline(x=humidityInput, color='r', linestyle='--')
plt.text(humidityInput, 0.5, f'Humidity: {humidityInput}', rotation=90, ha='right', va='center')

# Plot computed fan speed
fan_speed.compute()
plt.axhline(y=outputFanSpeed, color='g', linestyle='--')
plt.text(temperature.universe[-1], outputFanSpeed, f'Fan Speed: {round(outputFanSpeed, 2)}', ha='right', va='bottom')

plt.show()


fanSpeed.view(sim=fan_speed)