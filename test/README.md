# Simulation

The testbench instantiates the project with a 10 MHz system clock
Dependencies are listed in requirements.txt

```sh
make
python ../scripts/check_results.py results.xml
```

The suite runs the supplied SPI regression plus PWM and SPI edge case tests
The result checker fails when a test fails or the result file contains no tests

## Gate level simulation

The GDS workflow supplies the synthesized netlist and process models

```sh
make GATES=yes
```

## Waveforms

Simulation produces tb.vcd for inspection in GTKWave or Surfer
