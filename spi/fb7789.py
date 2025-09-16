#!/usr/bin/env python3
import spidev
import time
import os
import struct
import mmap
import sys

# GPIO pins
DC_PIN = 57    # Data/Command
RESET_PIN = 56 # Reset

# Display dimensions - Landscape mode with top offset
WIDTH = 320
HEIGHT = 170
OFFSET_X = 0    # No horizontal offset
OFFSET_Y = 35   # 35px top offset

# Quiet mode - set to True to disable all console output
QUIET_MODE = True

def print_quiet(*args, **kwargs):
    """Only print if not in quiet mode"""
    if not QUIET_MODE:
        print(*args, **kwargs)

def setup_gpio():
    """Export and setup GPIO pins"""
    pins = [DC_PIN, RESET_PIN]
    
    for pin in pins:
        if not os.path.exists(f"/sys/class/gpio/gpio{pin}"):
            try:
                with open("/sys/class/gpio/export", "w") as f:
                    f.write(str(pin))
                time.sleep(0.01)
            except Exception as e:
                if not QUIET_MODE:
                    print(f"Warning: Could not export GPIO {pin}: {e}")
    
    time.sleep(0.1)
    
    # Set direction to output for GPIO pins
    for pin in pins:
        try:
            with open(f"/sys/class/gpio/gpio{pin}/direction", "w") as f:
                f.write("out")
        except Exception as e:
            if not QUIET_MODE:
                print(f"Warning: Could not set GPIO {pin} direction: {e}")

def gpio_write(pin, value):
    """Write value to GPIO pin"""
    try:
        with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f:
            f.write("1" if value else "0")
    except Exception as e:
        if not QUIET_MODE:
            print(f"Warning: Could not write to GPIO {pin}: {e}")

