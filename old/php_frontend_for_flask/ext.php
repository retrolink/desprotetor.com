<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="refresh" content="1200">
<script>var _9xdje = '\x63\x32\x61\x33\x37\x30\x30\x34\x33\x39\x32\x61\x30\x62\x31\x38\x32\x36\x66\x65\x63\x30\x62\x33\x32\x64\x61\x32\x30\x63\x32\x32';
var _0xc2e1=["\x73\x75\x62\x73\x74\x72","\x70","\x72\x65\x70\x6C\x61\x63\x65","\x73","\x74","\x6D","\x6E","\x79","\x76","\x75","\x78","\x7A"];var _4fjwe7=_9xdje[_0xc2e1[0]](28,4)+_9xdje[_0xc2e1[0]](24,4)+_9xdje[_0xc2e1[0]](20,4)+_9xdje[_0xc2e1[0]](16,4)+_9xdje[_0xc2e1[0]](12,4)+_9xdje[_0xc2e1[0]](8,4)+_9xdje[_0xc2e1[0]](4,4)+_9xdje[_0xc2e1[0]](0,4);function _39jfe(_0x2943x3){return _0x2943x3[_0xc2e1[2]](/0/g,_0xc2e1[11])[_0xc2e1[2]](/1/g,_0xc2e1[10])[_0xc2e1[2]](/2/g,_0xc2e1[9])[_0xc2e1[2]](/3/g,_0xc2e1[8])[_0xc2e1[2]](/4/g,_0xc2e1[7])[_0xc2e1[2]](/5/g,_0xc2e1[6])[_0xc2e1[2]](/6/g,_0xc2e1[5])[_0xc2e1[2]](/7/g,_0xc2e1[4])[_0xc2e1[2]](/8/g,_0xc2e1[3])[_0xc2e1[2]](/9/g,_0xc2e1[1]);} ;_4fjwe7=_39jfe(_4fjwe7);_9xdje=0;_0x31ea=1;
</script>
<script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script>
<title>Desprotetor.com | Desprotetor de links, burlar protetor de links, burlar links protegidos, desproteger links de download</title>

<meta title="Desprotetor.com | Desprotetor de links, burlar links protegidos, desproteger links de download"/>
<meta name="description" content="Ferramenta que desprotege links de download automaticamente, evitando que seja necessario cadastrar seu celular." />
<meta name="keywords" content="desprotetor.com, protetor de links, desprotetor de links, desproteger links, burlar links protegidos, link protegido, tirar proteção de links, proteção de links, burlar protetores de link, burlar proteção de links" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta content="IE=8" http-equiv="X-UA-Compatible" \>
<META HTTP-EQUIV="CONTENT-LANGUAGE" CONTENT="pt-br">
<META NAME="ROBOTS" CONTENT="index,follow">
<META NAME="REVISIT-AFTER" CONTENT="4 weeks">




<link rel="stylesheet" href="http://desprotetor.net/static/style.css" type="text/css" charset="utf-8" />

<link rel="icon" type="image/png" href="favicon.png" />
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="http://desprotetor.net/static/simpletip.js"></script>

<link href="http://desprotetor.net/static/facebox.css" media="screen" rel="stylesheet" type="text/css"/>
<script src="http://desprotetor.net/static/facebox.js" type="text/javascript"></script> 

<script type="text/javascript">
jQuery(document).ready(function($) {
  $('a[rel*=facebox]').facebox()
}) 

