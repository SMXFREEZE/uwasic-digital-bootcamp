# PWM verification

The PWM tests are in [test_pwm.py](../test/test_pwm.py)
They run alongside the supplied SPI regression through [the test Makefile](../test/Makefile)
The same suite runs against the source design and the generated gate level netlist

## Onboarding requirements

| Requirement | Test | Check |
| --- | --- | --- |
| Frequency within one percent of 3 kHz | test_pwm_frequency | Eight complete periods between 2970 and 3030 Hz |
| Full duty sweep | test_pwm_all_duty_values | All 256 register settings with at most one percentage point of error |
| Zero duty | test_pwm_all_duty_values | Both output banks remain low for more than two periods |
| Half duty | test_pwm_frequency and test_pwm_all_duty_values | Rising and falling edge measurements at register value 128 |
| Full duty | test_pwm_all_duty_values | Both output banks remain high for more than two periods |
| Output enable overrides PWM | test_pwm_enable_precedence_all_outputs | Disabled outputs remain low with PWM enabled |
| Independent control of sixteen outputs | test_pwm_enable_precedence_all_outputs | Each output selected separately plus mixed enable masks |
| Bounded waits | level and test_pwm_all_duty_values | Transition waits expire after 700 microseconds and constant outputs use fixed observation periods |
| Reset | test_reset_during_pwm | Active PWM stops on reset and output registers return to zero |

## Measurement

Frequency is measured from one rising edge to the next
Duty is measured from the rising edge to the falling edge divided by the complete period
The expected fraction is the register value divided by 256
The maximum register value is treated as continuously high

Measurements use only the external output pins
They do not inspect the internal PWM counter

## Run the PWM tests

```sh
make -C test MODULE=test_pwm
python scripts/check_results.py test/results.xml
```

Run the full suite with make in the test directory

[UWASIC design requirements](https://docs.uwasic.com/s/onboarding/doc/2-about-our-design-I2KgIRAoEj)

[UWASIC PWM testing guide](https://docs.uwasic.com/s/onboarding/doc/7-writing-pwm-tests-ABrnH5kDNW)
