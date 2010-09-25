var Item = false;
var atual = false;

function changeOpac(opacity){
                             var obj = $('to-blend').style; 
                             obj.opacity=(opacity/100);
                             obj.MozOpacity=(opacity/100);
                             obj.KhtmlOpacity=(opacity/100);
}

function blend(imagefile){
                          var speed = 7;
                          var timer = 0;
                          if(Item[atual][0]!=" B"){
                                                   for(i = 185; i > 0; i-=2){ 
                                                                             setTimeout('changeOpac('+i+')', timer++ * speed);
                                                   }
                                                   if(!d.all){ 
                                                              setTimeout('changeContent()', timer * speed);
                                                   }
                                                   for(i = 0; i <= 185; i+=2){ 
                                                                              setTimeout('changeOpac('+i+')', timer++ * speed);
                                                   }
                          }
                          else{
                               if(!d.all){ 
                                          setTimeout('changeContent()', timer * speed);
                               }
                          }
}


function changeImg(id){
                       clearTimeout(timeoutId);
                       atual+=parseInt(id);
                       if(Item != false){
                        if(atual>Item.length-1) atual = 0;
                        if(atual<0) atual = Item.length-1;
                        if(imgDsp[atual].complete==false){
                                                          atual--;
                                                          timeoutId = setTimeout('changeImg('+id+')',500);
                                                          return;
                        } 
                       
                        if(d.all && navigator.userAgent.indexOf('Opera')==-1){
                                                                              try {
                                                                                   oDiv = $('to-blend');
                                                                                   oDiv.style.filter='blendTrans(duration=1.2)';
                                                                                   oDiv.filters.blendTrans.apply();
                                                                                   oDiv.filters.blendTrans.play();
                                                                                   changeContent();
                                                                              }
                                                                              catch(e){blend();}
                        }
                        else{blend();}
                      }
                       timeoutId = setTimeout('changeImg(1)',7000)
}


function loadImages(){
                      if (Item != false){
                       imgDsp = new Array();
                       for(n=0;n<Item.length;n++){
                                                  imgDsp[n] = new Array();
                                                  imgDsp[n].src = Item[n][1];
                       }
                      }
                      okToGo = true;
}

function changeContent(){
                         var type = Item[atual][6];
                         if (type != 'File'){
                          d.img1.src = imgDsp[atual].src;
                          d.img1.id = 'imgslide';
                          d.getElementById("chamadaImagem").href = Item[atual][3];
                          d.getElementById("credito").innerHTML = Item[atual][0];
                          $('chamadaLinks').innerHTML = '<a href="'+Item[atual][3]+'" id="p-link" target="_parent" alt="'+Item[atual][2]+'" title="'+Item[atual][2]+'"><div id="txt1"><span class="title">'+Item[atual][2]+'</span><BR/>'+Item[atual][5]+'</div></a>';
                         }
                         if (type == 'File'){
                          d.img1.src = 'cleardot.gif';
                          d.img1.width = '1';
                          d.img1.id = 'objflash';
                          d.getElementById("credito").innerHTML = Item[atual][0];
                          $('chamadaLinks').innerHTML = '<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=7,0,0,0" width="100%" height="100%"><param name="wmode" value="transparent"> <param name="movie" value="'+Item[atual][3]+'"> <param name="quality" value="high"> <param name="bgcolor" value="#FFFFFF"> <embed src="'+Item[atual][3]+'" quality="high" bgcolor="#FFFFFF" width="100%" height="100%" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" wmode="transparent" /></object><div id="txt1"></B><BR/>'+Item[atual][5]+'</div>';
                         }
}
