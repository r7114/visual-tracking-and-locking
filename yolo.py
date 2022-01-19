import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

import core.utils as utils
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from threading import Thread



def get_boxes(f,data,score,coi,scale):
    h, w, _ = f.shape
    l = []
    for i in range(data[3][0]):
        if np.int(data[2][0][i]) in coi:
            if data[1][0][i] > score:
                coor = np.copy(data[0][0][i])
                coor[0] = coor[0] * h
                coor[2] = coor[2] * h
                coor[1] = coor[1] * w
                coor[3] = coor[3] * w
                c1, c2 = np.array([coor[1], coor[0]]), np.array([coor[3], coor[2]])
                c3 = np.array([(coor[1]+coor[3])/2, (coor[0]+coor[2])/2])
                
                c1 = (c1 - c3)*scale + c3
                c2 = (c2 - c3)*scale + c3
                
                c1 = c1.astype(np.int)
                c2 = c2.astype(np.int)
                c3 = c3.astype(np.int)
                
                l.append([c1,c2,c3])

    return l




class flag_class:
    def __init__(self):
        self.framework = tf
        self.weights = './yolov4-tiny-416'
        self.size = 416
        self.tiny = True
        self.model = 'yolov4'
        self.video = '0'
        self.output = None
        self.output_format = 'XVID'
        self.iou = 0.45
        self.score = 0.25
        self.dont_show  = False

FLAGS = flag_class()


config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
input_size = FLAGS.size
video_path = FLAGS.video



saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']




class handler:
    def __init__(self,img_src,coi,sr,scale):
        self.img_scr = img_src
        self.coi = coi # class of interest
        self.sr = sr  # score requirement 
        self.scale = scale
        self.running = False
        
        self.l = []

        Thread(target = self.t1).start()



    def t1(self):

        while True:
            if self.running:
                frame = self.img_scr()
    
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
    
                
            
                image_data = cv2.resize(frame, (input_size, input_size))
                image_data = image_data / 255.
                image_data = image_data[np.newaxis, ...].astype(np.float32)
            
                batch_data = tf.constant(image_data)
                pred_bbox = infer(batch_data)
                for key, value in pred_bbox.items():
                    boxes = value[:, :, 0:4]
                    pred_conf = value[:, :, 4:]
                        
                
                boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
                    boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
                    scores=tf.reshape(
                        pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                    max_output_size_per_class=50,
                    max_total_size=50,
                    iou_threshold=FLAGS.iou,
                    score_threshold=FLAGS.score
                )
                pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
            
            
                
                image = np.asarray(frame)
                
                l = get_boxes(image,pred_bbox,self.sr,self.coi,self.scale)
                
                self.l = l # list of target
                #print(l)
                
                '''
                for i in l:
                    #print(i)
                    c1, c2, c3 = i
                    cv2.rectangle(image, (c1[0],c1[1]),(c2[0],c2[1]), (0,255,0), 3)
                    cv2.circle(image, (c3[0],c3[1]), radius=3, color=(0, 255, 0), thickness=3)
                
                
                
                cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
                result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
    
                cv2.imshow("result", result)
                
                cv2.waitKey(1)
                '''
            
            
    
    
    
    




































