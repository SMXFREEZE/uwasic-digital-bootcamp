# Copyright 2026 Sami El-Figha
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Edge, Timer, with_timeout
from cocotb.utils import get_sim_time

from helpers import configure, outputs, reset, write_register


async def level(dut, high):
    async def wait_for_level():
        while bool(int(dut.uo_out.value) & 1) != high:
            await Edge(dut.uo_out)
        return get_sim_time(units="ns")

    return await with_timeout(wait_for_level(), 700, "us")


async def measure_cycle(dut):
    # Discard a possibly partial cycle before measuring rising edge to rising edge
    await level(dut, False)
    start = await level(dut, True)
    fall = await level(dut, False)
    end = await level(dut, True)
    return 1e9 / (end - start), (fall - start) / (end - start)


@cocotb.test()
async def test_pwm_frequency(dut):
    await reset(dut)
    await configure(dut)
    frequencies = []
    for _ in range(8):
        frequency, duty = await measure_cycle(dut)
        assert 2970 <= frequency <= 3030, f"PWM frequency {frequency} Hz"
        assert abs(duty - 0.5) <= 0.01, f"PWM duty {duty}"
        frequencies.append(frequency)
    dut._log.info("Measured PWM frequency %.6f Hz", sum(frequencies) / len(frequencies))


@cocotb.test()
async def test_pwm_all_duty_values(dut):
    await reset(dut)
    await configure(dut)
    max_error = 0
    for value in range(256):
        await write_register(dut, 4, value)
        if value in (0, 255):
            expected = 0xFFFF if value == 255 else 0
            # Sample more than two full periods even when no edges exist
            for _ in range(710):
                await Timer(1000, units="ns")
                assert outputs(dut) == expected, f"Endpoint duty {value}"
        else:
            frequency, measured = await measure_cycle(dut)
            expected = value / 256
            error = abs(measured - expected)
            max_error = max(max_error, error)
            assert 2970 <= frequency <= 3030, f"Frequency at duty {value}"
            assert error <= 0.01, f"Duty {value}: expected {expected}, got {measured}"
        await Timer(2, units="ns")
    dut._log.info("Verified all 256 duty values with maximum error %.9f", max_error)


@cocotb.test()
async def test_pwm_enable_precedence_all_outputs(dut):
    await reset(dut)
    patterns = [(0, 0xFFFF), (0xFFFF, 0), (0xFFFF, 0xFFFF), (0xA55A, 0x3CC3)]
    patterns += [(1 << bit, 0xFFFF) for bit in range(16)]
    for enable, pwm in patterns:
        await configure(dut, enable=enable, pwm=pwm, duty=96)
        low_state = enable & ~pwm & 0xFFFF
        high_state = enable
        seen = set()
        # Observe actual pins across more than two PWM periods
        # No internal RTL names are needed so the test also works after synthesis
        for _ in range(710):
            await Timer(1000, units="ns")
            actual = outputs(dut)
            assert actual in (low_state, high_state), (
                f"Enable {enable:04x} PWM {pwm:04x} output {actual:04x}"
            )
            assert int(dut.uio_oe.value) == 255
            seen.add(actual)
        assert seen == {low_state, high_state}, f"Missing output state for {enable:04x}"


@cocotb.test()
async def test_reset_during_pwm(dut):
    await reset(dut)
    await configure(dut)
    await Timer(12345, units="ns")
    dut.rst_n.value = 0
    await Timer(20, units="ns")
    assert outputs(dut) == 0
    dut.rst_n.value = 1
    for _ in range(710):
        await Timer(1000, units="ns")
        assert outputs(dut) == 0
    await write_register(dut, 0, 0xA5)
    await write_register(dut, 1, 0x5A)
    assert outputs(dut) == 0x5AA5
