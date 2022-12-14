#!/usr/bin/env python3
#Checkout http://wiki.ros.org/cv_bridge/Tutorials

import sys
import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import sys
sys.path.insert(0, r'rootfs/catkin_ws/src/ros_basics_tutorials/scripts/HybridNets/')
import time
import torch
import torchvision.transforms as T
from torch.backends import cudnn
from glob import glob
from HybridNets.utils.utils import letterbox, scale_coords, postprocess, BBoxTransform, ClipBoxes, restricted_float, \
    boolean_string, Params
from HybridNets.utils.plot import STANDARD_COLORS, standard_to_bgr, get_index_label, plot_one_box
import os
from torchvision import transforms
import argparse
from HybridNets.utils.constants import *
from ros_basics_tutorials.msg import BoundingBox, BoundingBoxes, ObjectCount


boxes = BoundingBoxes();

# load models from pytorch
model = torch.hub.load('datvuthanh/hybridnets', 'hybridnets', pretrained=True,trust_repo=True)
torch.save(model.state_dict(), 'model_weights.pth')
weight = (torch.load('model_weights.pth'))
model.requires_grad_(False) #Note: something about the training, recheck
model.eval()
color_list_seg = {}

# initialize the bridge library to transfer bag file into cv2 file 
bridge = CvBridge()

