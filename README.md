# Pygame-Fractals
A python script that uses pygame to display interactive fractals.
There are 3 fractals on the script. They can be displayed on the colors gray, blue, pink.
You can walk and zoom on the fractals.

# Mandelbrot Set
![Mandelbrot Set](img/mandelbrot.png)

# Burning Ship
![Burning Ship](img/burning_ship.png)

# Other
![Other](img/other.png)


# Installation
The following modules are required:
- pygame
- numba

Just type:

    git clone https://github.com/mlchelCar/pygame-fractals.git
    cd pygame-fractals
    pip3 install -r requirements.txt

# Usage
python3 pygame-fractals.py fractal color

- fractal: mandelbrot/burning_ship/other
- color: gray/pink/blue

Keys
- Escape key:
  quit
- Up key:
  move up
- Down key:
  move down
- Left key:
  move left
- Right key:
  move right
- Shift key:
  zoom in
- Ctrl key:
  zoom out
- Space key:
  refresh
