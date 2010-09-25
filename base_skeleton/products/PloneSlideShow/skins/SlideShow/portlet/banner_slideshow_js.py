## Script (Python) "banner_slideshow_js"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=start_frame, frames, delaytime
##title=
##
print '''<script type="text/javascript">'''
print '''    start_slideshow(%s, %s, %s);''' % (start_frame,frames,delaytime)
print '''    function start_slideshow(start_frame, end_frame, delay) {'''
print '''        setTimeout(switch_slides(start_frame,start_frame,end_frame, delay), delay);'''
print '''    }'''
print '''    function switch_slides(frame, start_frame, end_frame, delay) {'''
print '''        return (function() {'''
print '''            Effect.Fade('slideshow' + frame);'''
print '''            if (frame == end_frame) { frame = start_frame; } else { frame = frame + 1; }'''
print '''            setTimeout("Effect.Appear('slideshow" + frame + "');", 850);'''
print '''            setTimeout(switch_slides(frame, start_frame, end_frame, delay), delay + 850);'''
print '''        })'''
print '''    }'''
print '''</script>'''

return printed
