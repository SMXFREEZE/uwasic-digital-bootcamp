# Verification results

September 13 2026

## Changes

The PWM module matches the original UWASIC file byte for byte
The SPI receiver uses the bit count instead of a separate active flag
The shift buffer no longer needs reset or chip select gating because a complete frame replaces all sixteen bits
The counter still rejects incomplete and overlong frames

## Cell usage

| Metric | Original submission | Current build |
| --- | --- | --- |
| Cells excluding fill and tap | 428 | 415 |
| Routed wire length in micrometres | 8468 | 7842 |

The layout uses thirteen fewer cells and meets the target of fewer than 420
The downloaded GDS contains the same 415 cells reported by the build

[Original build](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34664339060)

[Current layout and gate level checks](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34782054221)

## Tests

All eight existing tests pass with no failures or skipped tests
No tests were added or removed for this revision
The PWM tests cover all 256 duty values frequency limits output enables and reset
The measured frequency is approximately 3005 Hz within the required range of 2970 through 3030 Hz

Yosys synthesis and structural checks pass
Verilator checks pass with the usual Tiny Tapeout filename exception
Hosted source simulation documentation generation GDS generation physical precheck gate level simulation and viewer generation all pass

[PWM tests](test/test_pwm.py)

[PWM requirement coverage](docs/pwm_verification.md)

[Source simulation](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34782054234)

[Documentation build](https://github.com/SMXFREEZE/uwasic-digital-bootcamp/actions/runs/34782054196)

The tested implementation is commit da4a7688c549911376db2ca1962b6319745933b5
Later commits update notes and verification records

[Generated layout](https://smxfreeze.github.io/uwasic-digital-bootcamp/tinytapeout.gds)

## Review

Team approval remains pending
No hardware testing has been performed

The README contains the local test commands
The validation directory records test results tool versions and the layout checksum
