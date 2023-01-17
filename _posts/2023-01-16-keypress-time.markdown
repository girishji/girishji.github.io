---
layout: post
title:  "Keyboard: How Quickly Can You Press a Key"
date:   2023-01-16 10:16:45 +0200
categories:
tags: optical keyboard switch 
keywords: optical, keyboard, switch, phototransistor, ir, led
---

If you ever wondered whether a keypress happens in milliseconds or microseconds
in a keyboard wonder no more.

_TLDR; It takes less than 200us (microsec) to over 1ms (millisec) depending on
the switch and finger speed._

**What is measured?**

A switch has pre-activation (pre-travel), activation and post-activation
distance. In case of Gateron Yellow optical switches pre-activation is about
1mm, activation happens for another 1mm (height of optical elements) and
post-activation distance is about 1.2mm. For other 'non-fast' Gateron MX style
switches pre-activation is 2mm, activation is 1mm, and post-activation is 2mm.
Since the setup uses voltage waveform from an optical switch as a trigger only
the activation process is subject to measurement. Time taken for pre-activation
and post-activation are not accounted for. Secondly, the switch actuator does
not have to travel all the way through the actuation zone for the state change
to be registered in the microcontroller. The GPIO pin registers a "high" when
voltage rises to ~0.8V and "low" when voltage falls below ~2V.

## Setup

![Setup](/assets/tsetup1.jpeg){: width="400"}

The test setup consists of a highly responsive optical switch. The
phototransistor has rise and fall time of a few nanoseconds. You can verify from
the oscilloscope screen. Yellow line represents voltage drop across the
phototransistor while green line is the pulse applied to IR LED. Voltage drop
across phototransistor is inverted owing to the nature of the circuit. Each
horizontal division is 1us.

![phototransistor rise time](/assets/fastsw1.png){: width="550"}

Before measuring key-press time IR LED is driven from a constant voltage source.
When key is pressed IR light is interrupted from entering the base junction of
phototransistor. This corresponds to fall time and since the plot is reversed
the yellow line rises.

The switch used is of Gateron Yellow optical linear variety. About 10
measurements are taken but only a representative sample is presented here.

### Fast Key Press

It takes about 100us for fall time. Each horizontal division is 100us and
vertical division is 2V. Voltage rises from ~0V to ~3.3V. You can observe that
voltage rises very quickly to 0.8V, in less than 50us. This is when GPIO pin
will register state change. These types of fast keypresses are rare in normal
typing though.

![image](/assets/fastkp.png){: width="550"}

### Average Key Press

It takes about 200us to 2ms. Each horizontal division is 100us and vertical
division is 2V as above. Normal typing could be characterized as average.

![image](/assets/avkp.png){: width="550"}

### Lazy Key Press

It takes over 2ms. Each horizontal division is 1ms and vertical division is 2V.
This is generally rare for switch with lighter springs but quite common for
switch with heavier springs.

![image](/assets/lazykp.png){: width="550"}

### Average Key Release

It takes about the same time as key press. Each horizontal division is 100us.

![image](/assets/avkr.png){: width="550"}

### Note ###:

- Although no serious statistical evidence is compiled and sample size is just
  _one_, averaging over 10 keypresses a switch with lighter spring (15gf)
  resulted in faster keypresses compared to heavier Yellow (35gf) and Red (45gf)
  switches.

- With 15gf it is possible (although rare) to get sub 100us keypresses.

![image](/assets/superfastkp.png){: width="550"}

- There is generally a clean rise and fall curve of voltage drop across
  phototransistor. This is the reason why optical keyboards do not require
  debouncing. Even though there is a transition region of voltage (0.8v-1.2v)
  where GPIO pin can read unpredictable logical value, it is generally not the
  case. If such problem indeed was encountered a comparator with hysteresis
  (Schmitt trigger) can be added to the circuit.

- _How fast can an optical switch detect a keypress?_ As you may have noticed
  the optical switch used in this experiment has extremely low rise/fall time.
  So the key event is detected as soon as the voltage crosses TTL logic
  threshold. The switch uses about 2mA current (for IR LED and phototransistor
  combined). Given that USB can supply 500mA, all the switches in the keyboard
  can remain powered up all the time. This linear (non-switched) circuit is only
  limited by how soon the microprocessor can read the GPIO pins. On Nordic's
  nrf52840 a tight loop can read GPIO 'ports' (which contain a group of GPIO pins)
  all at once at 460kHz frequency (see pic). Suffice to say an optical switch
  will not be on the critical path.

![image](/assets/mindelay.png){: width="550"}

- This test does not measure keyboard latency. After the microprocessor detects
  state change event it has to ship the data to the host computer. Since
  keyboards are ususally configured as HID there will be at least 125us polling
  delay if the USB port is configured as HS (high speed) USB or (most likely the
  case) 1ms delay if port is FS (full speed) USB. The application on the host
  computer will have additional delay as well.
