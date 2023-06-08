from tkinter import *
class gameModel:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid_model = [[0] * width for _ in range(height)]
        self.next_grid_model = [[1] * width for _ in range(height)]

        self.glider_pattern = [[0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0],
                  [0, 0, 0, 1, 0],
                  [0, 1, 1, 1, 0],
                  [0, 0, 0, 0, 0]]

        self.glider_gun_pattern = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
              [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    def randomize(self):
        import random
        for i in range(self.height):
            for j in range(self.width):
                self.grid_model[i][j] = random.randint(0, 1)

    def next_gen(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = 0
                count = self.count_live_neighbors(i, j)

                if self.grid_model[i][j] == 0:
                    if count == 3:
                        cell = 1
                elif self.grid_model[i][j] == 1:
                    if count == 2 or count == 3:
                        cell = 1
                self.next_grid_model[i][j] = cell

        temp = self.grid_model
        self.grid_model = self.next_grid_model
        self.next_grid_model = temp

    def count_live_neighbors(self, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_row = (row + i + self.height) % self.height
                neighbor_col = (col + j + self.width) % self.width
                count += self.grid_model[neighbor_row][neighbor_col]
        count -= self.grid_model[row][col]
        return count
    
    def load_pattern(self, pattern, x_offset=0, y_offset=0):
        for i in range(self.height):
            for j in range(self.width):
                self.grid_model[i][j] = 0

        j = y_offset

        for row in pattern:
            i = x_offset
            for value in row:
                self.grid_model[i][j] = value
                i += 1
            j += 1

class view:
    def __init__(self, game):
        self.cell_size = 5
        self.is_running = False
        self.root = None
        self.grid_view = None
        self.start_button = None
        self.clear_button = None
        self.choice = None
        self.model = game

    def setup(self):
        self.root = Tk()
        self.root.title('The Game of Life')

        self.grid_view = Canvas(
            self.root,
            width=self.model.width * self.cell_size,
            height=self.model.height * self.cell_size,
            borderwidth=0,
            highlightthickness=0,
            bg='white'
        )

        self.start_button = Button(self.root, text='Start', width=12)
        self.clear_button = Button(self.root, text='Clear', width=12)

        self.choice = StringVar(self.root)
        self.choice.set('Choose a Pattern')
        option = OptionMenu(
            self.root,
            self.choice,
            'Choose a Pattern',
            'glider',
            'glider gun',
            'random',
            command=self.option_handler
        )
        option.config(width=20)

        self.grid_view.grid(row=0, columnspan=3, padx=20, pady=20)
        self.grid_view.bind('<Button-1>', self.grid_handler)
        self.start_button.grid(row=1, column=0, sticky=W, padx=20, pady=20)
        self.start_button.bind('<Button-1>', self.start_handler)
        option.grid(row=1, column=1, padx=20)
        self.clear_button.grid(row=1, column=2, sticky=E, padx=20, pady=20)
        self.clear_button.bind('<Button-1>', self.clear_handler)

    def option_handler(self, event):
        self.is_running = False
        self.start_button.configure(text='Start')

        selection = self.choice.get()

        if selection == 'glider':
            self.load_pattern(self.model.glider_pattern, 10, 10)
        elif selection == 'glider gun':
            self.load_pattern(self.model.glider_gun_pattern, 10, 10)
        elif selection == 'random':
            self.randomize()

        self.update()

    def start_handler(self, event):
        if self.is_running:
            self.is_running = False
            self.start_button.configure(text='Start')
        else:
            self.is_running = True
            self.start_button.configure(text='Pause')
            self.update()

    def clear_handler(self, event):
        self.is_running = False
        for i in range(self.height):
            for j in range(self.width):
                self.model.grid_model[i][j] = 0

        self.start_button.configure(text='Start')
        self.update()
    
    def grid_handler(self, event):
        x = int(event.x / self.cell_size)
        y = int(event.y / self.cell_size)

        if self.model.grid_model[y][x] == 1:
            self.model.grid_model[y][x] = 0
            self.draw_cell(x, y, 'white')
        else:
            self.model.grid_model[y][x] = 1
            self.draw_cell(x, y, 'black')
    
    def update(self):
        self.grid_view.delete(ALL)

        self.model.next_gen()
        for i in range(self.model.height):
            for j in range(self.model.width):
                if self.model.grid_model[i][j] == 1:
                    self.draw_cell(j, i, 'black')

        if self.is_running:
            self.root.after(100, self.update)

    def draw_cell(self, x, y, color):
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.grid_view.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

    def load_pattern(self, pattern, start_x, start_y):
        self.model.load_pattern(pattern, start_x, start_y)

    def randomize(self):
        self.model.randomize()

    def next_gen(self):
        self.model.next_gen()

    def count_live_neighbors(self, row, col):
        self.count_live_neighbors(row,col)
    
    def run(self):

        self.setup()
        self.update()
        self.root.mainloop()

if __name__ == '__main__':
    game = gameModel(height=100, width=100)
    mod = view(game)
    mod.run()