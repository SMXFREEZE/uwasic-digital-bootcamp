# Copyright 2026 Sami El-Figha
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

CLOCK_NS = 100


async def settle(dut, cycles=10):
    await ClockCycles(dut.clk, cycles)
    await Timer(2, units="ns")


async def reset(dut):
    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 4
    dut.rst_n.value = 0
    cocotb.start_soon(Clock(dut.clk, CLOCK_NS, units="ns").start())
    await settle(dut)
    dut.rst_n.value = 1
    await settle(dut)


def outputs(dut):
    return (int(dut.uio_out.value) << 8) | int(dut.uo_out.value)


def frame(address, data, write=True):
    word = (int(write) << 15) | (address << 8) | data
    return [(word >> bit) & 1 for bit in range(15, -1, -1)]


async def finish_spi(dut):
    dut.ui_in.value = 4
    await Timer(1000, units="ns")


async def send_bits(dut, bits, finish=True, half_period_ns=5003):
    # The SPI period is deliberately not an integer number of system cycles
    dut.ui_in.value = 0
    await Timer(half_period_ns, units="ns")
    for bit in bits:
        dut.ui_in.value = bit << 1
        await Timer(half_period_ns, units="ns")
        dut.ui_in.value = (bit << 1) | 1
        await Timer(half_period_ns, units="ns")
    if finish:
        await finish_spi(dut)


async def write_register(dut, address, data):
    await send_bits(dut, frame(address, data))


async def configure(dut, enable=0xFFFF, pwm=0xFFFF, duty=128):
    for address, data in enumerate(
        [enable & 255, enable >> 8, pwm & 255, pwm >> 8, duty]
    ):
        await write_register(dut, address, data)
