# Verification status

Validated on September 11 2026

## Simulation and static checks

Eight local simulation tests passed with no failures or skipped tests
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

## Hosted checks

[Simulation passed](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34664351792)

[GDS generation physical precheck gate level simulation and viewer generation passed](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34664339060)

[Documentation generation passed](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34664357022)

The initial hosted run tested commit 69c54a149c369b87571541ef3f0a0aa1e9663848

The review revision removes unnecessary reset and clear logic from the SPI transaction buffer
All eight local tests pass including a partial first frame after reset
Local synthesis reduces the SPI module from 134 to 117 generic cells
A fresh hosted build is required to measure mapped cells and validate the revised layout

[Generated chip layout](https://smxfreeze.github.io/uwasic-digital-bootcamp/tinytapeout.gds)

## Review status

The public repository was posted in the UWASIC onboarding forum
Review was requested from the digital project lead on September 11 2026
Team review and onboarding approval remain pending

No fabrication or hardware testing has been performed

## Reproduction

Run the commands in the README
Detailed test results and tool versions are recorded in the validation directory
