# TODO
- Neural Net IO
	- 4 outputs : x,y x,y
	- treat as vector => normalize => multiply by radius

	- Inputs: texture 32x32 (circle inscribed in square without circle) = 1024 + 2 points for me and enemy
	- 128 (packed) + 2 = 130

- Adapt Circle game
	- Adapt click: take in two points as input
	- Score: `self.points[self.move] += intersection_change`

- 'Fight'
	- Each one fights all of the other ones
	- Fitness: Define max number and subtract