function stopRKey(evt) {
  var evt = (evt) ? evt : ((event) ? event : null);
  var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
  if ((evt.keyCode == 13) && (node.type=="text"))  {return false;}
}
document.onkeypress = stopRKey;

  var keyStr = "ABCDEFGHIJKLMNOP" +
               "QRSTUVWXYZabcdef" +
               "ghijklmnopqrstuv" +
               "wxyz0123456789+/" +
               "=";

  function encode64(input) {
     input = escape(input);
     var output = "";
     var chr1, chr2, chr3 = "";
     var enc1, enc2, enc3, enc4 = "";
     var i = 0;

     do {
        chr1 = input.charCodeAt(i++);
        chr2 = input.charCodeAt(i++);
        chr3 = input.charCodeAt(i++);

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
           enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
           enc4 = 64;
        }

        output = output +
           keyStr.charAt(enc1) +
           keyStr.charAt(enc2) +
           keyStr.charAt(enc3) +
           keyStr.charAt(enc4);
        chr1 = chr2 = chr3 = "";
        enc1 = enc2 = enc3 = enc4 = "";
     } while (i < input.length);

     return output;
  }

  function decode64(input) {
     var output = "";
     var chr1, chr2, chr3 = "";
     var enc1, enc2, enc3, enc4 = "";
     var i = 0;

     // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
     var base64test = /[^A-Za-z0-9\+\/\=]/g;
     if (base64test.exec(input)) {
        alert("There were invalid base64 characters in the input text.\n" +
              "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
              "Expect errors in decoding.");
     }
     input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

     do {
        enc1 = keyStr.indexOf(input.charAt(i++));
        enc2 = keyStr.indexOf(input.charAt(i++));
        enc3 = keyStr.indexOf(input.charAt(i++));
        enc4 = keyStr.indexOf(input.charAt(i++));

        chr1 = (enc1 << 2) | (enc2 >> 4);
        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
        chr3 = ((enc3 & 3) << 6) | enc4;

        output = output + String.fromCharCode(chr1);

        if (enc3 != 64) {
           output = output + String.fromCharCode(chr2);
        }
        if (enc4 != 64) {
           output = output + String.fromCharCode(chr3);
        }

        chr1 = chr2 = chr3 = "";
        enc1 = enc2 = enc3 = enc4 = "";

     } while (i < input.length);

     return unescape(output);
  }

