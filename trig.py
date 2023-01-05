import tkinter as tk
import math


WIDTH = 1200
HEIGHT = 700
ORIGIN_X = WIDTH / 2
ORIGIN_Y = HEIGHT / 2

SCALE = 60



class Point:
	def __init__(self, x, y):
		self.setX(x)
		self.setY(y)


	def setX(self, x):
		self.x = x
		self.x_shift = x - ORIGIN_X
		self.x_scaled = self.x_shift / SCALE


	def setY(self, y):
		self.y = y
		self.y_shift = y - ORIGIN_Y
		self.y_scaled = -self.y_shift / SCALE



class Trig:

	def __init__(self, master):
		self.master = master
		self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT)
		self.canvas.pack()
		self.canvas.bind("<Motion>", self.move_mouse)

		self.origin = Point(ORIGIN_X, ORIGIN_Y)
		self.mouse = Point(ORIGIN_X, ORIGIN_Y)
		self.angle = 0
		self.dist = 0

		self.draw()
	
	

	def move_mouse(self, event):
		self.mouse.setX(event.x)
		self.mouse.setY(event.y)

		self.draw()



	def distance(self, point1, point2):
		x1, y1 = point1.x_scaled, point1.y_scaled
		x2, y2 = point2.x_scaled, point2.y_scaled

		dx = x1 - x2
		dy = y1 - y2

		dx_quadrado = dx ** 2
		dy_quadrado = dy ** 2

		distance = math.sqrt(dx_quadrado + dy_quadrado)

		return distance



	def draw_referential(self):
		center_top = Point(ORIGIN_X, 0)
		center_bottom = Point(ORIGIN_X, HEIGHT)

		center_left = Point(0, ORIGIN_Y)
		center_right = Point(WIDTH, ORIGIN_Y)


		self.canvas.create_line(center_top.x, center_top.y, center_bottom.x, center_bottom.y)
		self.canvas.create_line(center_left.x, center_left.y, center_right.x, center_right.y)

		half_scaled_width = (WIDTH // SCALE) // 2
		half_scaled_height = (HEIGHT // SCALE) // 2

		for x in range(-half_scaled_width + 1, half_scaled_width):
			self.canvas.create_text((half_scaled_width + x) * SCALE, ORIGIN_Y + 10, text=str(x))

		for y in range(-half_scaled_height, half_scaled_height + 1):
			if y != 0:
				self.canvas.create_text(ORIGIN_X - 15, (half_scaled_height - y + 0.80) * SCALE, text=str(y))



	def draw_unit_arc(self):
		coords = ORIGIN_X + SCALE, ORIGIN_Y + SCALE, ORIGIN_X - SCALE, ORIGIN_Y - SCALE

		angle = math.atan2(self.mouse.y_shift, self.mouse.x_shift)
		angle = -angle * 180 / math.pi
		
		if angle < 0:
			angle += 360

		self.angle = angle

		arc = self.canvas.create_arc(coords, start=0, extent=angle)
		self.canvas.create_text(self.origin.x + 25, self.origin.y - 30, text=f"{angle:.2f}º")



	def draw_arc_xs(self):
		coords = ORIGIN_X + SCALE * 2, ORIGIN_Y + SCALE * 2, ORIGIN_X - SCALE * 2, ORIGIN_Y - SCALE * 2

		start = 0
		angle = math.atan2(self.mouse.y_shift, self.mouse.x_shift)
		angle = -angle * 180 / math.pi

		xOffset = 60
		yOffset = -60

		if self.mouse.x < self.origin.x:
			xOffset *= -1

			if angle > 0:
				start = angle
				angle = 180 - angle

			else:
				start = 180
				angle = 180 + angle


		if self.mouse.y > self.origin.y:
			yOffset *= -1

			if self.mouse.x > self.origin.x:
				start = angle + 360
				angle = -angle



		arc = self.canvas.create_arc(coords, start=start, extent=angle, outline='red')
		self.canvas.create_text(self.origin.x + xOffset, self.origin.y + yOffset, text=f"{angle:.2f}º", fill='red')



	def draw_line_from_origin(self):
		x1, y1 = self.origin.x, self.origin.y
		x2, y2 = self.mouse.x, self.mouse.y

		distance = self.distance(self.origin, self.mouse)
		self.dist = distance

		yOffset = -40

		if y1 < y2:
			yOffset *= -1


		self.canvas.create_line(x1, y1, x2, y2, width=3)
		self.canvas.create_oval(x2-5, y2-5, x2+5, y2+5, fill="orange")
		self.canvas.create_text(x2, y2 + yOffset - 20, text=f"({self.mouse.x_scaled:.2f}, {self.mouse.y_scaled:.2f})")
		self.canvas.create_text(x2, y2 + yOffset, text=f"√(x² + y²) = {distance:.2f}")



	def draw_triangle_vert(self):
		x1, y1 = self.mouse.x, self.origin.y
		x2, y2 = self.mouse.x, self.mouse.y

		a = 15
		b = -15

		if x2 > self.origin.x:
			a *= -1

		
		if y2 > self.origin.y:
			b *= -1


		seno = math.sin(self.angle * math.pi / 180)


		textX = x2 - a * 6
		textY = y1 - (y1 - y2) / 2


		self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=3)
		self.canvas.create_line(x1, y1 + b, x1 + a, y1 + b, x1 + a, y1)
		self.canvas.create_text(textX, textY, text=f"sin({self.angle:.2f}º) = {seno:.2f}", fill='blue')
		self.canvas.create_text(textX, textY + 20, text=f"√(x² + y²) * sin({self.angle:.2f}º) ⟺", fill='blue')
		self.canvas.create_text(textX, textY + 40, text=f"⟺ {self.dist:.2f} * {seno:.2f} = {self.dist * seno:.2f}", fill='blue')



	def draw_triangle_hori(self):
		x1, y1 = self.origin.x, self.origin.y
		x2, y2 = self.mouse.x, self.origin.y

		flip = 1

		if self.mouse.y > self.origin.y:
			flip *= -1


		cosseno = math.cos(self.angle * math.pi / 180)

		textX = x1 - (x1 - x2) / 2
		textY = y2 + flip * 80 - 20


		self.canvas.create_line(x1, y1, x2, y2, fill='green', width=3)
		self.canvas.create_text(textX, textY, text=f"cos({self.angle:.2f}º) = {cosseno:.2f}", fill='green')
		self.canvas.create_text(textX, textY + 20, text=f"√(x² + y²) * cos({self.angle:.2f}º) ⟺", fill='green')
		self.canvas.create_text(textX, textY + 40, text=f"⟺ {self.dist:.2f} * {cosseno:.2f} = {self.dist * cosseno:.2f}", fill='green')



	def draw_tangent(self):
		lineX = ORIGIN_X + SCALE
		tan_line_top = Point(lineX, 0)
		tan_line_bottom = Point(lineX, HEIGHT)

		tangente = math.tan(self.angle * math.pi / 180)
		seno = math.sin(self.angle * math.pi / 180)
		cosseno = math.cos(self.angle * math.pi / 180)

		x1, y1 = self.origin.x, self.origin.y
		x2, y2 = lineX, self.origin.y - (tangente * SCALE)


		self.canvas.create_line(x1, y1, x2, y2, width=1, fill='red')
		self.canvas.create_line(tan_line_top.x, tan_line_top.y, tan_line_bottom.x, tan_line_bottom.y, dash=[2, 8])
		self.canvas.create_oval(x2-3, y2-3, x2+3, y2+3, fill="red")
		self.canvas.create_text(x2 + 140, y2, text=f"tan({self.angle:.2f}º) = {tangente:.2f}", fill='red')
		self.canvas.create_text(x2 + 140, y2 + 20, text=f"sin/cos ⟺ {seno:.2f}/{cosseno:.2f} = {seno/cosseno:.2f}", fill='red')



	def draw(self):
		self.canvas.delete("all")

		self.draw_unit_arc()
		self.draw_arc_xs()
		self.draw_referential()
		self.draw_line_from_origin()
		self.draw_triangle_vert()
		self.draw_triangle_hori()
		self.draw_tangent()



def main():
	root = tk.Tk()
	root.title('Triângulos & Trigonometria')
	app = Trig(root)
	root.mainloop()



if __name__ == "__main__":
	main()
