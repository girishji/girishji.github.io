---
layout: post
title:  "Optical Keyboard: Circuit Design Tips"
date:   2022-08-17 12:16:45 +0200
categories: opticalkb
---


## Introduction

Optical switch (like the kind sold by Gateron and Keychron) depends on an IR
LED (IR) and a phototransistor (PT) pair for
operation. When switch is actuated, a plunger blocks the IR light from striking
the PT causing voltage change across collector-emittor junction of PT. Unlike a
mechanical switch, an optical switch does not have copper contacts that rub
against the plastic shaft. Since there is no resistance caused by rubbing,
optical switches are extremely smooth. They can be used with low tension
springs (15gf), while a mechanical switch will not pop up reliably under this
low spring force. Secondly, optical switches respond quicker than mechanical
switches since there is no debounce delay. Scan rate of matrix can be as high
as the USB polling rate. This helps in gaming applications.

The fly in the ointment is that optical switches are not suitable for
handwiring (although possible). One needs at least a [single-switch pcb][optical-amoeba] to
even consider handwiring. On the other hand, it has become affordable to get pcb's made and SMD
componenets assembled in China ([jlcpcb][jlcpcb] charges for only 2 pcb's for SMD assembly if you choose
green FR4). [KiCad][kicad-org] has also matured, with decent
[scripting support]({% post_url 2022-08-17-kicad-python-footprints-curved-tracks-edge-cuts %}).
So designing the whole optical keyboard pcb and getting a few copies made is an
attractive proposition for DIY projects.

## Circuit

There are two ways you can measure voltage drop across PT. The circuit shown in
Figure (A) is a common-emitter amplifier, with IR shown on left and PT on the
right. Light input at the base causes the output (**Vout**) to decrease from high
to low. If you were to connect **Vout** to the GPIO pin of MCU it would read LOW to
HIGH when switch is depressed. The circuit shown in Figure (B) is a
common-collector amplifier with an output (**Vout**) increasing from low to high in
response to light input. In this case MCU pin will read HIGH to LOW. For these
circuits to operate in the switching mode, the load resistor (**RL**) should be set
in relation with the collector current (**Ic**) as
[**Vcc** < **RL** × **Ic**][photodevices].

![image](/assets/opic1.png){: width="550" }

*What are the values of **R** and **RL**?*

Phototransistors have excellent sensitivity; a photon absorbed at the junction
creates a corresponding electron-hole pair. But it takes a lot of electrons for
the current to be noticed above thermal noise. The more IR light that falls on
PT, the higher will be the collector current (**Ic**) and lower will be the switching time. 

Reducing **R** will increase current (**I**) flowing through IR. But the value of load
resistance (**RL**) has to be matched with **R** for PT to work as a switch. Higher the value
of **RL** higher will be sensitivity of PT. The smaller the current flowing through
phototransistor, the less light it takes to switch it. For any value of **R**
(within the working range) there is a corresponding value of **RL** below which
the PT is not sensitive enough. Below the threshold value of **RL**, the GPIO pin 
will not register anything as you press the switch, or the pin may register
random values not unlike a floating pin. Here are some sample
values:

For **3.3v**:

|  **R**  |  **I**  |  **RL** (threshold) |  **Ic** |
| --- | --- | --- | --- |
| 540 | 4.2 mA | 4k | 0.83 mA |
| 680 | 3.2 mA | 5k | 0.66 mA |
| 1k | 2.1 mA | 15k | 0.22 mA |
| 1.5k | 1.4 mA | 27k | 0.18 mA |
| 2.2k | 1.0 mA | 45k | 0.1 mA |

* Voltage across **R** is ~2.14V
* **I** = 2.14/**R**, and **Ic** ~ 3.3/**RL**
* To get reliable switching use **RL** atleast >20% above threshold value
* **R** and **RL** are in ohms

Switching can be accomplished at low currents (~1 mA at IR and 0.2 mA at PT) reliably as long as you
keep **RL** high. This means a single GPIO pin set as "Output" can drive a row of
15 switches in a typical keyboard. STM32 based MCU can supply up to 20 mA per GPIO
pin. RP2020 can provide upto 17 mA per GPIO pin.

Typical rise time of PT is about 15 uSec at 1 mA current. This is the minimum
amount of time you have to wait after activating IR ("Output" GPIO pin going HIGH) and before taking reading
at the "Input" GPIO pin. At low current (**Ic**) switching time will be
slightly longer, but not by much (20 uSec can work).


![image](/assets/opic2.png){: width="350" }


## Optical Matrix

The number of switches in a full-sized keyboard far exceed the number of GPIO pins available in a MCU. A solution
to this problem is to connect switches in a matrix. Optical matrix is not much different from matrix used
for mechanical switches. You either select a column and read rows one by one, or *vice versa*.

The above circuit cannot be directly applied to a matrix. If you connect **Vcc**
(above) to a GPIO pin (set as "Output") it will not work when there are 
additional switches also connected this way. When you depress one switch, current from that PT will be
redirected to another switch's IR. So the GPIO pin (set as "Input") will not
register any change in voltage. You could use diodes to solve this problem, but
even fast diodes (like 1N4148) will interfere with the rise time of PT and
affect scan rate (will be <70 Hz). The solution is to split the power source of IR and PT; have IR driven
by GPIO pin and PT driven by 3v3 pin.


### Select Column and Read Rows

In this arrangement we select a column (change column pin output to "High" and
wait for PT to "rise"), and read row pins one by one. After we are done,
change column pin output back to "Low" and proceed to the next column pin.
Reading time is usually negligible compared to PT rise time.
A full matrix scan will take approximately `rise_time x number_of_columns`. For 15 column
keyboard and 20 uSec wait time the matrix scan rate will be 3.33 kHz.

![image](/assets/opic4.png){: width="550" }

### Select Row and Read Columns

In this arrangement we select a row and read column pins one by one.
A full matrix scan will take `rise_time x number_of_rows`. This arrangment will produce higher scan rate.
For a 5 row keyboard scan rate will be 10 khz.

![image](/assets/opic3.png){: width="550" }

USB 1.1 supports 1 mSec polling (1 kHz), and USB 2 supports up to 8 kHz. Since
these polling packets are small, data transfer rate limitation does not apply.
In summary, you can have a *very quick* keyboard.


***

### Optical Keyboards


- [Optical keyboard with MX switches](https://github.com/girishji/optical-keyboard-mx)
- [Optical keyboard with low profile switches](https://github.com/girishji/keychron-optical-keyboard)
- [Amoeba single switch pcb](https://github.com/girishji/optical-amoeba)
- [Another optical keyboard](https://github.com/girishji/optical-keyboard)
- [Yet another](https://github.com/Dachtire/sok42)
- [Photdevices](http://educypedia.karadimov.info/library/Sharp%20photodevices.pdf)


### Thanks

[Optical Future](https://discord.com/login?redirect_to=%2Fchannels%2F715975244896272618)


[kicad-org]: https://www.kicad.org/
[photodevices]: http://educypedia.karadimov.info/library/Sharp%20photodevices.pdf
[optical-amoeba]: https://github.com/girishji/optical-amoeba
[jlcpcb]: https://jlcpcb.com/
