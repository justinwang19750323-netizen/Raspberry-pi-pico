from machine import Timer,Pin

def callback1000(n):    
    led = Pin("LED",mode=Pin.OUT)
    if led.value() == 0:
        led.on()
    else:
        led.off()
    
       
    
def main():
    timer = Timer(period=1000, callback=callback1000)
    
if __name__ == "__main__":
    main()