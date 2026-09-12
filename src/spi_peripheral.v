/*
 * Copyright (c) 2026 Sami El-Figha
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module spi_peripheral (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       ncs,
    input  wire       sclk,
    input  wire       copi,
    output reg  [7:0] en_reg_out_7_0,
    output reg  [7:0] en_reg_out_15_8,
    output reg  [7:0] en_reg_pwm_7_0,
    output reg  [7:0] en_reg_pwm_15_8,
    output reg  [7:0] pwm_duty_cycle
);

    // SPI inputs are asynchronous to clk
    // Only second stage values are used by the transaction logic
    (* ASYNC_REG = "TRUE" *) reg [1:0] ncs_sync;
    (* ASYNC_REG = "TRUE" *) reg [1:0] sclk_sync;
    (* ASYNC_REG = "TRUE" *) reg [1:0] copi_sync;
    reg ncs_previous;
    reg sclk_previous;

    wire ncs_falling = ncs_previous && !ncs_sync[1];
    wire ncs_rising = !ncs_previous && ncs_sync[1];
    wire sclk_rising = !sclk_previous && sclk_sync[1];

    reg active;
    reg [4:0] bit_count;
    reg [15:0] transaction;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ncs_sync <= 2'b11;
            sclk_sync <= 2'b00;
            copi_sync <= 2'b00;
            ncs_previous <= 1'b1;
            sclk_previous <= 1'b0;
        end else begin
            ncs_sync <= {ncs_sync[0], ncs};
            sclk_sync <= {sclk_sync[0], sclk};
            copi_sync <= {copi_sync[0], copi};
            ncs_previous <= ncs_sync[1];
            sclk_previous <= sclk_sync[1];
        end
    end

    // A complete frame overwrites every shift bit before it can be committed
    // Keeping the shift register unreset avoids reset and clear gates on the data path
    always @(posedge clk) begin
        if (active && !ncs_sync[1] && sclk_rising && bit_count < 5'd16)
            transaction <= {transaction[14:0], copi_sync[1]};
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            active <= 1'b0;
            bit_count <= 5'd0;
            en_reg_out_7_0 <= 8'd0;
            en_reg_out_15_8 <= 8'd0;
            en_reg_pwm_7_0 <= 8'd0;
            en_reg_pwm_15_8 <= 8'd0;
            pwm_duty_cycle <= 8'd0;
        end else if (ncs_falling) begin
            active <= 1'b1;
            bit_count <= 5'd0;
        end else if (ncs_rising) begin
            // Commit exactly one complete write when chip select is released
            // Reads and invalid addresses leave every register unchanged
            if (active && bit_count == 5'd16 && transaction[15]) begin
                case (transaction[14:8])
                    7'h00: en_reg_out_7_0 <= transaction[7:0];
                    7'h01: en_reg_out_15_8 <= transaction[7:0];
                    7'h02: en_reg_pwm_7_0 <= transaction[7:0];
                    7'h03: en_reg_pwm_15_8 <= transaction[7:0];
                    7'h04: pwm_duty_cycle <= transaction[7:0];
                    default: begin end
                endcase
            end
            active <= 1'b0;
        end else if (active && !ncs_sync[1] && sclk_rising) begin
            if (bit_count < 5'd16) begin
                bit_count <= bit_count + 5'd1;
            end else begin
                // Saturation prevents long malformed frames wrapping to valid
                bit_count <= 5'd17;
            end
        end
    end

endmodule
