import itertools as it

ROBOT = '@'
WALL = '#'
BOX = 'O'
EMPTY = '.'

LBOX = '['
RBOX = ']'

ALL_DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
ALL_INSTRUCTIONS = ['^', '>', 'v', '<']

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def direction_of(instruction):
    match (instruction):
        case '^': return UP
        case '>': return RIGHT
        case 'v': return DOWN
        case '<': return LEFT
    raise

def instruction_for(direction):
    return ALL_INSTRUCTIONS[ALL_DIRECTIONS.index(direction)]

def can_move_boxes(warehouse, box, direction):
    # there must exist an empty cell before we reach the wall
    di, dj = direction
    i, j = box
    while warehouse[i][j] != WALL:
        if warehouse[i][j] == EMPTY: return True
        i += di
        j += dj

    return False

def move_boxes(warehouse, instruction, robot):
    di, dj = ALL_DIRECTIONS[direction_of(instruction)]
    ri, rj = robot

    if not can_move_boxes(warehouse, (ri + di, rj + dj), (di, dj)):
        return (ri, rj)
    
    i, j = ri + di, rj + dj
    while warehouse[i][j] != EMPTY:
        i += di
        j += dj

    warehouse[i][j] = BOX
    warehouse[ri + di][rj + dj] = EMPTY

    return (ri + di, rj + dj)

def can_move_wide_box(warehouse, box, direction):
    i, j = box
    di, dj = direction

    if warehouse[i + di][j + dj] == EMPTY: return True
    if warehouse[i + di][j + dj] == WALL: return False
    if warehouse[i + di][j + dj] in [RBOX, LBOX]: return can_move_wide_boxes(warehouse, (i + di, j + dj), direction)
    raise

def can_move_wide_boxes(warehouse, box, direction):
    i, j = box
    bt = warehouse[i][j]

    if direction == ALL_DIRECTIONS[RIGHT]:
        if bt == RBOX: return can_move_wide_box(warehouse, box, direction)
        if bt == LBOX: return can_move_wide_box(warehouse, (i, j + 1), direction)
        raise

    if direction == ALL_DIRECTIONS[LEFT]:
        if bt == LBOX: return can_move_wide_box(warehouse, box, direction)
        if bt == RBOX: return can_move_wide_box(warehouse, (i, j - 1), direction)
        raise

    if warehouse[i][j] == LBOX:
        return can_move_wide_box(warehouse, box, direction) \
            and can_move_wide_box(warehouse, (i, j + 1), direction)

    if warehouse[i][j] == RBOX:
        return can_move_wide_box(warehouse, box, direction) \
            and can_move_wide_box(warehouse, (i, j - 1), direction)
    
    raise

def move_wide_box(warehouse, box, direction):
    i, j = box
    di, dj = direction
    this_cell = warehouse[i][j]
    next_cell = warehouse[i + di][j + dj]
    
    if next_cell == EMPTY:
        warehouse[i][j] = EMPTY
        warehouse[i + di][j + dj] = this_cell
        return

    if next_cell in [LBOX, RBOX]:
        move_wide_boxes(warehouse, instruction_for(direction), box, True)
        warehouse[i][j] = EMPTY
        warehouse[i + di][j + dj] = this_cell
        return
    
    raise

def move_wide_boxes(warehouse, instruction, robot, checked=False):
    di, dj = ALL_DIRECTIONS[direction_of(instruction)]
    ri, rj = robot

    if not checked and not can_move_wide_boxes(warehouse, (ri + di, rj + dj), (di, dj)):
        return (ri, rj)

    bt = warehouse[ri + di][rj + dj]

    move_wide_box(warehouse, (ri + di, rj + dj), (di, dj))
    if bt == LBOX and direction_of(instruction) == RIGHT: return (ri + di, rj + dj)
    if bt == RBOX and direction_of(instruction) == LEFT: return (ri + di, rj + dj)

    if bt == LBOX:
        move_wide_box(warehouse, (ri + di, rj + dj + 1), (di, dj))
    if bt == RBOX:
        move_wide_box(warehouse, (ri + di, rj + dj - 1), (di, dj))

    return (ri + di, rj + dj)


def run_instruction(warehouse, instruction, robot):
    di, dj = ALL_DIRECTIONS[direction_of(instruction)]
    ri, rj = robot
    next_cell = warehouse[ri + di][rj + dj]

    if next_cell == WALL: return (ri, rj)
    if next_cell == EMPTY: return (ri + di, rj + dj)    
    if next_cell == BOX: return move_boxes(warehouse, instruction, robot)
    if next_cell == LBOX or next_cell == RBOX: return move_wide_boxes(warehouse, instruction, robot)
    raise

def print_warehouse(warehouse, robot):
    ri, rj = robot
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if (i, j) == (ri, rj):
                print('@', end="")
            else:
                print(warehouse[i][j], end="")
        print()

def widen(car):
    if car == EMPTY: return EMPTY + EMPTY
    if car == WALL: return WALL + WALL
    if car == BOX: return LBOX + RBOX
    if car == ROBOT: return ROBOT + EMPTY

with open("input.txt") as file:
    warehouse, instructions = file.read().strip().split("\n\n")

    warehouse = [[c for c in line] for line in warehouse.split("\n")]
    wide_warehouse = [[c for c in ''.join([widen(c) for c in line])] for line in warehouse]

    instructions = [i for i in instructions if i != '\n']

    all_ij = list(it.product(range(len(warehouse)), range(len(warehouse[0]))))
    all_wide_ij = list(it.product(range(len(wide_warehouse)), range(len(wide_warehouse[0]))))

    robot = [(i, j) for i, j in all_ij if warehouse[i][j] == ROBOT][0]
    warehouse[robot[0]][robot[1]] = '.'

    wide_robot = [(i, j) for i, j in all_wide_ij if wide_warehouse[i][j] == ROBOT][0]
    wide_warehouse[wide_robot[0]][wide_robot[1]] = '.'

    for instruction in instructions:
        robot = run_instruction(warehouse, instruction, robot)

    print(sum([100 * i + j for i, j in all_ij if warehouse[i][j] == BOX]))

    for instruction in instructions:
        wide_robot = run_instruction(wide_warehouse, instruction, wide_robot)

    print(sum([100 * i + j for i, j in all_wide_ij if wide_warehouse[i][j] == LBOX]))

