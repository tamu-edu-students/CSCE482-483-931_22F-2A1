#!/usr/bin/env python3
#Checkout http://wiki.ros.org/cv_bridge/Tutorials
import sys
import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import torch
import sys
sys.path.insert(0, r'rootfs/rootfs/catkin_ws/src/ros_basics_tutorials/scripts/HybridNets/')
import time
import cv2
import torch
import torchvision.transforms as T
import torch
import time
import cv2

import time
import torch
from torch.backends import cudnn
#from backbone import HybridNetsBackbone
import cv2
import numpy as np
from glob import glob
from HybridNets.utils.utils import letterbox, scale_coords, postprocess, BBoxTransform, ClipBoxes, restricted_float, \
    boolean_string, Params
from HybridNets.utils.plot import STANDARD_COLORS, standard_to_bgr, get_index_label, plot_one_box
import os
from torchvision import transforms
import argparse
from HybridNets.utils.constants import *
from glob import glob
#from ros_basics_tutorials.msg import BoundingBox, BoundingBoxes, ObjectCount
#import cv2_imshow

#boxes = BoundingBoxes();
# load model
model = torch.hub.load('datvuthanh/hybridnets', 'hybridnets', pretrained=True)
torch.save(model.state_dict(), 'model_weights.pth')
#img = torch.randn(1,3,640,384)
#model.eval()
weight = (torch.load('model_weights.pth'))
model.requires_grad_(False) #Note: something about the training, recheck
model.eval()
color_list_seg = {}

#print("check-point")
#features, regression, classification, anchors, segmentation = model(img)
#help(model.eval())
#print(classification)
#help(model)
# print(features)
#print(model)
#help(model._parameters)