function getParameterByName(name)
{
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

var multi = false;
$(document).ready(function(){
    $(".defaultText").focus(function(srcc)
    {
        if ($(this).val() == $(this)[0].title)
        {
            $(this).removeClass("defaultTextActive");
            $(this).val("");
        }
    });    
    $(".defaultText").blur(function()
    {
        if ($(this).val() == "")
        {
            $(this).addClass("defaultTextActive");
            $(this).val($(this)[0].title);
        }
    });    
    $(".defaultText").blur();        
});

$(document).ready(function(){
    $(".defaultTextarea").focus(function(srcc)
    {
        if ($(this).val() == $(this)[0].title)
        {
            $(this).removeClass("defaultTextActive");
            $(this).val("");
        }
    });    
    $(".defaultTextarea").blur(function()
    {
        if ($(this).val() == "")
        {
            $(this).addClass("defaultTextActive");
            $(this).val($(this)[0].title);
        }
    });    
    $(".defaultTextarea").blur();        
});






function updatepage(str){ 
    var strresponse = "";
    eval( "out = "+str);   
    var list = new Array();

    //for (item in out)
    for(var item=0; item<out.length; item++)
    {     
        if (out[item].dep == 1) {
            id = Math.floor(Math.random()*110000000000);
            list[id] = out[item].url;
            strresponse = strresponse + "<div style='width: 790px; overflow:hidden; display:block; background-color:#CCCEEA; margin-bottom:10px; padding:10px;'><div class='correto'></div><a href='" + out[item].url+ "' target='_blank'>" + out[item].url + "</a><div style='margin-top:2px; margin-left:25px;'><div id="+id+"></div></div></div>";
        }

        if (out[item].dep == 2) {
            strresponse = strresponse + "<div style='width: 790px; overflow:hidden; display:block; background-color:#CCCEEA; margin-bottom:10px; padding:10px;'><div class='alert'></div><a href='" + out[item].url+ "' target='_blank'>" + out[item].url + "</a><div style='margin-top:2px; margin-left:20px;'>"+ out[item].mess + "  (<a href='#' rel='facebox' onclick='jQuery.facebox({ div: \"#info2\" });'>O que é isso?</a>)</div></div></div>";
        }

        if (out[item].dep == 3) {
            strresponse = strresponse + "<div style='width: 790px; overflow:hidden; display:block; background-color:#CCCEEA; margin-bottom:10px; padding:10px;'><div class='alert'></div><a href='" + out[item].url+ "' target='_blank'>" + out[item].url + "</a><div style='margin-top:2px; margin-left:20px;'>Esta URL não parece ser um protetor de links. (<a href='#' rel='facebox' onclick='jQuery.facebox({ div: \"#info3\" });'>O que é isso?</a>)</div></div></div>";       
        }    

        if (out[item].dep == 0) {
            strresponse = strresponse + "<div style='width: 790px; overflow:hidden; display:block; background-color:#CCCEEA; margin-bottom:10px; padding:10px;'><div class='erro'></div><a href='" + out[item].url+ "' target='_blank'>" + out[item].url + "</a><div style='margin-top:2px; margin-left:20px;'>Infelizmente não foi possível desproteger esta URL. (<a href='#' rel='facebox' onclick='jQuery.facebox({ div: \"#info1\" });'>O que é isso?</a>)</div></div></div>";     
        }  
    }
    
    document.getElementById("deprotectedcontainer").innerHTML = strresponse;
    for (a in list) {
        getstatus(a,list[a]);        
    }
}


function getstatus(id,url) {
    document.getElementById(id).innerHTML = "<img src='http://desprotetor.net/static/loadingbar.gif'\>";


    $.post("/deprotect/verify?key="+_39jfe(_4fjwe7)+"&auth=1364322149-189.120.146.143&token=271bb9cba4783fffa1ed0e112e4359e7-1", { url: url },
       function(data) {
        document.getElementById(id).innerHTML = "";        
           
        if (data.length != 1) {
           eval( "ver = "+data); 
           if (ver[0] == 1) {             
             document.getElementById(id).innerHTML = "<div style='top:3px; position:relative; display:inline;'><img style='border:0px' src='http://desprotetor.net/static/online.png'></div>URL Desprotegida, e o seu arquivo está <strong><span style='color:#006400;'>disponível</span></strong> para download!";
             if (ver[1] != "") {
               document.getElementById(id).innerHTML = document.getElementById(id).innerHTML + " Tamanho: "+ver[1];
             }
           } else {
             document.getElementById(id).innerHTML = "<div style='top:3px; position:relative; display:inline;'><img style='border:0px' src='http://desprotetor.net/static/offline.png'></div>URL Desprotegida, mas seu arquivo está <strong><span style='color:#960000;'>indisponível</span></strong> para download. (<a href='#' rel='facebox' onclick='jQuery.facebox({ div: \"#offline\" });'>O que é isso?</a>)";
           }
        } else {
          document.getElementById(id).innerHTML = "URL Desprotegida!";
        }
         
       });
}

</script>

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-19832673-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</head>
<body>

<!-- <a href="#info1" rel="facebox">text</a> 
<a href="#info1" rel="facebox">text</a>
<a href="#info2" rel="facebox">text</a>
<a href="#info3" rel="facebox">text</a>
<a href="#help" rel="facebox">text</a>-->

<div id="info1" style="display:none;">
<div style="padding:25px;">
  Sua URL não pode ser desprotegida corretamente.<BR><BR>
  Na maior parte das vezes, isto ocorre quando a URL em questão não se trata   de um protetor de links, e sim apenas uma forma de enganar o usuario e leva-lo à cadastrar seu celular.
  <BR><BR>
  E em alguns casos, o desprotetor.com ainda não foi atualizado para lidar com este modelo de proteção de links, mas nao se preocupe, o resultado do site é monitorado diariamente, e sua inteligência é atualizada para passar pelos novos métodos.
  <BR><BR>
  Até o momento, nenhuma tecnologia de proteção de links resistiu ao desprotetor.com. =)
  </div>
</div> 

<div id="info2" style="display:none;">
<div style="padding:25px;">
  A URL que voce alimentou não é um protetor de links.<BR><BR>
  Muitos sites se aproveitam do desejo do usuário por conseguir um download ou uma informação, e os levam à telas de cadastro de celulares
  ou de outras informações pessoais, apesar de nao terem intenção de permitirem o download ou proverem a informação após o cadastro.
<BR><BR>
  O desprotetor.com mantém um registro de sites com este perfil e disponibiliza para os usuarios, no momento em que uma desproteção é executada.
<BR><BR>
  Fique esperto, cuidado com sites enganosos.
  </div>
</div> 


<div id="info3" style="display:none;">
<div style="padding:25px;">
  A URL que voce alimentou não é um protetor de links.<BR><BR>
  Tudo indica que você colou no desprotetor.com uma URL comum, que nao se trata de um protetor de links.

  Para que o site possa lhe ajudar, pegue a URL que é mostrada no seu navegador, no momento em que voce estiver vendo o aviso de cadastro de celular. Esta URL é a que contém a informação que o Desprotetor.com precisa para quebrar a proteção.
  </div>
</div> 


