# Welcome to the rlhelper documentation.  
  
As of 11/28/2019, rlhelper helps with 2 things:  
1. Drawing customized strings with fewer lines of code  
2. Placing centred images and titles on 1 or 2 columns  
  
## Drawing customized strings with fewer lines of code:  
Input: points (1/72 inch)  
  
Draw a string with a specific font, color, weight, and size (left-aligned):  
  
simplestring(c, x, y, string, font color, font weight, font size)  
c = ReportLab canvas object  
x = x coordinate  
y = y coordinate  
string = string  
font color = color  
font weight = weight of font, assuming it is registered  
font size = font size  
  
Draw a centered string:  
  
simpleCentredstring(c, x, y, string, font color, font weight, font size)  
x = x coordinate for center of string  
see “simplestring” above for all other arguments  
  
Draw a string with multiple colors, fonts, sizes, and/or weights:  
 
complexCentredstring(c, x, y, strings, font colors, font weights, font sizes)  
x = x coordinate for center of string  
see “simplestring” above for all other arguments  
note: strings, font colors, font weights, and font sizes all accept lists for arguments.  
  
  
## Placing centred images and titles on 1 or 2 columns:  
  
Assumptions (unless otherwise specified):  
Margins are equal on left and right sides.  
Margins are equal on top and bottom.  
Crop (or “bleed space”) values are equal on left and right sides.  
Crop (or “bleed space”) values are equal on top and bottom.  
Input: inches  
Output: points (1/72 inch)  
  
Get y coordinate of top image:  
  
top_im_y(c, adj, page height, chart height, top margin)  
c = ReportLab canvas object  
adj = adjustment (if needed, else use 0)  
page height = height of page including total of margins and crop  
chart height = image height  
top margin = top margin + top crop  
  
Get y coordinate of image under the top image:  
  
under_im_y(c, adj, page height, c_above_y, chart height)  
c = ReportLab canvas object  
adj = adjustment (if needed, else use 0)  
page height = height of page including total of margins and crop  
c_above_y = y location of bottom of chart above  
chart height = image height  
  
Get x coordinate (in points) to center an image (or its title) on the left column:  
  
left_im_cntr(c, width, margin, center margin, page width)  
c = ReportLab canvas object  
width = image width  
margin = page margin - including crop, if any.  
center margin = space to allow between columns  
page width = width of page including total of margins and crop  
  
Get x coordinate (in points) to center an image (or its title) on the right column:  
  
right_im_cntr(c, width, margin, center margin, page width)  
See left_im_cntr above.  
  
  
### Future Iterations will include functions that…  
Draw simple and complex strings that adjust for spacing between characters  
Return x coordinate to center images and titles where there are more than 2 columns  
Return y coordinate for bottom image  
Generate customized table of contents entries  
Generate customized page numbers  
Generate crop lines  
Crop a document based on a value  
Other? Feel free to submit ideas