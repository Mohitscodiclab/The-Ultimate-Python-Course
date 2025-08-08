# Twist Effect Printer

A Python script that creates an animated "twist effect" when printing text messages. Each alphabetic character cycles through the alphabet before settling on the correct letter, creating a fun "hacker-style" typing animation.

## Features
- Animated text printing with a twist effect
- Preserves spaces and non-alphabetic characters
- Customizable animation speed
- User-friendly input prompt
- No external dependencies

## How to Run

1. Save the code in a file named `twist_effect.py`
2. Run the file using Python:
   ```
   python twist_effect.py
   ```
3. Enter your desired message when prompted

## Example

When you run the program and enter "Hello World", the output will look like this (animated in your terminal):

```
h
ha
hb
hc
hd
he
hf
hg
hh
hi
hj
hk
hl
hm
hn
ho
hp
hq
hr
hs
ht
hu
hv
hw
hx
hy
hz
he
hel
hela
helb
helc
held
hele
helf
helg
helh
heli
helj
helk
hell
hellm
helln
hello
hello 
hello w
hello wa
hello wb
hello wc
hello wd
hello we
hello wf
hello wg
hello wh
hello wi
hello wj
hello wk
hello wl
hello wm
hello wn
hello wo
hello wp
hello wq
hello wr
hello ws
hello wt
hello wu
hello wv
hello ww
hello wx
hello wy
hello wz
hello wo
hello wor
hello wora
hello worb
hello worc
hello word
hello wore
hello worf
hello worg
hello worh
hello wori
hello worj
hello work
hello worl
hello worm
hello worn
hello woro
hello worp
hello worq
hello worr
hello wors
hello wort
hello woru
hello worv
hello worw
hello worx
hello wory
hello worz
hello worl
hello worl
hello world
```

## Customization Options

1. **Change animation speed**:
   Modify the `time.sleep(0.09)` value in the code:
   - Smaller value = faster animation
   - Larger value = slower animation

2. **Change the prompt message**:
   Edit this line:
   ```python
   user_message = input("Enter the message you want to display with the twist effect: ")
   ```

3. **Create a loop for multiple messages**:
   Replace the main section with:
   ```python
   if __name__ == "__main__":
       print("Welcome to the Twist Effect Printer!")
       while True:
           user_message = input("\nEnter your message (or 'quit' to exit): ")
           if user_message.lower() == 'quit':
               print("Goodbye!")
               break
           print_with_twist(user_message)
   ```

## Requirements
- Python 3.x
- No external libraries needed (uses only built-in modules: `time` and `string`)

## License
This project is open source and available under the MIT License.