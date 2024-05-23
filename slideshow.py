import os, pygame

DELAY = 10000

PATH = "/home/pi/OneDrive"
fileList = os.listdir(PATH)

drivers = ["fbcon", "directfb", "svgalib", "xvfb", "Xvfb", "x11"]
found = False
for driver in drivers:
	if not os.getenv("SDL_VIDEODRIVER"):
		os.putenv("SDL_VIDEODRIVER", driver)
	try:
		pygame.display.init()
	except pygame.error:
		print("Driver failed!") #"Driver: {0} failed.".format(driver)
		continue
	found = True
	break

	if not found:
		raise Exception("No suitable video driver found!")

pygame.init()

displayInfo = pygame.display.Info()
display = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h), pygame.FULLSCREEN, pygame.NOFRAME)
clock = pygame.time.Clock()
running = True
pygame.mouse.set_visible(False)

images = []
for each in fileList:
	try:
		image = pygame.image.load(PATH + "/" + each)
		x, y = image.get_rect().size
		scale = float(displayInfo.current_w) / float(x)
		newX = int(x * scale)
		newY = int(y * scale)
		if x < y or newY > displayInfo.current_h:
			scale = float(displayInfo.current_h) / float(y)
			newX = int(x * scale)
			newY = int(y * scale)
		image = pygame.transform.smoothscale(image, (newX, newY))
		images.append(image)
	except:
		print("Invalid image!")
		continue

index = 0

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
			running = False
			pygame.quit()
			quit()
	display.fill((0, 0, 0))
	x, y = images[index].get_rect().size
	offsetX = (displayInfo.current_w / 2) - (x / 2)
	offsetY = (displayInfo.current_h / 2) - (y / 2)
	display.blit(images[index], (offsetX, offsetY))
	pygame.display.update()
	pygame.time.delay(DELAY)
	index = index + 1
	if (index >= len(images)):
		index = 0
	clock.tick(1)

pygame.quit()
quit()
