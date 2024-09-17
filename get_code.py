import keyboard

def on_key_press(event):
    print(f"Keycode: {event.scan_code}")

keyboard.on_press(on_key_press)

keyboard.wait('esc')  # Wait for the 'esc' key to be pressed