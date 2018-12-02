const marker = document.getElementById('ProgressMarker');
let ready = false;
const fileTitle = document.getElementById("fileTitle");
const fileArtist = document.getElementById("fileArtist");

function defaultList() {
    Amplitude.init({
        "callbacks": {
            'time_update': function () {
                let songPlayedPercentage = Amplitude.getSongPlayedPercentage();
                marker.style.left = (songPlayedPercentage * 3) + 'px';
                this.handleText();
            },
            'song_change': function(){
                fileTitle.textContent=Amplitude.getActiveSongMetadata().name;
                fileArtist.textContent=Amplitude.getActiveSongMetadata().artist;
                this.handleText();
                console.log('oh hj');
            },
        },
        "songs": [

        ]
        // "default_album_art": "./cover.png",

    });
};



defaultList();
Amplitude.setDefaultAlbumArt('./cover.png' );
maxLen = Amplitude.getSongs().length;
mainList = Amplitude.getSongs();
console.log(mainList);
playbutton = document.getElementById("play-pause");
playbutton.addEventListener("click", play);
// document.getElementById("next").addEventListener("click", next);
// document.getElementById("prev").addEventListener("click", prev);
shufflebutton = document.getElementById("shuffle");
shufflebutton.addEventListener("click", shuffle);
playlistType = document.getElementById('ListOptions');
playListValue = document.getElementById('ListValues');
sethandlers();
let playing = 0;
let shuffleval = 0;
uniArtists = [];
uniAlbums = [];
uniGenres = [];
ready=true;

function getUniques() {
    for(var i=0;i<mainList.length;i++){
        var obj = mainList[i];
        art = obj.artist;
        alb = obj.album;
        if(!uniArtists.includes(art)){
            uniArtists.push(art)
        }
        if(!uniAlbums.includes(alb)){
            uniAlbums.push(alb)
        }

    }
}
getUniques();
console.log(uniArtists);



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

function getList(option, value){
    songlist = Amplitude.getSongs()

}

function next(){
    if(playing===1){
        Amplitude.next()
    }
    else {
        Amplitude.next();
        Amplitude.pause()
    }
    window.requestAnimationFrame(updateInfo);
}

function prev(){
    if(playing===1){
        Amplitude.prev()
    }
    else {
        Amplitude.prev();
        Amplitude.pause()
    }
    window.requestAnimationFrame(updateInfo);
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
// console.log(maxLen);
function updateInfo(){
    if(!ready){
        return;
    }
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

    fileTitle.textContent=Amplitude.getActiveSongMetadata().name;
    fileArtist.textContent=Amplitude.getActiveSongMetadata().artist;
    handleText();
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
    document.getElementById("ProgressBack").addEventListener("click", songAdjust);
    shufflebutton.addEventListener("click", shuffle);
    document.getElementById('LoadList').addEventListener("click", loadList);
    playlistType.addEventListener("change", loadListValues);
    // playlistValue.addEventListener("change", myScript);
}


function getDex(value){
    if(value>=maxLen){
        return getDex(value-maxLen);
    }
    else{
        return value;
    }

}

function songAdjust(event){
    var offset = this.getBoundingClientRect();
    console.log(offset)
    var x = event.pageX - offset.left;
    console.log(x)

    Amplitude.setSongPlayedPercentage( ( parseFloat( x ) / parseFloat( this.offsetWidth) ) * 100 );
    songPlayedPercentage = Amplitude.getSongPlayedPercentage();
    marker.style.left = songPlayedPercentage * 300;

}

function handleText(){
    if(isElementOverflowing(fileTitle)){
        wrapContentsInMarquee(fileTitle, Amplitude.getSongByIndex(getDex(val)).name);
    }

    if(isElementOverflowing(fileArtist)){
        wrapContentsInMarquee(fileArtist, Amplitude.getSongByIndex(getDex(val)).name);
    }
}

function wrapContentsInMarquee(element, contents) {
    var marquee = document.createElement('marquee');


    marquee.innerText = contents;
    element.innerHTML = '';
    element.appendChild(marquee);
}


function isElementOverflowing(element) {
    var overflowX = element.offsetWidth < element.scrollWidth,
        overflowY = element.offsetHeight < element.scrollHeight;

    return (overflowX || overflowY);
}

function loadListValues(){
    value = playlistType.selectedIndex;
    playListValue.options.length = 0;
    switch (value){
        case 0:
            let option = document.createElement("option");
            option.text = "Default";
            playListValue.add(option);
            break;
        case 1:
            for(let i=0;i<uniArtists.length;i++) {
                let option = document.createElement("option");
                option.text = uniArtists[i];
                playListValue.add(option);
            }
                break;
        case 2:
            for(let i=0;i<uniAlbums.length;i++) {
                let option = document.createElement("option");
                option.text = uniAlbums[i];
                playListValue.add(option);
            }
            break;
    }
}

function loadList(){
    //GET PLAYLIST OPTIONS
    Amplitude.pause();
    playing=0;
    playbutton.style.background= 'url(./images/play.png)';
    option = playlistType.selectedIndex;
    value = playListValue.options[playListValue.selectedIndex].text;
    if(option===0){
        Amplitude.init({
            "callbacks": {
                'time_update': function () {
                    let songPlayedPercentage = Amplitude.getSongPlayedPercentage();
                    marker.style.left = (songPlayedPercentage * 3) + 'px';
                }
            }, 'songs': mainList,
        });
        maxLen = Amplitude.getSongs().length;
        return;
    }
    if(option===1){
        onPlayList('artist', value);
        return;
    }

    if(option===2){
        onPlayList('album', value);
    }

}

function onPlayList(option, value){
    newList=[];
    for(var i=0;i<mainList.length;i++){
        var obj = mainList[i];
        if(option==='artist') {
            if (obj.artist===value){
                newList.push(obj);
            }
        }

        else{
            if(obj.album===value){
                newList.push(obj);
            }
        }
    }

    Amplitude.init({
        "callbacks": {
            'time_update': function () {
                let songPlayedPercentage = Amplitude.getSongPlayedPercentage();
                marker.style.left = (songPlayedPercentage * 3) + 'px';
            }
        }, 'songs': newList,
    });
    maxLen = Amplitude.getSongs().length;
    Amplitude.setRepeat();
    window.requestAnimationFrame(updateInfo);

};

