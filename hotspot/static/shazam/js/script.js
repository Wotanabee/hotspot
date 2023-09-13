function monAdresseIP()
{
 var ip = false;
 if (window.XMLHttpRequest) xmlhttp = new XMLHttpRequest();
 else xmlhttp = new ActiveXObject(Microsoft.XMLHTTP);
 xmlhttp.open(GET,http://192.168.100.124:8800/shazam/,false);
 xmlhttp.send();
 var reponse = JSON.Parse(xmlhttp.responseText);
 //On suppose que l'adresse IP est stockée avec la clé ip. Regardez les exemples fournis par les services pour savoir quelle clé correspond à l'adresse IP
 if (reponse[ip])
 ip = reponse[ip]
 return ip;
}