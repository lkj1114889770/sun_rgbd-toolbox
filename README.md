A simple python based toolbox to get bbox2D for the SUNCG dataset.
The sun-rgbd dataset can be downloaded from [here](http://rgbd.cs.princeton.edu/data/SUNRGBD.zip), please see the [offical webpage](http://rgbd.cs.princeton.edu/) for more details about the data.

You can test the bbox annotation like this after dumps the lables_bbox2D.json file.

	def apply_bbox(image,bbox):
	    draw=ImageDraw.Draw(image)
	    x1,y1,x2,y2=bbox
	    draw.line((x1,y1,x2,y1,x2,y2,x1,y2,x1,y1),'red')
	    return image
	img=Image.open(annotations[10]['image'])
	print(annotations[10]['annotation'][4]['class_name'])
	apply_bbox(img,bbox=annotations[10]['annotation'][4]['bbox']) 

![](/img/1.png)