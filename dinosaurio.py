import random
import tkinter as tk


WIDTH = 800
HEIGHT = 300
GROUND_Y = 245


class DinosaurGame:
	def __init__(self, root):
		self.root = root
		self.root.title("Dinosaurio del desierto")
		self.root.resizable(False, False)

		self.canvas = tk.Canvas(
			root, width=WIDTH, height=HEIGHT, bg="#f7f7f7", highlightthickness=0
		)
		self.canvas.pack()
		self.canvas.bind("<space>", self.handle_key)
		self.canvas.bind("<Up>", self.handle_key)
		self.canvas.bind("<Key-r>", self.restart)
		self.canvas.focus_set()

		self.score = 0
		self.speed = 7
		self.dino_y = GROUND_Y - 44
		self.dino_velocity = 0
		self.obstacles = []
		self.clouds = [(170, 55), (510, 85), (710, 42)]
		self.running = False
		self.game_over = False
		self.draw()

	def handle_key(self, _event=None):
		if self.game_over:
			self.restart()
		elif not self.running:
			self.running = True
			self.jump()
		else:
			self.jump()

	def jump(self):
		if self.dino_y >= GROUND_Y - 44:
			self.dino_velocity = -14

	def restart(self, _event=None):
		self.score = 0
		self.speed = 7
		self.dino_y = GROUND_Y - 44
		self.dino_velocity = 0
		self.obstacles.clear()
		self.running = True
		self.game_over = False

	def update(self):
		if self.running and not self.game_over:
			self.score += 1
			self.speed = 7 + self.score // 500
			self.dino_y += self.dino_velocity
			self.dino_velocity += 0.7
			if self.dino_y > GROUND_Y - 44:
				self.dino_y = GROUND_Y - 44
				self.dino_velocity = 0

			if not self.obstacles or self.obstacles[-1][0] < WIDTH - random.randint(260, 430):
				height = random.choice((30, 42, 52))
				self.obstacles.append([WIDTH, height])

			for obstacle in self.obstacles:
				obstacle[0] -= self.speed
				if self.collides(obstacle):
					self.game_over = True

			self.obstacles = [item for item in self.obstacles if item[0] > -30]

		self.draw()
		self.root.after(20, self.update)

	def collides(self, obstacle):
		x, height = obstacle
		dino_box = (75, self.dino_y + 4, 115, self.dino_y + 43)
		cactus_box = (x + 4, GROUND_Y - height + 4, x + 25, GROUND_Y)
		return (
			dino_box[0] < cactus_box[2]
			and dino_box[2] > cactus_box[0]
			and dino_box[1] < cactus_box[3]
			and dino_box[3] > cactus_box[1]
		)

	def draw_dinosaur(self):
		x, y = 75, self.dino_y
		color = "#535353"
		self.canvas.create_rectangle(x + 8, y + 12, x + 34, y + 38, fill=color, outline=color)
		self.canvas.create_rectangle(x + 25, y, x + 48, y + 19, fill=color, outline=color)
		self.canvas.create_rectangle(x + 40, y + 12, x + 55, y + 18, fill=color, outline=color)
		self.canvas.create_rectangle(x + 30, y + 5, x + 33, y + 8, fill="#f7f7f7", outline="")
		self.canvas.create_rectangle(x, y + 20, x + 12, y + 25, fill=color, outline=color)
		leg_y = y + 36
		if self.running and not self.game_over and self.dino_y >= GROUND_Y - 44:
			leg_offset = (self.score // 5) % 2 * 5
		else:
			leg_offset = 0
		self.canvas.create_rectangle(x + 13, leg_y, x + 19, leg_y + 8 - leg_offset, fill=color, outline=color)
		self.canvas.create_rectangle(x + 29, leg_y, x + 35, leg_y + 8 + leg_offset, fill=color, outline=color)

	def draw(self):
		self.canvas.delete("all")
		for cloud_x, cloud_y in self.clouds:
			self.canvas.create_oval(cloud_x, cloud_y, cloud_x + 38, cloud_y + 12, fill="#dedede", outline="")
			self.canvas.create_oval(cloud_x + 12, cloud_y - 7, cloud_x + 31, cloud_y + 12, fill="#dedede", outline="")

		self.canvas.create_line(0, GROUND_Y, WIDTH, GROUND_Y, fill="#777777", width=2)
		self.draw_dinosaur()

		for x, height in self.obstacles:
			self.canvas.create_rectangle(x + 9, GROUND_Y - height, x + 21, GROUND_Y, fill="#535353", outline="")
			self.canvas.create_rectangle(x, GROUND_Y - height + 11, x + 11, GROUND_Y - height + 19, fill="#535353", outline="")

		self.canvas.create_text(WIDTH - 25, 25, text=f"PUNTOS: {self.score // 5:04}", anchor="e", fill="#535353", font=("Courier", 14, "bold"))
		if not self.running and not self.game_over:
			self.canvas.create_text(WIDTH // 2, 130, text="Pulsa ESPACIO para empezar", fill="#535353", font=("Arial", 16))
		elif self.game_over:
			self.canvas.create_text(WIDTH // 2, 125, text="¡FIN DEL JUEGO!", fill="#535353", font=("Arial", 22, "bold"))
			self.canvas.create_text(WIDTH // 2, 157, text="Pulsa ESPACIO o R para volver a jugar", fill="#535353", font=("Arial", 13))


if __name__ == "__main__":
	window = tk.Tk()
	game = DinosaurGame(window)
	game.update()
	window.mainloop()
