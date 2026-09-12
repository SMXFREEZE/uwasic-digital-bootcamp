# Copyright 2026 Sami El-Figha
# SPDX-License-Identifier: Apache-2.0

import random

import cocotb
from cocotb.triggers import Timer

from helpers import configure, finish_spi, frame, outputs, reset, send_bits, write_register


@cocotb.test()
async def test_spi_commits_only_complete_frames(dut):
    await reset(dut)
    # A partial first frame must not expose unknown shift register contents
    for length in (1, 8, 15):
        await send_bits(dut, frame(0, 0xFF)[:length])
        assert outputs(dut) == 0, f"Partial first frame length {length} changed output"
    await write_register(dut, 0, 0xA5)
    await send_bits(dut, frame(0, 0x3C), finish=False)
    assert outputs(dut) == 0xA5, "Register changed before chip select release"
    await finish_spi(dut)
    assert outputs(dut) == 0x3C
    for length in (0, 1, 7, 8, 15, 17, 32, 48, 80):
        bits = (frame(0, 0xFF) * 5)[:length]
        await send_bits(dut, bits)
        assert outputs(dut) == 0x3C, f"Malformed frame length {length} changed output"
    await write_register(dut, 0, 0x69)
    assert outputs(dut) == 0x69, "SPI did not recover after malformed frames"


@cocotb.test()
async def test_spi_reads_invalid_addresses_and_idle_clocks(dut):
    await reset(dut)
    await configure(dut, enable=0xA55A, pwm=0xFFFF, duty=255)
    for address in range(5):
        await send_bits(dut, frame(address, 0, write=False))
        assert outputs(dut) == 0xA55A, f"Read modified register {address}"
    # Turning PWM off reveals whether reads modified the hidden enable masks
    await write_register(dut, 4, 0)
    assert outputs(dut) == 0
    await write_register(dut, 4, 255)
    for address in range(5, 128):
        await write_register(dut, address, 0)
        assert outputs(dut) == 0xA55A, f"Invalid write at address {address}"
    await write_register(dut, 4, 0)
    assert outputs(dut) == 0, "Invalid address modified a PWM enable mask"
    await write_register(dut, 2, 0)
    await write_register(dut, 3, 0)
    assert outputs(dut) == 0xA55A
    for bit in frame(0, 0):
        dut.ui_in.value = 4 | (bit << 1)
        await Timer(5003, units="ns")
        dut.ui_in.value = 5 | (bit << 1)
        await Timer(5003, units="ns")
    await finish_spi(dut)
    assert outputs(dut) == 0xA55A, "Clocks while deselected changed output"


@cocotb.test()
async def test_spi_asynchronous_timing_and_reset(dut):
    await reset(dut)
    rng = random.Random(20260911)
    expected = 0
    for index in range(64):
        address = index % 2
        data = rng.randrange(256)
        await Timer(rng.randrange(1, 100), units="ns")
        await send_bits(dut, frame(address, data), half_period_ns=rng.randrange(4500, 5600))
        mask = 255 << (8 * address)
        expected = (expected & ~mask) | (data << (8 * address))
        assert outputs(dut) == expected
    await send_bits(dut, frame(0, 255)[:9], finish=False)
    dut.rst_n.value = 0
    await Timer(500, units="ns")
    assert outputs(dut) == 0
    dut.ui_in.value = 4
    dut.rst_n.value = 1
    await Timer(1000, units="ns")
    await write_register(dut, 1, 0x81)
    assert outputs(dut) == 0x8100