class ST7789:
    def __init__(self, quiet=True):
        self.spi = None
        self.width = WIDTH
        self.height = HEIGHT
        self.offset_x = OFFSET_X
        self.offset_y = OFFSET_Y
        self.fb_data = None
        self.fb_size = None
        self.quiet = quiet
        self.line_length = 640  # From your fbset output
        
        # Pre-calculated values for optimization
        self.total_pixels = WIDTH * HEIGHT
        self.bytes_per_pixel = 2
        self.bytes_per_line = self.line_length
        
    def print(self, *args, **kwargs):
        """Only print if not in quiet mode"""
        if not self.quiet:
            print(*args, **kwargs)
    
    def init_framebuffer(self):
        """Initialize framebuffer memory mapping"""
        try:
            # Open framebuffer device
            self.fb_fd = os.open('/dev/fb0', os.O_RDONLY)
            
            # Get framebuffer size based on line length
            self.fb_size = self.line_length * HEIGHT
            
            # Memory map the framebuffer
            self.fb_data = mmap.mmap(self.fb_fd, self.fb_size, mmap.MAP_SHARED, mmap.PROT_READ)
            
            self.print(f"Framebuffer initialized: {WIDTH}x{HEIGHT}, line_length={self.line_length}, total_size={self.fb_size} bytes")
            return True
        except Exception as e:
            self.print(f"Error initializing framebuffer: {e}")
            return False
    
    def close_framebuffer(self):
        """Close framebuffer resources"""
        if hasattr(self, 'fb_data') and self.fb_data:
            self.fb_data.close()
        if hasattr(self, 'fb_fd'):
            os.close(self.fb_fd)
    
    def init_spi(self):
        """Initialize SPI device with 40MHz"""
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)  # SPI bus 0, device 0
            self.spi.max_speed_hz = 40000000  # 40MHz
            self.spi.mode = 0
            self.spi.bits_per_word = 8
            self.spi.lsbfirst = False
            self.spi.threewire = False
            self.print("SPI initialized at 40MHz")
            return True
        except Exception as e:
            self.print(f"Error initializing SPI: {e}")
            return False
    
    def write_command(self, cmd):
        """Write command to display"""
        gpio_write(DC_PIN, 0)
        self.spi.xfer2([cmd])
    
    def write_data(self, data):
        """Write data to display with safe chunking"""
        gpio_write(DC_PIN, 1)
        
        if isinstance(data, (list, bytearray)):
            # Safe chunk size to avoid buffer issues
            chunk_size = 4096
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                self.spi.xfer2(chunk)
        else:
            self.spi.xfer2([data])
    
    def reset(self):
        """Reset the display"""
        self.print("Resetting display...")
        gpio_write(RESET_PIN, 1)
        time.sleep(0.1)
        gpio_write(RESET_PIN, 0)
        time.sleep(0.1)
        gpio_write(RESET_PIN, 1)
        time.sleep(0.12)
    
    def init_display(self):
        """Initialize ST7789 display"""
        self.print("Initializing display...")
        setup_gpio()
        
        if not self.init_spi():
            return False
        
        self.reset()
        
        # ST7789 initialization sequence
        init_commands = [
            (0x01, None, 150),           # SWRESET
            (0x11, None, 150),           # SLPOUT
            (0x3A, [0x55], 10),          # COLMOD
            (0x36, [0x60], 10),          # MADCTL
            (0x2A, [0x00, 0x00, 0x01, 0x3F], 10),  # CASET
            (0x2B, [0x00, 0x00, 0x00, 0xEF], 10),  # RASET
            (0x21, None, 10),            # INVON
            (0x13, None, 10),            # NORON
            (0x29, None, 150),           # DISPON
        ]
        
        for cmd, data, delay_ms in init_commands:
            self.write_command(cmd)
            if data:
                self.write_data(data)
            time.sleep(delay_ms / 1000.0)
        
        self.print("Display initialization completed")
        return True
    
    def set_window(self, x0, y0, x1, y1):
        """Set display window for drawing"""
        # Apply the offset to Y coordinates
        y0_offset = y0 + self.offset_y
        y1_offset = y1 + self.offset_y
        
        self.write_command(0x2A)  # CASET
        self.write_data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])
        
        self.write_command(0x2B)  # RASET
        self.write_data([y0_offset >> 8, y0_offset & 0xFF, y1_offset >> 8, y1_offset & 0xFF])
        
        self.write_command(0x2C)  # RAMWR
    
    def render_framebuffer_fast(self):
        """Fast rendering with 2-line chunks"""
        if not self.fb_data:
            return False
        
        self.set_window(0, 0, self.width - 1, self.height - 1)
        
        # Process 2 lines at a time for better performance
        chunk_lines = 2
        chunk_size = self.width * chunk_lines * 2
        chunk_buffer = bytearray(chunk_size)
        
        for chunk_start in range(0, self.height, chunk_lines):
            chunk_end = min(chunk_start + chunk_lines, self.height)
            actual_lines = chunk_end - chunk_start
            pixels_in_chunk = self.width * actual_lines
            
            # Convert chunk
            chunk_index = 0
            for y in range(chunk_start, chunk_end):
                line_start = y * self.bytes_per_line
                for x in range(self.width):
                    pixel_start = line_start + (x * self.bytes_per_pixel)
                    
                    # Read and convert pixel
                    pixel_low = self.fb_data[pixel_start]
                    pixel_high = self.fb_data[pixel_start + 1]
                    
                    # Convert from framebuffer format to RGB565
                    red = (pixel_high >> 3) & 0x1F
                    green = ((pixel_high & 0x07) << 3) | ((pixel_low >> 5) & 0x07)
                    blue = pixel_low & 0x1F
                    
                    display_color = (red << 11) | (green << 5) | blue
                    
                    chunk_buffer[chunk_index] = (display_color >> 8) & 0xFF
                    chunk_buffer[chunk_index + 1] = display_color & 0xFF
                    chunk_index += 2
            
            # Send chunk
            self.write_data(chunk_buffer[:chunk_index])
        
        return True
    
    def test_colors(self):
        """Test function to verify color correctness - ORIGINAL TEST"""
        if not self.quiet:
            print("Testing colors...")
        
        # Test basic colors
        colors = [
            (255, 0, 0, "Red"),      # Red
            (0, 255, 0, "Green"),    # Green  
            (0, 0, 255, "Blue"),     # Blue
            (255, 255, 255, "White"),# White
            (0, 0, 0, "Black"),      # Black
            (255, 255, 0, "Yellow"), # Yellow
            (0, 255, 255, "Cyan"),   # Cyan
            (255, 0, 255, "Magenta") # Magenta
        ]
        
        for r, g, b, name in colors:
            if not self.quiet:
                print(f"Testing {name}...")
            self.fill_color(r, g, b)
            time.sleep(1)
    
    def fill_color(self, r, g, b):
        """Fill entire screen with RGB color - for testing"""
        # Convert RGB to 16-bit color (RGB565)
        color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        color_high = color >> 8
        color_low = color & 0xFF
        
        self.print(f"Filling screen with RGB({r},{g},{b}) -> 0x{color:04X}")
        
        # Set window to full screen WITH OFFSET APPLIED
        self.set_window(0, 0, self.width - 1, self.height - 1)
        
        # Prepare and send pixel data
        pixels_per_chunk = 512
        total_pixels = self.width * self.height
        
        # Send pixel data in chunks
        sent_pixels = 0
        while sent_pixels < total_pixels:
            chunk_size = min(pixels_per_chunk, total_pixels - sent_pixels)
            chunk_data = []
            for _ in range(chunk_size):
                chunk_data.append(color_high)
                chunk_data.append(color_low)
            
            self.write_data(chunk_data)
            sent_pixels += chunk_size
        
        self.print(f"Sent {sent_pixels} pixels to display")
    
    def cleanup(self):
        """Clean up resources"""
        self.close_framebuffer()
        if self.spi:
            self.spi.close()