#print("Khai is good")
bridge = CvBridge()
print("check-point")
def callback_Img(data):
	#print("got an image")
	global bridge
	#print("Khai is good")
	try:
		img = bridge.imgmsg_to_cv2(data, desired_encoding='rgb8')
	except CvBridgeError as e:
		print(e)
	#print("Khai is insite")
	# Start coordinate, here (5, 5)
	# represents the top left corner of rectangle
	#start_point = (5, 5)
	#cv2.imwrite(f'{output}/origin.jpg', img)
	# Ending coordinate, here (220, 220)
	# represents the bottom right corner of rectangle
	#end_point = (220, 220)

	# Blue color in BGR
	#color = (255, 0, 0)


	# Line thickness of 2 px
	#thickness = 2
	#img = cv2.rectangle(img, start_point, end_point, color, thickness)
	#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


	# This is the lines of code from Hybridnets

	# Initialization
	params = Params(f'/root/rootfs/rootfs/catkin_ws/src/ros_basics_tutorials/scripts/bdd100k.yml')
	input_imgs = []
	shapes = []
	output = '/root/rootfs/rootfs/catkin_ws/src/ros_basics_tutorials/scripts/'
	output = output[:-1]
	# Might not need this in the ROS package
	source = '/content'
	img_path = glob(f'{source}/*.jpg')
	color_list_seg = {}
	for seg_class in params.seg_list:
		# edit your color here if you wanna fix to your liking
		color_list_seg[seg_class] = list(np.random.choice(range(256), size=3))
	#compound_coef = args.compound_coef
	#source = args.source

	input_imgs = []
	shapes = []
	det_only_imgs = []

	anchors_ratios = params.anchors_ratios
	anchors_scales = params.anchors_scales


	#imshow = args.imshow
	#imwrite = args.imwrite
	#show_det = args.show_det
	#show_seg = args.show_seg
	#os.makedirs(output, exist_ok=True)

	#use_cuda = args.cuda
	#use_float16 = args.float16
	cudnn.fastest = True
	cudnn.benchmark = True

	obj_list = params.obj_list
	seg_list = params.seg_list

	color_list = standard_to_bgr(STANDARD_COLORS)
	# ori_imgs = [cv2.imread(i, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION) for i in img_path] # Change
	#ori_imgs = cv2.imread(img, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION)
	
	#img1 = cv2.imread(img, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION) 
	#ori_imgs.append(img)
	#ori_imgs = [cv2.cvtColor(i, cv2.COLOR_BGR2RGB) for i in ori_imgs]
	ori_imgs = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB)]
	cv2.imwrite(f'{output}/i.jpg', ori_imgs[0])
	#print(f"FOUND {len(ori_imgs)} IMAGES")
	# cv2.imwrite('ori.jpg', ori_imgs[0])
	# cv2.imwrite('normalized.jpg', normalized_imgs[0]*255)
	#cv2.imwrite(f'test.jpg', ori_imgs[0])
	resized_shape = params.model['image_size']
	if isinstance(resized_shape, list):
		resized_shape = max(resized_shape)
		normalize = transforms.Normalize(
		mean=params.mean, std=params.std
		)
		transform = transforms.Compose([
		transforms.ToTensor(),
		normalize,
		])
	for ori_img in ori_imgs:
		h0, w0 = ori_img.shape[:2]  # orig hw
		r = resized_shape / max(h0, w0)  # resize image to img_size
		input_img = cv2.resize(ori_img, (int(w0 * r), int(h0 * r)), interpolation=cv2.INTER_AREA)
		h, w = input_img.shape[:2]

		(input_img, _), ratio, pad = letterbox((input_img, None), resized_shape, auto=True,
			      scaleup=False)

		input_imgs.append(input_img)
		# cv2.imwrite('input.jpg', input_img * 255)
		shapes.append(((h0, w0), ((h / h0, w / w0), pad)))  # for COCO mAP rescaling



	x = torch.stack([transform(fi) for fi in input_imgs], 0)

	x = x.to(torch.float32)
	# print(x.shape)
	#weight = torch.load(weight)
	#new_weight = OrderedDict((k[6:], v) for k, v in weight['model'].items())
	weight_last_layer_seg = weight['segmentation_head.0.weight']
	if weight_last_layer_seg.size(0) == 1:
		seg_mode = BINARY_MODE
	else:
		if params.seg_multilabel:
			seg_mode = MULTILABEL_MODE
		else:
			seg_mode = MULTICLASS_MODE
	#print("DETECTED SEGMENTATION MODE FROM WEIGHT AND PROJECT FILE:", seg_mode)

	model.load_state_dict(weight)

	model.requires_grad_(False)
	model.eval()


	with torch.no_grad():
		features, regression, classification, anchors, seg = model(x)

		# in case of MULTILABEL_MODE, each segmentation class gets their own inference image
		seg_mask_list = []
		# (B, C, W, H) -> (B, W, H)

		seg_mask_list = [torch.where(torch.sigmoid(seg)[:, i, ...] >= 0.5, 1, 0) for i in range(seg.size(1))]
		# but remove background class from the list
		seg_mask_list.pop(0)

		# (B, W, H) -> (W, H)
		for i in range(seg.size(0)):
			#   print(i)
			for seg_class_index, seg_mask in enumerate(seg_mask_list):
				seg_mask_ = seg_mask[i].squeeze().cpu().numpy()
				pad_h = int(shapes[i][1][1][1])
				pad_w = int(shapes[i][1][1][0])
				seg_mask_ = seg_mask_[pad_h:seg_mask_.shape[0]-pad_h, pad_w:seg_mask_.shape[1]-pad_w]
				seg_mask_ = cv2.resize(seg_mask_, dsize=shapes[i][0][::-1], interpolation=cv2.INTER_NEAREST)
				color_seg = np.zeros((seg_mask_.shape[0], seg_mask_.shape[1], 3), dtype=np.uint8)
				for index, seg_class in enumerate(params.seg_list):
					color_seg[seg_mask_ == index+1] = color_list_seg[seg_class]
				color_seg = color_seg[..., ::-1]  # RGB -> BGR
				# cv2.imwrite('seg_only_{}.jpg'.format(i), color_seg)

				color_mask = np.mean(color_seg, 2)  # (H, W, C) -> (H, W), check if any pixel is not background
				# prepare to show det on 2 different imgs
				# (with and without seg) -> (full and det_only)
				det_only_imgs.append(ori_imgs[i].copy())
				seg_img = ori_imgs[i].copy()  # do not work on original images if MULTILABEL_MODE
				seg_img[color_mask != 0] = seg_img[color_mask != 0] * 0.5 + color_seg[color_mask != 0] * 0.5
				seg_img = seg_img.astype(np.uint8)
				seg_filename = f'{output}/{i}_{params.seg_list[seg_class_index]}_seg.jpg' 

				cv2.imwrite(seg_filename, cv2.cvtColor(seg_img, cv2.COLOR_RGB2BGR))
				seg_img = seg_img.astype(np.uint8)

		regressBoxes = BBoxTransform()
		clipBoxes = ClipBoxes()
		out = postprocess(x,
		anchors, regression, classification,
		regressBoxes, clipBoxes,
		0.25, 0.3)
		show_det = True #Might change this
		imshow = False
		imwrite = True
		for i in range(len(ori_imgs)):
			#print(i)
			#cv2_imshow(ori_imgs[i])
			out[i]['rois'] = scale_coords(ori_imgs[i][:2], out[i]['rois'], shapes[i][0], shapes[i][1])
			for j in range(len(out[i]['rois'])):
				x1, y1, x2, y2 = out[i]['rois'][j].astype(int)
				obj = obj_list[out[i]['class_ids'][j]]
				score = float(out[i]['scores'][j])
				plot_one_box(ori_imgs[i], [x1, y1, x2, y2], label=obj, score=score, color=color_list[get_index_label(obj, obj_list)])
				
				#Add to BoundingBoxes
				#box = BoundingBox()
				#box.xmin = x1
				#box.xmax = x2
				#box.ymin = y1
				#box.ymax = y2
				#box.id = j
				#box.probability = score
				#box.Class = obj
				#boxes.bounding_boxes.append(box)
				
				#print(box.xmin)
				#print(box.xmax)
				#print(box.ymin)
				#print(box.ymax)
				#print(box.id)
				#print(box.probability)
				#print(box.Class) 

                               #cv2_imshow(ori_imgs[i])
				#grayImageMsg = CvBridge().cv2_to_imgmsg(ori_imgs[i].astype(np.uint8))
	#grayImageMsg.header = data.header
				#grayImageMsg.encoding = '8UC1'
				#grayImgPub.publish(grayImageMsg)

				if show_det:
					plot_one_box(det_only_imgs[i], [x1, y1, x2, y2], label=obj, score=score, color=color_list[get_index_label(obj, obj_list)])
			#cv2.imshow(ori_imgs[i])
			if show_det:
				cv2.imwrite(f'{output}/{i}_det.jpg',  cv2.cvtColor(det_only_imgs[i], cv2.COLOR_RGB2BGR))

			if imshow:
				cv2.imshow('img', ori_imgs[i])
				cv2.waitKey(0)

			if imwrite:
				cv2.imwrite(f'{output}/{i}.jpg', cv2.cvtColor(ori_imgs[i], cv2.COLOR_RGB2BGR))
	gray = cv2.cvtColor(ori_imgs[0], cv2.COLOR_RGB2BGR)
	#cv2.imwrite(f'{output}/{i}.jpg', cv2.cvtColor(gray, cv2.COLOR_RGB2BGR))
	#print("check-point")
	# cv2.imshow('img',gray)
	
	grayImageMsg = CvBridge().cv2_to_imgmsg(gray.astype(np.uint8)) #change
	grayImageMsg.header = data.header
	grayImageMsg.encoding = '8UC1' #Change
	grayImgPub.publish(grayImageMsg) #Change




	



	# end of copy paste




	



rospy.init_node('img_record_node')
rospy.Subscriber("/front_camera/image_raw", Image, callback_Img)
#print("check")
grayImgPub = rospy.Publisher('/img_gray', Image, queue_size=10)
#print("check2")
rospy.spin()

