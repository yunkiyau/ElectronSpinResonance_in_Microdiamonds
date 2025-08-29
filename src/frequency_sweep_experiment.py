import serial
import time
import numpy as np
import pyvisa
import matplotlib.pyplot as plt
import csv
import matplotlib.ticker as ticker
from datetime import datetime

''' Increasing bin length gives you more photons per bin. Increasing num_bins
gives you more values (Data points) per freq '''

# Connect to SPCM via VISA
def connect_spcm():
    rm = pyvisa.ResourceManager()
    for dev in rm.list_resources():
        try:
            instr = rm.open_resource(dev)
            idn = instr.query("*IDN?")
            if "Thorlabs" in idn or "SPCM" in idn:
                print(f"Connected to SPCM: {idn.strip()}")
                return instr
            instr.close()
        except Exception:
            pass
    raise RuntimeError("SPCM not found via VISA.")


# Configure SPCM for timed bin counting
def configure_spcm(spcm, bin, delay):
    spcm.write("*CLS")
    spcm.write("GATE:MODE 2")       # Free running timed mode
    spcm.write("APD:GATE 0")        # APD always active - counter gating only
    spcm.write(f"GATE:APER {bin}")     # Bin length 
    spcm.write(f"GATE:DEL {delay}")     # Delay (not sure how long this should be - depends on expected arrival time)
                                    # Making this longer seems to make the first few fqs not pick up photons
    spcm.write("ARR:STAT 1")       # Enable array mode
    spcm.write("ARRay:NPOInts 1")        # bins per array - not sure how this works
    spcm.write("STAT:MEAS:CLE")               # Clear accumulated state
    print("SPCM configured for timed bin counting")


# Connect to RF Signal Generator
def connect_dsi(port='COM6', baud=115200):
    ser = serial.Serial(port, baud, timeout=1)
    if not ser.isOpen():
        raise RuntimeError(f"Failed to open {port}")
    print(f"{ser.name} open...")
    return ser

def main():
    bin_length = 1.0
    num_bins = 100
    delay = 0.005

    spcm = connect_spcm()
    dsi = connect_dsi()
    configure_spcm(spcm, bin_length, delay)

    frequencies_mhz = np.arange(2770, 2971, 1)

    count_dict = {}

    dsi.write(b"OUTP:STAT ON\n")
    dsi.write(b"FREQ:CW 0.100000GHZ\n")
    dsi.write(b"POWER 15\n")

    # Interactive plotting
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Photon Counts")
    ax.set_xlim(2.769, 2.972)  # Set fixed x-axis range
    #ax.set_ylim(50000,100000)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:.5f}"))  
    ax.grid(True, linestyle='--', alpha=0.7)
    scatter_line, = ax.plot([], [], 'o', markersize=0.5)
    #avg_line, = ax.plot([], [], '-', label='Average Count')
    #ax.legend()
    plt.show()

    freqs = []
    avg_counts = []

    for freq_mhz in frequencies_mhz:
        freq_ghz_str = f"{freq_mhz / 1000:.6f}GHZ"
        dsi.write(f"FREQ:CW {freq_ghz_str}\n".encode())
        time.sleep(0.025)

        bin_counts = []

        for _ in range(num_bins):  # Take several individual bins
            spcm.write("STAT:MEAS:CLE")
            spcm.write("MEAS:STAR")
            time.sleep(bin_length + delay + 0.01)  # Bin + delay
            response = spcm.query("DATA?")

            try:
                count_str, state_str, index_str = response.strip().split(";")
                count_val = int(count_str)
                bin_counts.append(count_val)
            except ValueError:
                bin_counts.append(0)  # Handle failed parse

        avg_count = np.mean(bin_counts)
        std_count = np.std(bin_counts)
        freq_ghz = round(freq_mhz / 1000, 6)
        count_dict[freq_ghz] = [bin_counts, avg_count, std_count]

        freqs.append(freq_ghz)
        avg_counts.append(avg_count)

        # Update scatter plot with individual bin counts
        scatter_freqs = [freq_ghz] * num_bins

        current_xdata = list(scatter_line.get_xdata())
        current_ydata = list(scatter_line.get_ydata())

        scatter_line.set_xdata(current_xdata + scatter_freqs)
        scatter_line.set_ydata(current_ydata + bin_counts)

        # Update average line plot
        #avg_line.set_xdata(freqs)
        #avg_line.set_ydata(avg_counts)

        std_devs = [count_dict[f][2] for f in freqs]  # Extract std deviations
        ax.errorbar(freqs, avg_counts, yerr=std_devs, fmt='-o', color='orange', capsize=3, label='Average ± Std Dev')

        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)

    spcm.write("MEAS:STOP")
    spcm.close()
    dsi.write(b"OUTP:STAT OFF\n")
    dsi.close()

    # Display summary
    print("\n=== Photon Counts per Frequency ===")
    for freq, (bins, avg, std) in count_dict.items():
        print(f"{freq:.2f} MHz: {bins} → avg = {avg:.2f}\tstd = {std:.2f}")

    # Generate filename with specifics
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"freqsweep_1MHz_{num_bins}steps_{timestamp}.csv"
    with open(output_filename, mode="w", newline='') as f:
        writer = csv.writer(f)
    
        # Header: Frequency + Bin columns + Avg
        bin_headers = [f"Bin {i+1}" for i in range(num_bins)]
        writer.writerow(["Frequency (MHz)"] + bin_headers + ["Average Count", "Std Dev"])

        # Data rows
        for freq, (bins, avg, std) in count_dict.items():
            row = [freq] + bins + avg + std
            writer.writerow(row)

    print(f"\nPhoton count data saved to {output_filename}")

    plt.ioff()
    plt.show()


# Run
if __name__ == "__main__":
    main()