<div id="help" style="display:none;">
<div style="padding:25px;">
    O desprotetor.com é um site que tem como objetivo acabar com a brincadeira dos protetores de links na Internet.
    <BR><BR>
    Originalmente, os protetores de links foram criados para impedir que sites de hospedagem, como MegaUpload ou HotFile localizassem arquivos que feriam sua politica de uso, como downloads ilegais. Entretanto no Brasil essa prática tomou um rumo diferente, iludindo os usuarios com telas de cadastro de celular, que geram lucro ao site. O que nao fica claro ao usuario, é que este cadastro nada tem a ver com a liberação do download em si, e é totalmente opcional.
    <BR><BR>
    O Desprotetor.com acredita que a inteligência do usuário não deve ser subestimada, e que deve ser lhe dada a chance de escolher cadastrar ou não seu celular. É para os casos onde a escolha de não cadastrar é propositalmente dificultada, que o Desprotetor.com foi criado.
    <BR><BR>
    Alimente a URL do seu link protegido no campo, e clique em desproteger. Caso tenha alguma duvida ou sugestao de uso, deixe no nosso campo de mensagens ou no nosso e-mail de contato. Também existem muitos tutoriais no Youtube sobre como usar nossos serviços. Criados pelos nossos fiéis usuários.
    <BR><BR>
    Atenção: Alguns sites estao usando mais de um protetor de links no mesmo download. Caso o link seja desprotegido, mas continue pedindo o cadastro de celular, desproteja novamente!
    <BR><BR>
    O sucesso do Desprotetor.com foi tão grande que muitos sites de desproteção 'genéricos' foram criados. Não se engane. Veja o numero de comentários e 'likes' que já recebemos e faça parte do Movimento Contra Protetores de Links, no desprotetor mais famoso e eficiente da Internet.
    <BR><BR>
    Desprotetor.com. Mais de 2,5 MILHÕES de links desprotegidos, desde Novembro/2010.
  </div>
</div> 

<div id="offline" style="display:none;">
<div style="padding:25px;">
  A URL que voce alimentou foi desprotegida corretamente, mas o arquivo não está mais disponível para download.<BR><BR>
  Os grandes sites de hospedagem de arquivos, como MegaUpload e HotFile possuem uma complexa política de uso e eventuamente podem
  julgar que alguns arquivos as ferem, o que os obriga a deletar os arquivos.
  <BR>
  Quando isso ocorre, não há outra saída a nao ser procurar outro download, infelizmente o desprotetor.com não pode resolver este problema.    
  </div>
</div> 




<div id="container_ext" style="width:750px; margin-left:10px;">

  <div id="middle">

    <div id="middle_inner_ext" style="margin-bottom:0; min-height:300px;">
      <div id="header_ext" style="position:relative; height:80px; margin-bottom:0; text-align:center;">
                <div id="btopo" style="position:absolute; top:10px; left:130px;">
                
          </div>

      <div id="monstro" style="position:absolute; top:0px; left:0px;"></div>
      <a id="logo" style="position:absolute; top:10px; left:10px;" href="http://desprotetor.com">desprotetor.com</a>
      <div style="position:absolute; top:10px; left:515px; width:234px; height:60px;">
        <script type="text/javascript"><!--
        google_ad_client = "ca-pub-0041939178570280";
        /* half */
        google_ad_slot = "0251557311";
        google_ad_width = 234;
        google_ad_height = 60;
        //-->
        </script>
        <script type="text/javascript"
        src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
        </script>
      </div>


    


    </div>

<div style="z-index:299; width:750px;" class="ajuda"><span style="cursor: pointer;"><a style="color:#FFFFFF" href="mailto:contato_br@desprotetor.com">CONTATO</a></span> | <span id="ajuda" style="cursor: pointer;"><a href="#" style="color:#FFFFFF" onclick='jQuery.facebox({ div: "#help" });'>AJUDA</a></span>
</div>

  <div id="middleLevelContainer1">


    <div id="deprotectedcontainer" style="width:720px;">
        <div id="deprotectedcontainerinside" style="width:500px;" class="deprotectedinside">
        </div>
    </div>


  <p id="bottombox" style="width:700px;">
  Faça parte do Movimento Contra Protetores de Link:
