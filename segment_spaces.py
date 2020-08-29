import cv2
import numpy as np

def segmentspaces_input(PATH,filename,linenum):
    # Insert location of image here
    image = cv2.imread(PATH)
    ret,image = cv2.threshold(image,220,255,cv2.THRESH_BINARY)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((5, 5), np.uint8)
    img_dilated = cv2.dilate(thresh, kernel, iterations = 1)

    cnts, _ = cv2.findContours(img_dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Array of initial bounding rects
    rects = []

    # Bool array indicating which initial bounding rect has
    # already been used
    rectsUsed = []

    # Just initialize bounding rects and set all bools to false
    for cnt in cnts:
        rects.append(cv2.boundingRect(cnt))
        rectsUsed.append(False)

    # Sort bounding rects by x coordinate
    def getXFromRect(item):
        return item[0]

    rects.sort(key = getXFromRect)

    # Array of accepted rects
    acceptedRects = []

    # Merge threshold for x coordinate distance
    xThr = 5

    # Iterate all initial bounding rects
    for supIdx, supVal in enumerate(rects):
        if (rectsUsed[supIdx] == False):

            # Initialize current rect
            currxMin = supVal[0]
            currxMax = supVal[0] + supVal[2]
            curryMin = supVal[1]
            curryMax = supVal[1] + supVal[3]

            # This bounding rect is used
            rectsUsed[supIdx] = True

            # Iterate all initial bounding rects
            # starting from the next
            for subIdx, subVal in enumerate(rects[(supIdx+1):], start = (supIdx+1)):

                # Initialize merge candidate
                candxMin = subVal[0]
                candxMax = subVal[0] + subVal[2]
                candyMin = subVal[1]
                candyMax = subVal[1] + subVal[3]

                # Check if x distance between current rect
                # and merge candidate is small enough
                if (candxMin <= currxMax + xThr):

                    # Reset coordinates of current rect
                    currxMax = candxMax
                    curryMin = min(curryMin, candyMin)
                    curryMax = max(curryMax, candyMax)

                    # Merge candidate (bounding rect) is used
                    rectsUsed[subIdx] = True
                else:
                    break

            # No more merge candidates possible, accept current rect
            acceptedRects.append([currxMin, curryMin, currxMax - currxMin, curryMax - curryMin])

    # for rect in acceptedRects:
        # print(rect[0],rect[1],rect[2],rect[3])
        # img = cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (121, 11, 189), 2)

    # cv2_imshow(image)
    c=0
    c=0
    for i in range(len(acceptedRects)):
        flag=0
        stpt = [acceptedRects[i][0], acceptedRects[i][1]]
        endpt=[acceptedRects[i][0]+acceptedRects[i][2], acceptedRects[i][1]+acceptedRects[i][3]]
        if i<len(acceptedRects)-1:
            nstpt = [acceptedRects[i+1][0], acceptedRects[i+1][1]]
            nendpt=[acceptedRects[i+1][0]+acceptedRects[i+1][2], acceptedRects[i+1][1]+acceptedRects[i+1][3]]
            dis = nstpt[0]-endpt[0]
            print(dis)
            if dis > 100:
                temp1 = np.zeros((6,9), dtype=int)
                # cv2_imshow(temp1)
                flag=1
        cropp= image[stpt[1]:endpt[1], stpt[0]:endpt[0]]
        chkEmpty=cropp.shape[0]*cropp.shape[1]
        color = [255, 255, 255]
        pad=100
        if chkEmpty<1000:
            continue
        new_im = cv2.copyMakeBorder(cropp, pad, pad, pad, pad, cv2.BORDER_CONSTANT,value=color)
        c+=1
        cv2.imwrite("./static/images/{}line{}c{}.png".format(filename,linenum,c), new_im)
        if flag==1:
            c+=1
            cv2.imwrite("./static/images/{}line{}c{}.png".format(filename,linenum,c), temp1)
    return c