import cv2
import numpy as np

point_count = 0
point_coords = []
ix,iy = 0,0
drag = False
user_input = "Image"

# to update x and y coordinates of selected region
def updatepoints(x, y):
    global point_coords, ix, iy
    if ix - x <= 0:                                                                     # dragged to the right
        point_coords = [(i + int(abs(ix - x)), j) for i,j in point_coords]
    elif ix - x > 0:                                                                    # dragged to the left
        point_coords = [(i - int(abs(ix - x)), j) for i,j in point_coords]
    if iy - y <= 0:                                                                     # dragged to the bottom
        point_coords = [(i, j + int(abs(iy - y))) for i,j in point_coords]
    elif iy - y > 0:                                                                    # dragged to the top
        point_coords = [(i, j - int(abs(iy - y))) for i,j in point_coords]
    ix,iy = x,y

# to drag selected region
def movepoint(event, x, y, flags, param):
    global drag, img, point_coords, ix, iy

    np_point_coords = np.array(point_coords, np.int32) 
    np_point_coords = np_point_coords.reshape((-1,1,2))

    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x,y
        cv2.polylines(img, [np_point_coords], True, (255,255,255))
        if cv2.pointPolygonTest(np_point_coords, (x,y), False) > 0:     #if cursor is within the marked region
            drag = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drag: 
            cv2.imshow('image', img)
            
            '''for i in range(len(point_coords)):
                cv2.circle(img, (point_coords[i][0]+int(x-w),point_coords[i][1]+int(y-h)), 2, (255,255,0), -1)'''
                
            updatepoints(x,y)
            np_point_coords = np.array(point_coords, np.int32)
            cv2.polylines(img, [np_point_coords], True, (255,255,255))

    elif event == cv2.EVENT_LBUTTONUP:
        drag = False
        img = cv2.imread('cat.jpg')
        cv2.polylines(img, [np_point_coords], True, (255,255,255))
        cv2.imshow('image', img)
        
        '''print(point_coords)
        print(f"Ix-x= {ix-x}, Iy-y={iy-y}")
        print(f"Ix = {ix}, Iy = {iy}")
        print(f"x = {x}, y = {y}")
        print(point_coords)'''

        ix,iy = 0,0
        

    elif event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.destroyWindow('ROI')
        ROIView(np_point_coords)

# to reset the image back to the original image
def reset_image():
    global img
    img = np.copy(img)

# to draw the image
def draw_image():
    cv2.imshow('image',img)
    np_point_coords = np.array(point_coords, np.int32) #excluding last input
    np_point_coords = np_point_coords.reshape((-1,1,2))
    cv2.polylines(img, [np_point_coords], True, (255,255,255))
    return np_point_coords

# to save coordinates of an image
def dispCoords():
    open('ROICoordinates.txt', 'w').close()
    file = open("ROICoordinates.txt", "a")
    file.write("Point_no, X, Y\n")
    for i in range(len(point_coords)):
        file.write(f"{i}, {point_coords[i][0]}, {point_coords[i][1]}\n")

# to open a new window for the specified ROI
def ROIView(point_coords):
    cv2.namedWindow('ROI')
    cv2.moveWindow('ROI', 1000,1000)
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [point_coords], color=(255,255,255))
    ROIimg = cv2.bitwise_and(img, mask)
    cv2.imshow('ROI', ROIimg)

    if user_input == "Image":
        cv2.setMouseCallback('image', lambda *args : None) #stopping any further input
        cv2.setMouseCallback('image', movepoint)
    else:
        np_point_coords = draw_image()
        cv2.polylines(img, [np_point_coords], True, (255,255,255))
        cv2.setMouseCallback('image', movepoint)

    dispCoords()

# mouse callback function
def plotpoints(event,x,y,flags,param):
    global point_coords, point_count

    #if lbutton is held down
    if event == cv2.EVENT_LBUTTONDOWN:
        point_count+=1
        point_coords.append((x,y))
        cv2.circle(img, (x,y), 2, (255,255,255), -1)

        #connect lines if more than one point
        if point_count > 1:
            for i in range (len(point_coords)-1):
                cv2.line(img, point_coords[i], point_coords[i+1], (255,255,255), 2)

        #fill in last line if point returns back to original point
        if point_count > 2:
            dist = (((x - point_coords[0][0]) ** 2) + ((y - point_coords[0][1]) ** 2))**0.5

            if dist < 10:
                reset_image()
                del point_coords[-1]
                np_point_coords = draw_image()
                ROIView(np_point_coords)


choice = int(input("Enter 1 to plot points on image or 2 to enter coordinates manually\n"))
if(choice == 1):
    img = cv2.imread("cat.jpg")
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', plotpoints)   
else:
    user_input = "Manual"
    print("Enter your coordinates")
    flag = ""
    while(flag != "q"):
        x = int(input("X = "))
        y = int(input("Y = "))
        point_coords.append((x,y))
        flag = input("Enter q to quit input")
    
    np_point_coords = np.array(point_coords)
    img = cv2.imread("cat.jpg")
    ROIView(np_point_coords)

while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
