---
layout: post
title:  "Keyboard: How Quickly Can You Press a Key"
date:   2022-08-17 12:16:45 +0200
categories:
tags: optical keyboard switch 
keywords: optical, keyboard, switch, phototransistor, ir, led
---

If you ever wondered whether a keypress happens in milliseconds or microseconds
in a keyboard wonder no more. I have systematically measured key-press and
key-release times.

TLDR; It takes about 100us to over 2ms.

The test setup consists of a highly responsive optical switch. The phototransistor
has rise and fall time of a few nanoseconds. In the following oscilloscope
screen capture yellow line represents phototransistor rise and fall time while
green line is the pulse applied to IR LED. Voltage drop across phototransistor
is inverted owing to the nature of the circuit. Each horizontal division is 1us. 

![phototransistor rise time](/assets/fastsw1.png){: width="550"}

Before measuring key-press time IR LED is driven from a constant voltage
source. When key is pressed IR light is interrupted from entering the base
junction of phototransistor. This corresponds to fall time and since the plot
is reversed the yellow line rises. 

The switch used is Gateron Yellow Optical Linear variety.

#### Fast Key Press ####

It takes about 100us. Each horizontal division is 100us.

![image](/assets/fastkp.png){: width="550"}

#### Average Key Press ####

It takes about 200us to 500us. Each horizontal division is 100us. Normal typing
could be characterized as average.

![image](/assets/avkp.png){: width="550"}

#### Lazy Key Press ####

It takes about 2ms or longer. Each horizontal division is 1ms. This is
generally rare for switch with lighter springs. 

![image](/assets/lazykp.png){: width="550"}

#### Average Key Release ####

It takes about 200us to 500us. Each horizontal division is 100us.

![image](/assets/avkr.png){: width="550"}


**Notes**:

- Although no serious statistical evidence is compiled, just averaging over 10
keypresses, a switch with lighter spring (15gf) resulted in faster keypresses
compared to heavier Yellow (35gf) and Red (45gf) switches. 

- With 15gf it is possible (although rare) to get sub 100us keypresses.

![image](/assets/superfastkp.png){: width="550"}

- There is generally a clean rise and fall curve of voltage drop across
  phototransistor. This is the reason why optical keyboards do not require
  debouncing. Even though there is a transition region of voltage (0.8v-1.2v)
  where GPIO pin can read unpredictable logical value, it is generally not a
  problem. If such problem indeed was encountered a comparator with hysteresis
  (Schmitt trigger) can be added to the circuit. 

