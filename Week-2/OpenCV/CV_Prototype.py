import cv2
import numpy as np

point_count = 0
point_coords = []
ix,iy = 0,0
drag = False
dragpoint = False
poi = 0
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

# to update x and y region of a selected point
def updatepoint(x, y, poi):
    global point_coords, ix, iy
    if ix - x <= 0:                                                                     # dragged to the right
        point_coords[poi] = (point_coords[poi][0] + int(abs(ix - x)), point_coords[poi][1])
    elif ix - x > 0:                                                                    # dragged to the left
        point_coords[poi] = (point_coords[poi][0] - int(abs(ix - x)), point_coords[poi][1])
    if iy - y <= 0:                                                                     # dragged to the bottom
        point_coords[poi] = (point_coords[poi][0], point_coords[poi][1] + int(abs(iy - y)))
    elif iy - y > 0:                                                                    # dragged to the top
        point_coords[poi] = (point_coords[poi][0], point_coords[poi][1] - int(abs(iy - y)))
    ix,iy = x,y

# to drag selected region
def movepoint(event, x, y, flags, param):
    global drag, img, point_coords, ix, iy, dragpoint, poi, point_count

    np_point_coords = np.array(point_coords, np.int32) 
    np_point_coords = np_point_coords.reshape((-1,1,2))

    if event == cv2.EVENT_LBUTTONDOWN:  #to drag either point or selected area
        ix, iy = x,y
        cv2.polylines(img, [np_point_coords], True, (255,255,255))

        for i in range(len(point_coords)):
            if (((x - point_coords[i][0])**2 + (y - point_coords[i][1])**2)**0.5) < 5:
                dragpoint = True
                poi = i

        if cv2.pointPolygonTest(np_point_coords, (x,y), False) > 0 and not dragpoint:     #if cursor is within the marked region
            drag = True

    elif event == cv2.EVENT_MOUSEMOVE:  #motion of dragging point/selected area
        if drag: 
            cv2.imshow('image', img)
            updatepoints(x,y)
            np_point_coords = np.array(point_coords, np.int32)
            cv2.polylines(img, [np_point_coords], True, (255,255,255))

        elif dragpoint:
            cv2.imshow('image', img)
            updatepoint(x,y,poi)
            cv2.circle(img, (point_coords[poi][0],point_coords[poi][1]), 2, (255,255,0), -1)

    elif event == cv2.EVENT_LBUTTONUP:  #stopping motion of dragged point/selected area
        drag = False
        dragpoint = False
        img = cv2.imread('cat.jpg')
        draw_image()
        ix,iy = 0,0
        
    elif event == cv2.EVENT_LBUTTONDBLCLK:  #regenerate ROI window
        cv2.destroyWindow('ROI')
        ROIView(np_point_coords)

    elif event == cv2.EVENT_MBUTTONDOWN:    #add new point wrt first point
        point_coords.append((x,y))
        point_count += 1
        draw_image()

    elif event == cv2.EVENT_RBUTTONDOWN:
        for i in range(len(point_coords)):
            if ((((x - point_coords[i][0])**2 + (y - point_coords[i][1])**2)**0.5) < 5) and point_count > 3:
                del point_coords[i]
                point_count -= 1
                break

    elif event == cv2.EVENT_RBUTTONUP:
        draw_image()

# to draw the image
def draw_image():
    img = cv2.imread('cat.jpg')
    np_point_coords = np.array(point_coords, np.int32) #excluding last input
    np_point_coords = np_point_coords.reshape((-1,1,2))
    cv2.polylines(img, [np_point_coords], True, (255,255,255))
    for i in range(len(point_coords)):
        cv2.circle(img, (point_coords[i][0],point_coords[i][1]), 5, (255,255,255), -1)
    cv2.imshow('image',img)
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
    global img
    cv2.namedWindow('ROI')
    cv2.moveWindow('ROI', 1000,1000)
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [point_coords], color=(255,255,255))
    img = cv2.imread('cat.jpg')
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
    global point_coords, point_count, img

    #if lbutton is held down
    if event == cv2.EVENT_LBUTTONDOWN:
        point_count+=1
        point_coords.append((x,y))
        cv2.circle(img, (x,y), 5, (255,255,255), -1)

        #connect lines if more than one point
        if point_count > 1:
            for i in range (len(point_coords)-1):
                cv2.line(img, point_coords[i], point_coords[i+1], (255,255,255), 2)

        #fill in last line if point returns back to original point
        if point_count > 2:
            dist = (((x - point_coords[0][0]) ** 2) + ((y - point_coords[0][1]) ** 2))**0.5

            if dist < 10:
                img = np.copy(img)
                del point_coords[-1]
                point_count -= 1
                np_point_coords = draw_image()
                ROIView(np_point_coords)


choice = int(input("Enter 1 to plot points on image or 2 to enter coordinates manually\n"))
if(choice == 1):
    img = cv2.imread("cat.jpg")
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', plotpoints)   
else:
    user_input = "Manual"
    input_str = input("Enter the coordinates\n")
    input_str = input_str.strip('[]')
    for pair in input_str.split('),'):
        pair = pair.strip().strip('()')
        point_coords.append(tuple(map(int, pair.split(','))))

    np_point_coords = np.array(point_coords)
    img = cv2.imread("cat.jpg")
    ROIView(np_point_coords)

while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
