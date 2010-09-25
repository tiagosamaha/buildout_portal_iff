// JavaScript Document
var w = 'None';

function PopUpController(url,name){
    if (w == 'None') {Open(url,name);}
    else {Close();}
}
function Open(url,name) {
   w=window.open(url,name,
   "width=200,height=200,top=20,left=600,status=no,directories=no,resizable=no,location=no,menubar=no,status=no,scrollbars=no");
}

function Close() {
    w.close();
    w = 'None';
}






