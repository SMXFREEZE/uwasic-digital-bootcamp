# Verification status

Validated on September 12 2026

## Review revision

The PWM divider counter is narrowed from eleven bits to four bits
It resets after twelve so the reachable values are zero through twelve
The seven removed upper bits were always zero after reset
The divider period and PWM behavior are unchanged

## Cell usage

| Metric | Original submission | Review revision |
| --- | --- | --- |
| Mapped cells excluding fill and tap | 428 | 390 |
| Routed wire length in micrometres | 8468 | 7925 |

The revised layout uses thirty eight fewer cells
The downloaded GDS was independently checked against the reported cell count

[Original build](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34664339060)

[Revised build](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34674874098)

## PWM verification

[PWM test source](test/test_pwm.py)

[Requirement coverage](docs/pwm_verification.md)

The tests cover all 256 duty values frequency limits both output banks mixed enable masks and reset
Constant high and low outputs use bounded observation periods
Transition waits use explicit timeouts
The measured PWM frequency is approximately 3005 Hz within the accepted range of 2970 through 3030 Hz

## Results

Eight local simulation tests passed with no failures or skipped tests
Yosys synthesis and structural checks passed
Verilator checks passed with the expected Tiny Tapeout filename naming exception
A partial first frame after reset was added to the SPI regression

[Hosted source simulation passed](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34674874068)

[GDS generation physical precheck gate level simulation and viewer generation passed](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34674874098)

[Documentation generation passed](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34674874083)

The tested implementation is commit 7fd000ed1758d1bdd934c53753d639993cd35afa
Later commits update documentation and verification records

[Generated chip layout](https://smxfreeze.github.io/uwasic-digital-bootcamp/tinytapeout.gds)

## Team review

The revision addresses the cell usage feedback and includes direct links to the PWM tests
Team approval remains pending
No fabrication or hardware testing has been performed

## Reproduction

Run the commands in the README
Detailed test results tool versions and layout checksums are recorded in the validation directory
