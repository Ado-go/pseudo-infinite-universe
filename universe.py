import tkinter as tk

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
        self.up = 0
        self.left = 0
        self.moving = False

    def create_stars(self):
        canvas.delete("all")
        col = -10
        for i in range(Width // 30):
            col += 30
            row = 0
            for j in range(Height // 30):
                row += 14
                random_number = lehmer_random_number(((i + self.x) & 16777215) << 64 | ((j + self.y) & 16777215))
                if random_number % 11 == 10:
                    size = random_number % 26
                    canvas.create_oval(i + col - size // 2 - 15,
                                       j + row * 2 - size // 2 - 10,
                                       i + size + col - size // 2 - 10,
                                       j + size + row * 2 - size // 2 - 5,
                                       outline="white", fill=random_color(random_number))
                    canvas.create_text(110, 20, text="X: {} Y: {} ".format(self.x, self.y),
                                       font=("Arial", 25),
                                       fill="white")

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
            self.create_stars()
        canvas.after(10, self.space_travel)

    def stop_moving(self, event):
        if event.keysym == "w" or event.keysym == "s":
            self.up = 0
        if event.keysym == "a" or event.keysym == "d":
            self.left = 0
        if self.up == 0 and self.left == 0:
            self.moving = False

    def hover_over_planet(self, event):
        x = event.x // 30
        y = event.y // 30
        random_number = lehmer_random_number(((x + self.x) & 16777215) << 64 | ((y + self.y) & 16777215))
        if random_number % 11 == 10:
            canvas.create_rectangle(0, Height//2, Width, Height,
                                    outline="lightblue", fill="lightblue")
            canvas.create_oval(10, Height // 2 + Height // 4,
                               60, Height // 2 + Height // 4 + 50,
                               fill=random_color(random_number))
            num = random_number % 999999999
            canvas.create_text(45, Height // 2 + Height // 4 - 30,
                               text="Star " + str(num))
            number_of_planets = random_number % 10
            space = 0
            for i in range(number_of_planets):
                moon_space = 0
                number_of_moons = (random_number + i) % 4
                space += 35
                canvas.create_oval(65 + space, Height // 2 + Height // 4 + 10,
                                   65 + space + 30, Height // 2 + Height // 4 + 40,
                                   fill=random_color(random_number << i))
                for j in range(number_of_moons):
                    moon_space += 22
                    canvas.create_oval(70 + space,
                                       Height // 2 + Height // 4 + 25 + moon_space,
                                       65 + space + 25,
                                       Height // 2 + Height // 4 + 45 + moon_space,
                                       fill=random_color(random_number, True))


def random_color(random_number, moon=False):
    color_palette = ["0", "1", "2", "3", "4", "5", "6", "7",
                     "8", "9", "a", "b", "c", "d", "e", "f"]
    color = "#"
    for i in range(6):
        if moon:
            x = color_palette[random_number % 16]
            y = color_palette[(random_number + 5) % 16]
            color += x+y+x+y+x+y
            return color
        color += color_palette[(random_number ^ i) % 16]
    return color


universe = Universe()
universe.create_stars()

canvas.after(10, universe.space_travel)
canvas.bind("<Button-1>", lambda e: universe.hover_over_planet(e))
canvas.bind_all("<KeyRelease>", universe.stop_moving)
canvas.bind_all("<Key>", universe.movement)


canvas.mainloop()
