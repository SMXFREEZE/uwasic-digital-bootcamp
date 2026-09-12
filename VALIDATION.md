# Verification status

Validated locally on September 11 2026

## Completed

Eight simulation tests passed with no failures or skipped tests
The supplied UWASIC SPI regression passed
Every duty value from zero through 255 was verified
All sixteen output pins were tested
Output enable precedence and mixed PWM enable masks were verified
Reads all invalid addresses truncated frames and overlong frames were checked
Reset behavior and asynchronous SPI timing were checked
Yosys synthesis and structural checks passed
Verilator static checks passed with the expected Tiny Tapeout filename naming exception
The supplied PWM source remains unchanged

The measured PWM frequency was approximately 3005 Hz
The accepted range is 2970 through 3030 Hz
The duty sweep matched each expected digital timing ratio

## Pending

GitHub repository publication requires sign in
Hosted GDS generation Tiny Tapeout precheck gate level simulation and documentation generation have not run
No fabrication or hardware testing has been performed
No completion review has been requested in Discord

## Reproduction

Run the commands in the README
Detailed test results and tool versions are recorded in the validation directory
