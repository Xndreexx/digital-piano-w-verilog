import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start Piano Simulation")

    # Reloj de 10 MHz (periodo 100 ns) - en cocotb 2.1.0 se usa 'unit' en singular
    clock = Clock(dut.clk, 100, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset inicial
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)

    # 1. Verificar reposo: Display debe mostrar "-" (uo_out[7:1] = 0b1000000 = 0x40)
    seg7 = (int(dut.uo_out.value) >> 1) & 0x7F
    assert seg7 == 0x40, f"Error en reposo: esperado 0x40, obtenido {hex(seg7)}"

    # 2. Presionar tecla Do (ui_in[0] = 1) en Octava 4 (uio_in[6:5] = 10)
    dut.ui_in.value = 0b00000001
    dut.uio_in.value = 0b01000000
    await ClockCycles(dut.clk, 50)

    # Verificar que el display muestre "C" (0b0111001 = 0x39)
    seg7 = (int(dut.uo_out.value) >> 1) & 0x7F
    assert seg7 == 0x39, f"Error en nota Do: esperado 0x39 ('C'), obtenido {hex(seg7)}"

    # 3. Probar acorde de 3 notas (Do + Mi + Sol) y verificar que haya actividad de audio
    dut.ui_in.value = 0b00010101
    audio_transitions = 0
    prev_audio = int(dut.uo_out.value) & 1

    for _ in range(500):
        await ClockCycles(dut.clk, 1)
        curr_audio = int(dut.uo_out.value) & 1
        if curr_audio != prev_audio:
            audio_transitions += 1
            prev_audio = curr_audio

    assert audio_transitions > 10, "Error: No se detectaron pulsos Sigma-Delta en uo_out[0]"
    dut._log.info(f"Prueba exitosa! Transiciones de audio detectadas: {audio_transitions}")
