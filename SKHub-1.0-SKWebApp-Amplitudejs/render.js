Amplitude.init({
    "songs": [

    ],
    // "default_album_art": "./cover.png",

});
Amplitude.setDefaultAlbumArt('./cover.png' );
maxLen = Amplitude.getSongs().length;
const fileTitle = document.getElementById("fileTitle");
const fileArtist = document.getElementById("fileArtist");
playbutton = document.getElementById("play-pause");
playbutton.addEventListener("click", play);
document.getElementById("next").addEventListener("click", next);
document.getElementById("prev").addEventListener("click", prev);
shufflebutton = document.getElementById("shuffle");
shufflebutton.addEventListener("click", shuffle);
sethandlers();

let playing = 0;
let shuffleval = 0;


function play(){
    if(playing===0){
        Amplitude.play();
        playbutton.style.background= 'url(./images/pause.png)';
        playing=1;
    }
    else{
        Amplitude.pause();
        playbutton.style.background= 'url(./images/play.png)';
        playing=0;
    }
}

function next(){
    Amplitude.next()
}

function prev(){
    Amplitude.prev()
}

function shuffle(){
    if(shuffleval===0) {
        Amplitude.setShuffle();
        shufflebutton.style.background = 'url(images/shuffleon.png)';
        shuffleval = 1;
    }

    else{
        Amplitude.setShuffle();
        shufflebutton.style.background = 'url(images/shuffle.png)';
        shuffleval=0;
    }
}

updateInfo();
console.log(maxLen);
function updateInfo(){
    val = Amplitude.getActiveIndex();
    let playlist = Amplitude.getActivePlaylist();
    document.getElementById("playdex1").textContent=Amplitude.getSongByIndex(getDex(val+1)).name;
    document.getElementById("artdex1").textContent=Amplitude.getSongByIndex(getDex(val+1)).artist;
    document.getElementById("playdex2").textContent=Amplitude.getSongByIndex(getDex(val+2)).name;
    document.getElementById("artdex2").textContent=Amplitude.getSongByIndex(getDex(val+2)).artist;
    document.getElementById("playdex3").textContent=Amplitude.getSongByIndex(getDex(val+3)).name;
    document.getElementById("artdex3").textContent=Amplitude.getSongByIndex(getDex(val+3)).artist;
    document.getElementById("playdex4").textContent=Amplitude.getSongByIndex(getDex(val+4)).name;
    document.getElementById("artdex4").textContent=Amplitude.getSongByIndex(getDex(val+4)).artist;
    document.getElementById("playdex5").textContent=Amplitude.getSongByIndex(getDex(val+5)).name;
    document.getElementById("artdex5").textContent=Amplitude.getSongByIndex(getDex(val+5)).artist;

    fileTitle.textContent=Amplitude.getSongByIndex(getDex(val)).name;
    fileArtist.textContent=Amplitude.getSongByIndex(getDex(val)).artist;
    window.requestAnimationFrame(updateInfo);

}

function sethandlers(){
    window.addEventListener('keydown', event => {
        var key = event.keyCode;
        switch (key) {
            case 32:
                play();
                break;
            case 39:
                next();
                break;
            case 37:
                prev();
                break;
        }
    });

    playbutton.addEventListener("click", play);
    document.getElementById("next").addEventListener("click", next);
    document.getElementById("prev").addEventListener("click", prev);
    shufflebutton.addEventListener("click", shuffle);
}
function getDex(value){
    if(value>=maxLen){
        return value-maxLen;
    }
    else{
        return value;
    }

}
