import os
import shutil

import qrcode
import cv2

from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

def createqr(data, name):
	# output file name
	filename = f"{name}.JPG"
	# generate qr code
	img = qrcode.make(data)
	# save img to a file
	img.save(filename)

def readqr(fname):
	# preprocessing using opencv
	im = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
	blur = cv2.GaussianBlur(im, (5, 5), 0)
	ret, bw_im = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# scanning the image using pyzbar
	qrscan = decode(bw_im, symbols=[ZBarSymbol.QRCODE])

	if(len(qrscan)>0):
		return qrscan[0].data.decode()
	else:
		return False	
  	  
if __name__ == '__main__':
	# lising the image files in the folder
	files = [f for f in sorted(os.listdir('.')) if os.path.isfile(f) if f.endswith("jpg") or f.endswith("png") or f.endswith("jpeg") or f.endswith('JPG')]
	if(len (files)==0):
		print('no images are present')
		exit()
	else:
		pass	

	event_dir = ''

	for f in files:
		# scanning the files 
		scan = readqr(f)
		if (scan!=False):
			created = scan

			if(created[:-2] != event_dir):
				event_dir = created[:-2]
				# creating directory for the event
				os.mkdir(event_dir)


			try:
				# creating new directory with the client id 
				os.mkdir(scan)
				# moving the client dir to event dir 
				image_dir = shutil.move(scan, event_dir)
				# renaming the qr code file after folder creating
				qrname = f'qr-{f}'
				os.rename(f, qrname)
				shutil.move(qrname, image_dir)
				# initializing image count to be placed in that client folder 
				no_of_images = 0

			except Exception as e:
				print(e)
				exit()
			
		else:
			no_of_images += 1
			file_rename = f"{created}{'{:03}'.format(no_of_images)}.JPG"
			os.rename(f, file_rename)
			new_path = shutil.move(file_rename, image_dir)
			print(f'{f} moved to {new_path}')


	# moving the folders into a city folder
	# city_folder = created[0:13]	
	# os.mkdir(city_folder)
	# for f in os.listdir('.'):
	# 	if not os.path.isfile(f):
	# 		shutil.move(f, city_folder)
			
	# print('task completed successfully')		

	



