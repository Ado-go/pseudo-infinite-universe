import tkinter as tk
from random import randint

Width = 500
Height = 500
root = tk.Tk()
root.title("Universe")
canvas = tk.Canvas(width=Width, height=Height, bg="black")
canvas.pack()


def lehmer_random_number(new_seed):
    new_seed += 3777035285
    temp = new_seed * 1245296397
    m1 = temp >> 32 ^ temp
    temp = m1 * 318428617
    m2 = temp >> 32 ^ temp
    return m2


class Universe:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.randomness = randint(0, 900_000_000)
        self.up = 0
        self.left = 0
        self.moving = False

    def draw(self):
        canvas.delete("all")
        self.create_stars()
        self.draw_coordinates()

    def draw_coordinates(self):
        canvas.create_text(20 + len(str(self.x)) * 9, 20, text="X: {}".format(self.x), font=("Arial", 25), fill="white")
        canvas.create_text(20 + len(str(self.y)) * 9, 50, text="Y: {}".format(self.y), font=("Arial", 25), fill="white")

    def create_stars(self):
        col = -10
        for i in range(Width // 30):
            col += 30
            row = 0
            for j in range(Height // 30):
                row += 14
                random_number = lehmer_random_number(((i + self.x) & 16777215) << 64 | ((j + self.y) & 16777215)
                                                     + self.randomness)
                if random_number % 11 == 10:
                    size = random_number % 26
                    canvas.create_oval(i + col - size // 2 - 15,
                                       j + row * 2 - size // 2 - 10,
                                       i + size + col - size // 2 - 10,
                                       j + size + row * 2 - size // 2 - 5,
                                       fill=random_color(random_number))

    def movement(self, event):
        if event.keysym == "a":
            self.left = -1
        if event.keysym == "d":
            self.left = 1
        if event.keysym == "w":
            self.up = -1
        if event.keysym == "s":
            self.up = 1
        self.moving = True

    def space_travel(self):
        if self.moving:
            self.x += self.left
            self.y += self.up
            self.draw()
        canvas.after(10, self.space_travel)

    def stop_moving(self, event):
        if event.keysym == "w" or event.keysym == "s":
            self.up = 0
        if event.keysym == "a" or event.keysym == "d":
            self.left = 0
        if self.up == 0 and self.left == 0:
            self.moving = False

    def draw_solar_system(self, random_number):
        canvas.create_rectangle(0, Height // 2, Width, Height, outline="lightblue", fill="lightblue")
        canvas.create_oval(10, Height // 2 + Height // 4, 60, Height // 2 + Height // 4 + 50,
                           fill=random_color(random_number))

        canvas.create_text(45, Height // 2 + Height // 4 - 30, text="Star " + str(random_number % 999_999_999))

        number_of_planets = random_number % 10
        space = 0
        for i in range(number_of_planets):
            moon_space = 0
            number_of_moons = (random_number + i) % 4
            space += 35
            canvas.create_oval(65 + space, Height // 2 + Height // 4 + 10,
                               65 + space + 30, Height // 2 + Height // 4 + 40,
                               fill=random_color(random_number << i + 1))
            for j in range(number_of_moons):
                moon_space += 22
                canvas.create_oval(70 + space,
                                   Height // 2 + Height // 4 + 25 + moon_space,
                                   65 + space + 25,
                                   Height // 2 + Height // 4 + 45 + moon_space,
                                   fill=random_color(random_number << j + 1, True))

    def hover_over_planet(self, event):
        x = event.x // 30
        y = event.y // 30
        random_number = lehmer_random_number(((x + self.x) & 16_777_215) << 64 | ((y + self.y) & 16_777_215)
                                             + self.randomness)
        if random_number % 11 == 10:
            self.draw_solar_system(random_number)


def random_color(random_number, moon=False):
    color_palette = ["0", "1", "2", "3", "4", "5", "6", "7",
                     "8", "9", "a", "b", "c", "d", "e", "f"]
    color = "#"
    for i in range(6):
        new_random_number = lehmer_random_number(random_number + i + 100)
        if moon:
            x = color_palette[new_random_number % 16]
            y = color_palette[new_random_number % 16]
            color += x+y+x+y+x+y
            return color
        color += color_palette[new_random_number % 16]
    return color


universe = Universe()
universe.draw()

canvas.after(10, universe.space_travel)
canvas.bind("<Button-1>", lambda e: universe.hover_over_planet(e))
canvas.bind_all("<KeyRelease>", universe.stop_moving)
canvas.bind_all("<Key>", universe.movement)


canvas.mainloop()
