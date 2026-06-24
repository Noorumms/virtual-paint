import cv2
import numpy as np
import time

# ---- SETUP ----
frameWidth = 960
frameHeight = 540

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

# ---- COLORS TO DETECT (HSV) ----
myColors = [[5,107,0,19,255,255],      # orange
            [133,56,0,159,156,255],    # purple
            [5,76,0,100,255,255]]      # green

# ---- COLORS FOR DRAWING (BGR) ----
myColorValues = [[51,153,255],         # orange
                 [255,0,255],          # purple
                 [0,255,0]]            # green

# ---- STATE ----
myPoints = []
brushSize = 10
currentColor = myColorValues[0]
savedMsg = False
savedMsgTimer = 0
eraserMode = False


# ---- FIND TIP POSITION IN MASK ----
def getContours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w//2, y


# ---- DETECT COLORS AND GET TIP POINTS ----
def findColor(img, myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    count = 0
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        if x != 0 and y != 0:
            newPoints.append([x, y, count, brushSize, eraserMode])  # ✅ 5 values now
        count += 1
    return newPoints


# ---- DRAW ALL SAVED POINTS ----
def drawOnCanvas(imgResult, myPoints, myColorValues):
    for point in myPoints:
        if point[4] == True:                    # eraser point
            color = (0, 0, 0)                   # black
        else:
            color = myColorValues[point[2]]     # normal color
        cv2.circle(imgResult,
                   (point[0], point[1]),
                   point[3],
                   color,
                   cv2.FILLED)


# ---- SAVE DRAWING ----
def saveDrawing(imgResult):
    filename = f"drawing_{int(time.time())}.png"
    cv2.imwrite(filename, imgResult)
    print(f"Saved: {filename}")


# ---- DRAW HEADER BAR ----
def drawHeader(imgResult, brushSize, currentColor, savedMsg, eraserMode):
    cv2.rectangle(imgResult, (0,0), (frameWidth,60), (50,50,50), cv2.FILLED)

    if eraserMode:
        cv2.putText(imgResult, "ERASER",
                    (10,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,0,255), 2)
    else:
        cv2.putText(imgResult, f"Brush: {brushSize}",
                    (10,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255,255,255), 2)

    cv2.circle(imgResult, (300,30), 20, currentColor, cv2.FILLED)

    cv2.putText(imgResult, "      Z=Sm X=Md V=Lg C=Clear S=Save E=Erase Q=Quit",
                (330,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45, (200,200,200), 1)

    if savedMsg:
        cv2.putText(imgResult, "SAVED!",
                    (260,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,255,0), 2)


# ---- MAIN LOOP ----
while True:
    success, img = cap.read()

    if not success:
        print("Webcam not found")
        break

    imgResult = img.copy()

    newPoints = findColor(img, myColors)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
            currentColor = myColorValues[newP[2]]

    if len(myPoints) != 0:
        drawOnCanvas(imgResult, myPoints, myColorValues)

    if savedMsg:
        savedMsgTimer -= 1
        if savedMsgTimer <= 0:
            savedMsg = False

    drawHeader(imgResult, brushSize, currentColor, savedMsg, eraserMode)

    cv2.imshow("Virtual Paint", imgResult)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    if key == ord('c'):
        myPoints = []
    if key == ord('z'):
        brushSize = 5
    if key == ord('x'):
        brushSize = 15
    if key == ord('v'):
        brushSize = 25
    if key == ord('s'):
        saveDrawing(imgResult)
        savedMsg = True
        savedMsgTimer = 50
    if key == ord('e'):                        # ✅ toggle eraser
        eraserMode = not eraserMode            # True→False or False→True

cap.release()
cv2.destroyAllWindows()