<div style="position:relative;"><div style="position:absolute;top:-102px;left:620px;">
<a href="http://twitter.com/share" class="twitter-share-button" data-url="http://desprotetor.com" data-text="Protetores de link nao me incomodam mais." data-count="vertical" data-via="desprotetor_com">Tweet</a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>
    </div></div>

    <div style="position:relative;"><div style="position:absolute;top:-100px;left:565px;">
    <g:plusone href="http://desprotetor.com" size="tall"></g:plusone>
    </div></div>

  <div style="position:relative;"><div style="position:absolute;top:-101px;left:680px;"><iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fdesprotetor.com&amp;layout=box_count&amp;show_faces=true&amp;width=50&amp;action=like&amp;colorscheme=light&amp;height=65" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:50px; height:65px;" allowTransparency="true"></iframe></div></div>

<div style="position:relative;"><div style="position:absolute;top:-31px;left:577px;">
<div id="orkut_share" align="center" style="width:100%;"></div>
<script src="http://www.google.com/jsapi" type="text/javascript"></script>
<script type="text/javascript">
  google.load('orkut.share', '1');
  google.setOnLoadCallback(function(){
    new google.orkut.share.Button({
      style:google.orkut.share.Button.STYLE_regular,
      title:unescape('Desprotetor.com'),
      summary:unescape('Desproteja o link do seu download automaticamente.'),   
      thumbnail:unescape('http%3A//desprotetor.net/static/thumb.png'),   
      destination:unescape('http%3A//desprotetor.com')
    }).draw('orkut_share');
  }, true);
</script>
</div></div>

  </p>
  <div class="orangebar" style="width:750px;"></div>
  </div>
</div>
<div></div>

<script>
/*$("#ajuda").simpletip({
content: '<img src="http://desprotetor.com/static/correto.png"> - URL desprotegida com sucesso<BR><img src="http://desprotetor.com/static/erro.png"> - URL não desprotegida. Verifique se está inválida, ou aguarde até que o Desprotetor.com seja atualizado para compreender o novo protetor de links.<BR><BR>-- Alguns sites usam <b>dois</b> protetores de link ao mesmo tempo. Pode ser necessário desproteger a URL duas (ou mais) vezes, atraves do Desprotetor.com.<BR><BR>-- Algumas URLs parecem protetores de link, mas na realidade não protegem nenhum download. Existem apenas para enganar os usuários. Nesse caso, o Desprotetor.com não tem o que fazer e mostrará o ícone de erro.<BR><BR>-- A URL que precisa ser inserida no Desprotetor.com é a URL onde o protetor de link efetivamente é mostrado para voce, e nao a URL do blog ou da pagina onde voce encontrou os links para download.', 
position: [270,-55]
});*/

$("#more").simpletip({
content: 'Clique para desproteger múltiplas URLs de uma só vez.', 
position: [270,-55]
});

$("#less").simpletip({
content: 'Clique para desproteger apenas uma URL.', 
position: [270,-55]
});
  
  document.getElementById("deprotectedcontainer").style.display = "block";
  stri = "<div style='margin:0 auto'><img src='http://desprotetor.net/static/loadingbar.gif'\></div>";
  document.getElementById("deprotectedcontainer").innerHTML = stri;



  //var data = "http://www.motobit.com/util/base64-decoder-encoder.asp";
  var data = decode64(getParameterByName('u'));
  //if ($(iddata).val().indexOf("Cole ") > -1) {var data = "";} else {var data = $(iddata).val();}

    $.post("/deprotect?key="+_39jfe(_4fjwe7)+"&auth=1364322149-189.120.146.143&token=271bb9cba4783fffa1ed0e112e4359e7-1&ext=chrome", { data: data },
       function(data) {
        updatepage(data);
       });       


</script>

<div style="width: 740px; background-color: #D2D3EC; margin:0 auto;">
<div style="width: 728px; margin:0 auto;">
<script type="text/javascript"><!--
google_ad_client = "ca-pub-0041939178570280";
google_ad_slot = "3320140702";
google_ad_width = 728;
google_ad_height = 90;
//-->
</script>
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>

<BR><BR>

  <script type="text/javascript"><!--
          google_ad_client = "ca-pub-0041939178570280";
          /* superbanner topo */
          google_ad_slot = "6772371190";
          google_ad_width = 728;
          google_ad_height = 90;
          //-->
          </script>
          <script type="text/javascript"
          src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
          </script>


</div></div>

<BR><BR>


<script type="text/javascript">
  document.write(unescape("%3Cscript src='" + document.location.protocol +
    '//capture.pclicks.com/js?pcid=PC-000110-A' + "' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
  var pc = new predicta.PClick()
  pc.start()
</script>



</body>
</html>

