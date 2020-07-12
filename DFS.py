SHIFT_FOR_NEIGHBOURS = [-1, 0, 1]


class Labyrinth:
    def __init__(self):
        self.rows_count = -1
        self.columns_count = -1
        self.labyrinth = []
        self.start_position = tuple()
        self.end_position = tuple()
        self.come_from = {}

    def read_field(self):
        with open('in.txt') as input_file:
            self.rows_count = int(input_file.readline())
            self.columns_count = int(input_file.readline())
            for row in range(self.rows_count):
                self.labyrinth.append([])
                line = input_file.readline().split()
                for element in line:
                    self.labyrinth[row].append(int(element))

            self.start_position = read_position(input_file)
            self.end_position = read_position(input_file)

    def get_cell_condition(self, x, y):
        return self.labyrinth[x][y]

    def find_way(self):
        if (self.get_cell_condition(*self.end_position) == 1 or
                self.get_cell_condition(*self.start_position) == 1):
            return False

        queue = []
        visited_cells = []
        queue.append(self.start_position)
        while len(queue) != 0:
            position = queue.pop()
            if position == self.end_position:
                return True

            visited_cells.append(position)
            self.check_neighbours(position, visited_cells, queue)

        return False

    def check_neighbours(self, position, visited_cells, queue):
        for dx in SHIFT_FOR_NEIGHBOURS:
            for dy in SHIFT_FOR_NEIGHBOURS:
                if abs(dx) == abs(dy):
                    continue

                if (position[0] + dx < 0 or position[1] + dy < 0 or
                        position[0] + dx >= self.rows_count or
                        position[1] + dy >= self.columns_count):
                    continue

                if (self.get_cell_condition(position[0] + dx,
                                            position[1] + dy) == 1
                        or (position[0] + dx, position[1] + dy) in visited_cells):
                    continue

                queue.append((position[0] + dx, position[1] + dy))
                self.come_from[(position[0] + dx, position[1] + dy)] = position

    def get_path(self):
        with open('out.txt', 'w') as output_file:
            if self.find_way():
                restore_path = []
                position = self.end_position
                while position != self.start_position:
                    restore_path.append((position[0] + 1, position[1] + 1))
                    position = self.come_from[position]

                restore_path.append((position[0] + 1, position[1] + 1))
                restore_path.reverse()
                output_file.write('Y\n')
                for position in restore_path:
                    output_file.write(f'{position[0]} {position[1]}\n')

            else:
                output_file.write('N')


def read_position(file):
    temp_array = []
    line = file.readline().split()
    for element in line:
        temp_array.append(int(element) - 1)
    return tuple(temp_array)


def main():
    labyrinth = Labyrinth()
    labyrinth.read_field()
    labyrinth.get_path()
    print('Complete')


if __name__ == '__main__':
    main()
