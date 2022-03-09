
import cv2
from particle_filter import ParticleFilter,read_video,read_masks,gt_centroid, square_size
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

def create_legend(img,pt1,pt2):
    text1 = "Before resampling"
    cv2.putText(img,text1, pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))
    text2 = "After resampling"
    cv2.putText(img,text2, pt2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
    
def main():
    image_name = "bear"
    video  =read_video(image_name, r'.\sequences-train')
    first_frame = video[:,:,:,0]
    print(video.shape)

    masks = read_masks(image_name, r'.\sequences-train')
    print("MAIN:",first_frame.shape)
    
    
    first_frame = cv2.cvtColor(first_frame.astype('uint8'), cv2.COLOR_BGR2HSV)
    first_mask = masks[:,:,0,0].astype('uint8')
    x,y = gt_centroid(masks[:,:,:,0])

    sq_size = square_size(masks[:,:,:,0])
    print(sq_size)
    seg = first_frame[first_mask==0]=0
    pf = ParticleFilter(x,y,first_frame, first_mask=first_mask,n_particles=500,square_size=sq_size,
    						dt=0.20)
    alpha = 0.5
    index =-1
    for index in range(video.shape[3]-1):
    # while index < video.shape[3]:
        print(index)
        index+=1
        frame  = video[:,:,:,index].astype('uint8')      
        orig = np.array(frame)
        img = frame
        norm_factor = 255.0/np.sum(frame,axis=2)[:,:,np.newaxis]

        frame = frame*norm_factor
        frame = cv2.convertScaleAbs(frame)
        frame = cv2.blur(frame,(5,5))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        x,y,sq_size,distrib,distrib_control = pf.next_state(frame)
        p1 = (int(y-sq_size),int(x-sq_size))
        p2 = (int(y+sq_size),int(x+sq_size))
        
        # before resampling
        for (x2,y2,scale2) in distrib_control:
            x2 = int(x2)
            y2 = int(y2)
            cv2.circle(img, (y2,x2), 1, (255,0,0),thickness=10) 
        # after resampling
        for (x1,y1,scale1) in distrib:
            x1 = int(x1)
            y1 = int(y1)
            cv2.circle(img, (y1,x1), 1, (0,0,255),thickness=10) 
        	

        cv2.rectangle(img,p1,p2,(0,0,255),thickness=5)

        cv2.addWeighted(orig, alpha, img, 1 - alpha,0, img)   
        create_legend(img,(40,40),(40,20))

        cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break       






    # cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
