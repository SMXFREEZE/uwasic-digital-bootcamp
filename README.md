# UWASIC Digital Onboarding

Sami El Figha

Electrical Engineering

## Project

An SPI controlled peripheral with sixteen independently enabled outputs and a shared PWM generator

The implementation follows the UWASIC digital onboarding specification
The supplied PWM module is retained unchanged
The new SPI module commits complete writes when chip select returns high

## Verification

The suite includes the original UWASIC SPI test and coverage for every duty setting all sixteen outputs invalid addresses reads malformed frames reset behavior and asynchronous SPI timing

## Run locally

Install Icarus Verilog and Python with the dependencies below

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r test/requirements.txt
make -C test
python scripts/check_results.py test/results.xml
```

## Repository contents

| Path | Purpose |
| --- | --- |
| src/spi_peripheral.v | SPI synchronization framing validation and registers |
| src/pwm_peripheral.v | Original UWASIC PWM peripheral |
| src/project.v | Tiny Tapeout integration |
| test/test.py | Original SPI regression |
| test/test_pwm.py | Frequency duty sweep enable controls and reset checks |
| test/test_spi_edges.py | Protocol robustness and asynchronous timing |
| docs/info.md | Tiny Tapeout datasheet |
| docs/design_walkthrough.md | Design reasoning and review questions |
| VALIDATION.md | Recorded verification status |

## GitHub workflows

The test workflow runs the complete simulation suite
The GDS workflow builds the layout runs Tiny Tapeout prechecks and repeats the tests against the gate level netlist
The documentation workflow builds the datasheet

Enable GitHub Actions for a fork and select GitHub Actions as the Pages source to publish the layout viewer
Physical design and gate level checks require successful hosted workflow runs before the bootcamp can be considered complete

## Sources

[UWASIC onboarding guide](https://docs.uwasic.com/s/onboarding)

[UWASIC starter repository](https://github.com/UW-ASIC/onboarding-start)

This project retains the Apache license and original source attribution