def callback_Img(data):
	# Reading the images and catch the error if any
	try:
		img = bridge.imgmsg_to_cv2(data, desired_encoding='rgb8')
	except CvBridgeError as e:
		print(e)

	# Initialization of paths
	# NOTE: change your path accordingly 
	params = Params(f'/root/rootfs/catkin_ws/src/ros_basics_tutorials/scripts/bdd100k.yml') 
	input_imgs = []
	shapes = []
	det_only_imgs = []
	# NOTE: change your path accordingly 
	output = '/root/rootfs/catkin_ws/src/ros_basics_tutorials/scripts/' 
	output = output[:-1]
	source = '/content' # NOTE: change your path accordingly 
	img_path = glob(f'{source}/*.jpg')
	color_list_seg = {}
	
	for seg_class in params.seg_list:
		# edit your color here if you wanna fix to your liking
		color_list_seg[seg_class] = list(np.random.choice(range(256), size=3))

	anchors_ratios = params.anchors_ratios
	anchors_scales = params.anchors_scales
	
	# for running in GPU
	cudnn.fastest = True
	cudnn.benchmark = True

	obj_list = params.obj_list
	seg_list = params.seg_list

	color_list = standard_to_bgr(STANDARD_COLORS)
	
	# IMPORTANT: convert your image to RGB color space and put it into array
	ori_imgs = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB)] 
	resized_shape = params.model['image_size']
	
	# Resizing
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
		shapes.append(((h0, w0), ((h / h0, w / w0), pad)))  # for COCO mAP rescaling


	# Using pytorch
	x = torch.stack([transform(fi) for fi in input_imgs], 0)
	x = x.to(torch.float32)
	weight_last_layer_seg = weight['segmentation_head.0.weight']
	if weight_last_layer_seg.size(0) == 1:
		seg_mode = BINARY_MODE
	else:
		if params.seg_multilabel:
			seg_mode = MULTILABEL_MODE
		else:
			seg_mode = MULTICLASS_MODE
	#print("DETECTED SEGMENTATION MODE FROM WEIGHT AND PROJECT FILE:", seg_mode) # -> For testing 
	
	model.load_state_dict(weight)
	model.requires_grad_(False)
	model.eval()
	
	# NOTE: find the road segments and lane detections
	with torch.no_grad():
		features, regression, classification, anchors, seg = model(x)

		# in case of MULTILABEL_MODE, each segmentation class gets their own inference image
		seg_mask_list = []
		# (B, C, W, H) -> (B, W, H)
		# test case with multiclass
		_, seg_mask = torch.max(seg,1)
		seg_mask_list.append(seg_mask)
		#seg_mask_list = [torch.where(torch.sigmoid(seg)[:, i, ...] >= 0.5, 1, 0) for i in range(seg.size(1))]
		# but remove background class from the list
		#seg_mask_list.pop(0)

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

				color_mask = np.mean(color_seg, 2)  # (H, W, C) -> (H, W), check if any pixel is not background
				# prepare to show det on 2 different imgs
				# (with and without seg) -> (full and det_only)
				####important
				det_only_imgs.append(ori_imgs[i].copy())
				seg_img = ori_imgs[i]  # do not work on original images if MULTILABEL_MODE IMPORTANT do seg_img = ori_imgs[i].copy() in stead
				seg_img[color_mask != 0] = seg_img[color_mask != 0] * 0.5 + color_seg[color_mask != 0] * 0.5
				seg_img = seg_img.astype(np.uint8)
				seg_filename = f'{output}/{i}_{params.seg_list[seg_class_index]}_seg.jpg' 
				
				
				newImage = cv2.cvtColor(seg_img, cv2.COLOR_RGB2BGR)
				cv2.imwrite(seg_filename, cv2.cvtColor(newImage, cv2.COLOR_RGB2BGR)) # producing image output, might comment out if unneccessary
				
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
		
		# Note: Drawing the bounding box for cars
		
		for i in range(len(ori_imgs)):
			out[i]['rois'] = scale_coords(ori_imgs[i][:2], out[i]['rois'], shapes[i][0], shapes[i][1])
			boxes.bounding_boxes = []
			for j in range(len(out[i]['rois'])):
				x1, y1, x2, y2 = out[i]['rois'][j].astype(int)
				obj = obj_list[out[i]['class_ids'][j]]
				score = float(out[i]['scores'][j])
				plot_one_box(ori_imgs[i], [x1, y1, x2, y2], label=obj, score=score, color=color_list[get_index_label(obj, obj_list)])
				
				#Add to BoundingBoxes
				box = BoundingBox()
				box.xmin = x1
				box.xmax = x2
				box.ymin = y1
				box.ymax = y2
				box.id = j
				box.probability = score
				box.Class = obj
				boxes.bounding_boxes.append(box)
				boxPub.publish(boxes);


				if show_det:
					plot_one_box(det_only_imgs[i], [x1, y1, x2, y2], label=obj, score=score, color=color_list[get_index_label(obj, obj_list)]) # chang to original image
		
			if show_det:
				cv2.imwrite(f'{output}/{i}_det.jpg',  cv2.cvtColor(det_only_imgs[i], cv2.COLOR_RGB2BGR))

			if imshow:
				cv2.imshow('img', ori_imgs[i])
				cv2.waitKey(0)

			if imwrite:
				cv2.imwrite(f'{output}/{i}.jpg', cv2.cvtColor(ori_imgs[i], cv2.COLOR_RGB2BGR))

	gray = cv2.cvtColor(ori_imgs[0], cv2.COLOR_BGR2GRAY) # This is for vnc output
	
	# Convert into color spaces for image outputs
	color = ori_imgs[0].copy() #This is for images output
	color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
	cv2.imwrite(f'{output}/{i}.jpg', cv2.cvtColor(color, cv2.COLOR_RGB2BGR))
	
	# Transfer back into bag file type images
	grayImageMsg = CvBridge().cv2_to_imgmsg(gray.astype(np.uint8)) 
	grayImageMsg.header = data.header
	grayImageMsg.encoding = '8UC1'
	grayImgPub.publish(grayImageMsg) 





																																																																																																										
	


# Publish ros into img_gray
rospy.init_node('img_record_node')
rospy.Subscriber("/front_camera/image_raw", Image, callback_Img)
grayImgPub = rospy.Publisher('/img_gray', Image, queue_size=10)
boxPub = rospy.Publisher('bounding_boxes', BoundingBoxes, queue_size=10)
rospy.spin()


