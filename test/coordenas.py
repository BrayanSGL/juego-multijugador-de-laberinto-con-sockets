def convert_coodinate(x_maze, y_maze):
    x = x_maze * 50
    y = y_maze * 50
    return x, y

def convert_coodinate_reverse(x, y):
    x_maze = x / 50
    y_maze = y / 50
    return x_maze, y_maze

print(convert_coodinate(12, 12))