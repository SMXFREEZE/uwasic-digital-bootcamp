## How it works

This design implements the UWASIC digital onboarding peripheral for Sami El Figha in Electrical Engineering

A write only SPI interface controls sixteen outputs through five configuration registers
The system clock operates at 10 MHz and the SPI clock at approximately 100 kHz
SPI mode zero captures the most significant bit first on rising serial clock edges

Each transaction contains one write bit seven address bits and eight data bits
The write bit must be one
Registers update only when chip select returns high after exactly sixteen bits
Reads invalid addresses incomplete frames and overlong frames are ignored

| Address | Register | Reset |
| --- | --- | --- |
| 0x00 | Enable outputs 0 through 7 | 0x00 |
| 0x01 | Enable outputs 8 through 15 | 0x00 |
| 0x02 | Enable PWM on outputs 0 through 7 | 0x00 |
| 0x03 | Enable PWM on outputs 8 through 15 | 0x00 |
| 0x04 | Shared PWM duty value | 0x00 |

Disabled outputs remain low
Enabled outputs remain high when PWM is disabled
Enabled outputs follow the common PWM waveform when PWM is enabled
All eight bidirectional pins are configured as outputs

The supplied PWM peripheral divides the system clock by thirteen and then by 256
This produces approximately 3005 Hz at a 10 MHz system clock
The duty fraction is the register value divided by 256
The maximum register value forces the waveform continuously high
A zero register value forces it low

Two flip flops synchronize each SPI input before edge detection in the system clock domain
Active low reset clears all configuration registers and output values

## How to test

Connect the system clock and reset
Connect SCLK to input zero COPI to input one and active low chip select to input two
Keep chip select high between transactions

To enable PWM on output zero write one to address zero and address two
Write 128 to address four for a half duty waveform
Measure output zero with an oscilloscope or logic analyzer
Expected frequency is between 2970 and 3030 Hz

The automated Cocotb suite retains the supplied SPI test and adds measurements for every duty value
It checks all sixteen outputs enable precedence invalid addresses reads malformed transactions reset recovery and asynchronous SPI timing
Tests use external pins so that they can also run against the synthesized netlist

## External hardware

A clock source and an SPI controller are sufficient to configure the design
An oscilloscope or logic analyzer can measure its outputs
LEDs require suitable series resistors and loads beyond pin drive capability require an external driver
