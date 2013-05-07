import curses
import time
import random

screen = curses.initscr()
dims = screen.getmaxyx()
curses.curs_set(0)
curses.noecho()
screen.nodelay(1)
screen.border()

char = 'X'
deadChar = ' '

class Cell(object):
	def __init__(self):
		self.alive = bool(random.randrange(0, 100) < 20)

	def __repr__(self):
		return self.alice

def is_cell_alive(y, x, cells):
	""" Check if the cell is currently displaied as alive """
	if y >= len(cells):
		y = 0
	if x >= len(cells[0]):
		x = 0
	if y < 0:
		y = len(cells)-1
	if x < 0:
		x = len(cells[0])-1
	return (screen.inch(y, x) == ord(char))

def cell_neighbour_count(y, x, cells):
	""" Count the number of alive neighbours """
	count = 0
	if is_cell_alive(y-1, x-1, cells): 
		count += 1
	if is_cell_alive(y, x-1, cells): 
		count += 1
	if is_cell_alive(y+1, x-1, cells): 
		count += 1
	if is_cell_alive(y-1, x, cells): 
		count += 1
	if is_cell_alive(y+1, x, cells): 
		count += 1
	if is_cell_alive(y-1, x+1, cells): 
		count += 1
	if is_cell_alive(y, x+1, cells): 
		count += 1
	if is_cell_alive(y+ 1, x+1, cells): 
		count += 1
	return count

def should_cell_live(y, x, cells):
	""" Check if the cell should be alive for next rendering """
	neighbours = cell_neighbour_count(y, x, cells)
	if screen.inch(y, x) == ord(char):
		if neighbours == 2 or neighbours == 3:
			return True
		else:
			return False
	elif(neighbours == 3):
		return True
	else:
		return False

def update_cell_statuses(cells):
	""" Update the status of the cells for the next rendering """
	for y in range(0, len(cells)):
		for x in range(0, len(cells[0])):
			cells[y][x].alive = should_cell_live(y, x, cells)

def render_board(cells):
	""" Render all alive cells to the board and remove the dead """
	for y in range(1, len(cells)):
		for x in range(1, len(cells[0])):
			if cells[y][x].alive:
				screen.addch(y, x, char)
			else:
				screen.addch(y, x, deadChar)

def create_cells():
	""" Create a random pattern of living cells """
	cells = []
	for i in range(0, dims[0]-1):
		tempList = []
		for n in range(0, dims[1]-2):
			tempList.append(Cell())
		cells.append(tempList)
	return cells

def create_stress_test():
	""" A stress test with a heavy pattern, a staraight line full with living cells """
	cells = []
	for i in range(0, dims[0]-1):
		tempList = []
		for n in range(0, dims[1]-2):
			tempCell = Cell()
			tempCell.alive = bool(i == 20)
			tempList.append(tempCell)
		cells.append(tempList)
	return cells	

def game():
	""" Start a game of life """
	cells = create_cells()

	# Create a stress test with a heavy starting pattern
	# cells = create_stress_test()
	
	render_board(cells)
	q = -1
	screen.refresh()
	while q != ord('q'):
		q = screen.getch()
		if q == ord('p'):
			time.sleep(5)
		elif q == ord('r'):
			break
		update_cell_statuses(cells)
		render_board(cells)
		screen.refresh()
		time.sleep(0.05)
	else:
		curses.endwin()
		exit()

	game()


game()
curses.endwin()
