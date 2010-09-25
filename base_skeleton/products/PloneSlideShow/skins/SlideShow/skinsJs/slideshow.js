var d=document;

$ = function(id) {
                 if(!arguments[1]) return document.getElementById(id);
                 else document.getElementById(id).style[arguments[1]] = arguments[2];
}


function delItem(arr,item){
                           for(;item<arr.length;item++) arr[item]=arr[item + 1];arr.length=arr.length-1;
}

function startSlide(){
                      loadImages();
                      timeoutId = setTimeout('changeImg(1)', 3000);
}

function initialize(){
                      timeoutId = 0;
                      textareaContent = d.tv_home.select_tv_home.value.split(/[\r\n]/i);
                      Item = new Array();

                      for(x=0,y=0;x<textareaContent.length;x++){
                          if(textareaContent[x].length>30) Item[y++] = textareaContent[x].split('|');
                      }

                      for(i=Item.length-1;i>=0;i--){Item[i][0]=Item[i][0].replace(/([ \n\t\r])+/, " ");
                          Item[i][4]=(Item[i][4].length<3) ? '' : '<img src="cleardot.gif" border="0" hspace="2" align="absmiddle" style="margin-left:2px">';
                          if(Item[i][1].length<1||Item[i][3].length<1||Item[i][2].length<1||Item[i][0].length<1) delItem(Item,i);
                      }

                      if(Item.length==1) d.write('<style>#anterior,#proximo{visibility:hidden;}</style>');
                      atual = Math.random().toString().substring(2,6) % Item.length;
}

function startPanel(){usaCredito = '';
                      initialize();
                      if(arguments.length>0){
                                             if(!isNaN(arguments[0])) atual = arguments[0];
                      }



                      var usaCredito = '';
                      usaCredito += '<div id="credito">'+Item[atual][0]+'</div>';
                      var caminhoGenerico = '';
                      caminhoGenerico += '<div id="imgSL">';
                      caminhoGenerico += '<a href="'+Item[atual][3]+'" target="_parent" id="chamadaImagem"><img src="'+Item[atual][1]+'" id="imgslide" name="img1" border="0"></a>';
                      caminhoGenerico += '</div>';
                      d.write('<div id="to-blend">'+usaCredito+caminhoGenerico);
                      d.write('<h2 align="center"><div id="chamadaLinks"><a href="'+Item[atual][3]+'" id="p-link" target="_parent"><div id="txt1"><span class="title">'+Item[atual][2]+'</span><BR/>'+Item[atual][5]+'</div></a></div></h2></div>');
}var okToGo=false;onload=startSlide;
