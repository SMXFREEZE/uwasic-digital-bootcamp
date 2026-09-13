# Design notes

## SPI

Transactions contain a write bit followed by a seven bit address and eight data bits
Data is shifted on synchronized rising SCLK edges
A register changes only when chip select returns high after exactly sixteen bits
Reads and unmapped addresses leave the register bank unchanged
The bit counter saturates at seventeen so an overlong frame cannot wrap into a valid transaction

Chip select and the bit count track each frame without a separate active flag
The shift buffer samples each rising SPI clock without a reset or chip select gate
Each complete frame overwrites all sixteen bits before a register can change
Chip select clears the bit count while idle
The counter stops at sixteen and marks the frame invalid if another bit arrives

## Clock crossing

Each SPI input passes through two flip flops clocked at 10 MHz
Delayed synchronized values provide edge detection
The nominal 100 kHz SPI clock leaves many system clock cycles between signal transitions
Functional simulation does not model metastability

## PWM

The PWM module is unchanged from the UWASIC starter
Its divider and eight bit counter produce one period every 3328 system clock cycles
The duty fraction is the register value divided by 256 with a continuously high output at the maximum value
Output enable takes precedence over PWM enable

## Tests

Tests observe the external pins so the same suite can run on RTL and the gate level netlist
The duty sweep covers all 256 values
Constant outputs use bounded observation periods
Other tests cover every output pin mixed enable masks invalid addresses reads malformed frames asynchronous SPI timing and reset recovery
