import pygame
import time
import os 

#http://www.karoltomala.com/blog/?p=679
drivers = ['directfb', 'fbcon', 'svgalib']

found = False
for driver in drivers:
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True
    break

if not found:
   raise Exception('No suitable video driver found!')

print os.getenv('SDL_VIDEODRIVER')

disp_no = os.getenv("DISPLAY")
if disp_no:
	print "I'm running under X display = {0}".format(disp_no)
 
#Pygame init
pygame.display.init()
pygame.mouse.set_visible(False)
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print "Framebuffer size: %d x %d" % (size[0], size[1])

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
print "Sono qui"
#pygame.display.flip()

os.system("dwebp sticker.webp -o sticker.png")
img=pygame.image.load("sticker.png") 
rect=img.get_rect().size

if rect[0]>64:
	w=64
	h1=rect[1]*w/rect[0]

if h1>128:
	h=128
	w=w*h/h1
else:
	h=h1
	
print rect
print w
print h

img = pygame.transform.scale(img,(w,h))
img = pygame.transform.rotate(img,90)

screen.blit(img,(0,0))
pygame.display.update()

time.sleep(2)
pygame.quit()