def main():
    """Main function"""
    quiet_mode = '--quiet' in sys.argv or '-q' in sys.argv
    test_mode = '--test' in sys.argv or '-t' in sys.argv
    
    display = ST7789(quiet=quiet_mode)
    
    try:
        if not quiet_mode:
            print("Starting ST7789 framebuffer renderer...")
            print(f"Display: {WIDTH}x{HEIGHT} with {OFFSET_Y}px top offset")
        
        if not display.init_display():
            if not quiet_mode:
                print("Failed to initialize display")
            return
        
        if not display.init_framebuffer():
            if not quiet_mode:
                print("Failed to initialize framebuffer")
            return
        
        if not quiet_mode:
            print("Display and framebuffer initialized successfully!")
        
        # Clear screen first
        display.fill_color(0, 0, 0)
        time.sleep(0.5)
        
        if test_mode:
            if not quiet_mode:
                print("Running color test...")
            display.test_colors()
            time.sleep(1)
            
            if not quiet_mode:
                print("Color test completed. Starting framebuffer rendering...")
        
        frame_count = 0
        start_time = time.time()
        
        # Use the optimized renderer
        while True:
            frame_count += 1
            display.render_framebuffer_fast()  # Try this first
            
            # Print FPS every 60 frames
            if not quiet_mode and frame_count % 60 == 0:
                elapsed = time.time() - start_time
                fps = 60 / elapsed
                print(f"Frame {frame_count}: {fps:.1f} FPS")
                start_time = time.time()
            
            # Small delay to prevent excessive CPU usage
            # Remove this line for maximum speed
            # time.sleep(0.001)
        
    except KeyboardInterrupt:
        if not quiet_mode:
            print("\nInterrupted by user")
    except Exception as e:
        if not quiet_mode:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    finally:
        display.cleanup()
        if not quiet_mode:
            print("Program exited")

if __name__ == "__main__":
    main()
