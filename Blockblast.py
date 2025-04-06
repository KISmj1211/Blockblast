import tkinter, random

FONT = ("Malgun Gothic", 20, "bold")

key = ""
keyOff = False
idx = 0
tmr = 0
stage = 0
score = 0
barX = 0
barY = 540
ballX = 0
ballY = 0
ballXp = 0
ballYp = 0
isClear = True

block = []
for i in range(5):
    block.append([1] * 10)
for i in range(10):
    block.append([0] * 10)

def key_down(e):
    global key
    key = e.keysym

def key_up(e):
    global keyOff
    keyOff = True

def draw_block():
    global isClear
    isClear = True
    cnvs.delete("BG")
    for y in range(15):
        for x in range(10):
            gx = x * 80
            gy = y * 40
            if block[y][x] == 1:
                cnvs.create_rectangle(gx+1, gy+4, gx+79, gy+32, fill=block_color(x,y), width=0, tag="BG")
                isClear = False
    cnvs.create_text(200, 20, text=f"STAGE: {stage}", fill="white", font=FONT, tag="BG")
    cnvs.create_text(600, 20, text=f"SCORE: {score}", fill="white", font=FONT, tag="BG")

def block_color(x, y):
    col = "#{0:x}{1:x}{2:x}".format((15-x-int(y/3)), (x+1), (y*3+3))
    return col

def draw_bar():
    cnvs.delete("BAR")
    cnvs.create_rectangle(barX-80, barY-12, barX+80, barY+12, fill="silver", width=0, tag="BAR")
    cnvs.create_rectangle(barX-78, barY-14, barX+78, barY+14, fill="silver", width=0, tag="BAR")
    cnvs.create_rectangle(barX-78, barY-12, barX+78, barY+12, fill="white", width=0, tag="BAR")

def move_bar():
    global barX
    if key == "Left" and barX > 80: barX -= 40
    if key == "Right" and barX < 720: barX += 40

def draw_ball():
    cnvs.delete("BALL")
    cnvs.create_oval(ballX-20, ballY-20, ballX+20, ballY+20, fill="gold", outline="orange", width=2, tag="BALL")
    cnvs.create_oval(ballX-16, ballY-16, ballX+16, ballY+16, fill="yellow", width=0, tag="BALL")

def move_ball():
    global idx, tmr, score, ballX, ballY, ballXp, ballYp
    ballX += ballXp
    if ballX < 20:
        ballX = 20
        ballXp = -ballXp
    if ballX > 780:
        ballX = 780
        ballXp = -ballXp

    x = int(ballX / 80)
    y = int(ballY / 40)
    if block[y][x] == 1:
        block[y][x] = 0
        ballXp = -ballXp
        score += 10

    ballY += ballYp
    if ballY < 30:
        ballY = 30
        ballYp = -ballYp
    if ballY >= 600:
        idx = 2
        tmr = 0
        return

    x = int(ballX / 80)
    y = int(ballY / 40)
    if block[y][x] == 1:
        block[y][x] = 0
        ballYp = -ballYp
        score += 10

    if barY-40 <= ballY and ballY <= barY:
        if barX-80 <= ballX and ballX <= barX+80:
            ballYp = -10
            ballXp = random.choice([-5, 5])
            score += 1
        elif barX-100 <= ballX and ballX <= barX-80:
            ballYp = -10
            ballXp = random.randint(-20, -10)
            score += 2
        elif barX+80 <= ballX and ballX <= barX+100:
            ballYp = -10
            ballXp = random.randint(10, 20)
            score += 2

def main():
    global key, keyOff
    global idx, tmr, stage, score
    global barX, barY, ballX, ballY, ballXp, ballYp

    if idx == 0:
        tmr += 1
        if tmr == 1:
            stage = 1
            score = 0
        if tmr == 2:
            ballX = 100
            ballY = 240
            ballXp = 10
            ballYp = 10
            barX = 400
            draw_block()
            draw_ball()
            draw_bar()
            cnvs.create_text(400, 300, text="START", fill="white", font=FONT, tag="TXT")
        if tmr == 30:
            cnvs.delete("TXT")
            idx = 1

    elif idx == 1:
        move_ball()
        move_bar()
        draw_block()
        draw_ball()
        draw_bar()
        if isClear == True:
            idx = 3
            tmr = 0

    elif idx == 2:
        tmr += 1
        if tmr == 1:
            cnvs.create_text(400, 200, text="GAME OVER", fill="red", font=FONT, tag="TXT")
        if tmr == 15:
            cnvs.create_text(300, 340, text="[R] Try again", fill="cyan", font=FONT, tag="TXT")
            cnvs.create_text(500, 340, text="[N] New game", fill="magenta", font=FONT, tag="TXT")
        if key == 'r':
            cnvs.delete("TXT")
            idx = 0
            tmr = 1
        if key == 'n':
            cnvs.delete("TXT")
            for y in range(5):
                for x in range(10):
                    block[y][x] = 1
            idx = 0
            tmr = 0

    elif idx == 3:
        tmr += 1
        if tmr == 1:
            cnvs.create_text(400, 260, text="Clear stage!", fill="lime", font=FONT, tag="TXT")
        if tmr == 15:
            cnvs.create_text(400, 340, text="[SPACE] To the next", fill="yellow", font=FONT, tag="TXT")
        if key == "space":
            cnvs.delete("TXT")
            for y in range(5):
                for x in range(10):
                    block[y][x] = 1
            idx = 0
            tmr = 1
            stage += 1
        if keyOff == True:
            keyOff = False
            if key != '':
                key = ''

    wndw.after(52-(stage * 2), main)

wndw = tkinter.Tk()
wndw.title("블록 격파")
wndw.resizable(False, False)
wndw.bind("<Key>", key_down)
wndw.bind("<KeyRelease>", key_up)

cnvs = tkinter.Canvas(wndw, width=800, height=600, bg="black")
cnvs.pack(side="top")

main()
wndw.mainloop()