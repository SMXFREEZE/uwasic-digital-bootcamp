# Design walkthrough

## Signal path

SPI pins enter two stage synchronizers
Delayed copies identify chip select and serial clock edges
The controller collects sixteen bits into a shift register
A valid completed write updates one of five configuration registers
The supplied PWM peripheral combines those registers into sixteen outputs

## Synchronization

The SPI controller and system clock are asynchronous
Sampling near a system clock edge can produce metastability
Two flip flops provide additional settling time before the controller uses the signal
Simulation validates functional timing but does not model or prove analog metastability behavior
At the specified SPI rate each signal is stable for many system clock cycles
This design does not claim support for SPI clocks close to the system clock frequency

## Transaction completion

Waiting for chip select release prevents intermediate bits from changing outputs
The bit counter saturates at seventeen for overlong frames
Additional bits therefore cannot wrap the counter back to a valid length

## PWM reasoning

The supplied divider advances once every thirteen system clock cycles
The PWM counter spans 256 steps
One period therefore lasts 3328 system clock cycles
The output frequency is approximately 3005 Hz at a 10 MHz clock
The comparator holds the waveform high while the counter is below the duty value
The maximum duty value bypasses the comparator to provide a continuously high output
Output enable has priority over PWM enable

## Verification reasoning

The frequency test measures output edges against the specification
The duty test covers every register value
Constant output settings use bounded observations instead of waiting indefinitely for edges
The enable test checks every output and mixed masks across multiple periods
The SPI tests drive phases and periods that differ from the system clock
All assertions use external pins to support both RTL and gate level simulation

## Review questions

Explain why the shift register includes the write bit and address

Trace the controller after fifteen sixteen and seventeen serial clock edges

Explain why synchronizers reduce metastability risk without eliminating it

Calculate the PWM period and expected pulse width for a duty value of 64

Explain how tests detect an upper output enable register connected to the lower bank

Identify which checks remain necessary after functional simulation passes

## Physical checks

Synthesis confirms that RTL can become a digital circuit
It does not establish physical manufacturability or timing closure
The GDS build precheck and gate level simulation must pass before requesting completed bootcamp review
