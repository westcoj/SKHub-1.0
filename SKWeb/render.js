const marker = document.getElementById('ProgressMarker');
let ready = false;
const fileTitle = document.getElementById("fileTitle");
const fileArtist = document.getElementById("fileArtist");
bufferedBar = document.getElementById('ProgressBuff');

mainList = [

];


function defaultList() {
    Amplitude.init({
        "callbacks": {
            'time_update': function () {
                let songPlayedPercentage = Amplitude.getSongPlayedPercentage();
                marker.style.left = (songPlayedPercentage * 3) + 'px';
                this.handleText();

                let songBufferedPercentage = Amplitude.getBuffered();
                bufferedBar.style.paddingRight = (songBufferedPercentage * 3) + 'px';
            },
            'song_change': function(){
                fileTitle.textContent=Amplitude.getActiveSongMetadata().name;
                fileArtist.textContent=Amplitude.getActiveSongMetadata().artist;
                this.handleText();
                console.log('oh hj');
            },
        },
        "songs": [
            {
                "name": "Monument of Non-Existence (Kefka Palazzo - Final Fantasy VI)",
                "artist": "Lashmush",
                "album": "BadAss: Boss Themes: Volume 2",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-01 Lashmush - Monument of Non-Existence (Kefka Palazzo - Final Fantasy VI).mp3",
                "keydex": "0"
            },
            {
                "name": "Zeromus Sum Game (Zeromus - Final Fantasy IV)",
                "artist": "Sbeast",
                "album": "BadAss: Boss Themes: Volume 3",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-02 Sbeast - Zeromus Sum Game (Zeromus - Final Fantasy IV).mp3",
                "keydex": "1"
            },
            {
                "name": "Darksightedness (Dark Bowser - Mario & Luigi: Bowser's Inside Story)",
                "artist": "Kammo64",
                "album": "BadAss: Boss Themes: Volume 2",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-03 Kammo64 - Darksightedness (Dark Bowser - Mario & Luigi - Bowser's Inside Story).mp3",
                "keydex": "2"
            },
            {
                "name": "The Metal Emperor (Machinedramon - Digimon World)",
                "artist": "Chernabogue",
                "album": "BadAss: Boss Themes: Volume 1",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-04 Chernabogue, AngelCityOutlaw, Furilas - The Metal Emperor (Machinedramon - Digimon World).mp3",
                "keydex": "3"
            },
            {
                "name": "Warriors of Shredder (Slash - Teenage Mutant Ninja Turtles III)",
                "artist": "Lashmush",
                "album": "BadAss: Boss Themes: Volume 2",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-05 Gamer Shredding - Warriors of Shredder (Slash - Teenage Mutant Ninja Turtles III).mp3",
                "keydex": "4"
            },
            {
                "name": "Jaded by Death (Deathevan - Breath of Fire II)",
                "artist": "HoboKa",
                "album": "BadAss: Boss Themes: Volume 1",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-06 HoboKa - Jaded by Death (Deathevan - Breath of Fire II).mp3",
                "keydex": "5"
            },
            {
                "name": "Crescendo to Chaos (Rival - Pokémon Red Version)",
                "artist": "Chernabogue",
                "album": "BadAss: Boss Themes: Volume 1",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-07 Chernabogue - Crescendo to Chaos (Rival - Pokemon Red Version).mp3",
                "keydex": "6"
            },
            {
                "name": "The Power (Grahf - Xenogears)",
                "artist": "Sbeast",
                "album": "BadAss: Boss Themes: Volume 3",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-08 XPRTNovice - The Power (Grahf - Xenogears).mp3",
                "keydex": "7"
            },
            {
                "name": "Amputate Your Metal (Big Bertha - Wild Guns)",
                "artist": "Kammo64",
                "album": "BadAss: Boss Themes: Volume 2",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-09 Mak Eightman - Amputate Your Metal (Big Bertha - Wild Guns).mp3",
                "keydex": "8"
            },
            {
                "name": "Are You BadAss? (Sturm - Advance Wars)",
                "artist": "Chernabogue",
                "album": "BadAss: Boss Themes: Volume 1",
                "url": "./songs/BadAss - Boss Themes - Volume III/1-10 Chernabogue, Tuberz McGee, Furilas, Mirby, Brandon Strader - Are You BadAss (Sturm - Advance Wars).mp3",
                "keydex": "9"
            },
            {
                "name": "Opening the Way (Colossi - Shadow of the Colossus)",
                "artist": "Lashmush",
                "album": "BadAss: Boss Themes: Volume 2",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-01 Pablo Coma - Opening the Way (Colossi - Shadow of the Colossus).mp3",
                "keydex": "10"
            },
            {
                "name": "The Dark Defender (Magus - Chrono Trigger)",
                "artist": "Sbeast",
                "album": "BadAss: Boss Themes: Volume 3",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-02 pu_freak - The Dark Defender (Magus - Chrono Trigger).mp3",
                "keydex": "11"
            },
            {
                "name": "(Progeny) Of a Frail Humanity (Albert Wesker - Resident Evil series)",
                "artist": "HoboKa",
                "album": "BadAss: Boss Themes: Volume 1",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-03 David L. Puga, Mak Eightman - (Progeny) Of a Frail Humanity (Albert Wesker - Resident Evil series).mp3",
                "keydex": "12"
            },
            {
                "name": "Fortress of Doom (Koopalings - Super Mario World)",
                "artist": "Kammo64",
                "album": "BadAss: Boss Themes: Volume 2",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-04 neshead80 - Fortress of Doom (Koopalings - Super Mario World).mp3",
                "keydex": "13"
            },
            {
                "name": "Molgera's Love (Molgera - Legend of Zelda: The Wind Waker)",
                "artist": "HoboKa",
                "album": "BadAss: Boss Themes: Volume 1",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-05 Chimpazilla, Redg - Molgera's Love (Molgera - Legend of Zelda - The Wind Waker).mp3",
                "keydex": "14"
            },
            {
                "name": "Mad Jack's Drop (Mad Jack - Donkey Kong 64)",
                "artist": "Kammo64",
                "album": "BadAss: Boss Themes: Volume 2",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-06 Kammo64 - Mad Jack's Drop (Mad Jack - Donkey Kong 64).mp3",
                "keydex": "15"
            },
            {
                "name": "Twisted Rebirth (Dark Samus - Metroid Prime series)",
                "artist": "Sbeast",
                "album": "BadAss: Boss Themes: Volume 3",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-07 SkyRiderX feat. XPRTNovice - Twisted Rebirth (Dark Samus - Metroid Prime series).mp3",
                "keydex": "16"
            },
            {
                "name": "Soiled by the Egyptians (Orbot Purple - Vectorman series)",
                "artist": "Sbeast",
                "album": "BadAss: Boss Themes: Volume 3",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-08 timaeus222 - Soiled by the Egyptians (Orbot Purple - Vectorman series).mp3",
                "keydex": "17"
            },
            {
                "name": "Become Death (Metalhead - Vectorman)",
                "artist": "HoboKa",
                "album": "BadAss: Boss Themes: Volume 1",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-09 Darkmoocher, timaeus222 - Become Death (Metalhead - Vectorman).mp3",
                "keydex": "18"
            },
            {
                "name": "Seed of Perdition (Lavos - Chrono Trigger)",
                "artist": "Lashmush",
                "album": "BadAss: Boss Themes: Volume 2",
                "url": "./songs/BadAss - Boss Themes - Volume III/2-10 Lashmush - Seed of Perdition (Lavos - Chrono Trigger).mp3",
                "keydex": "19"
            },
            {
                "name": "Heaven Rd. 2",
                "artist": "EnV",
                "album": "EnV 2016",
                "url": "./songs/ENV/105753_Heaven_remix.mp3",
                "keydex": "20"
            },
            {
                "name": "FireFrost",
                "artist": "EnV",
                "album": "EnV 2016",
                "url": "./songs/ENV/498830_EnV---FireFrost.mp3",
                "keydex": "21"
            },
            {
                "name": "RPM",
                "artist": "EnV",
                "album": "EnV 2016",
                "url": "./songs/ENV/509762_EnV---RPM.mp3",
                "keydex": "22"
            },
            {
                "name": "Uprise",
                "artist": "EnV",
                "album": "EnV 2016",
                "url": "./songs/ENV/513064_EnV---Uprise.mp3",
                "keydex": "23"
            },
            {
                "name": "Pneumatic-Tok",
                "artist": "EnV",
                "album": "EnV 2016",
                "url": "./songs/ENV/516336_EnV---Pneumatic-Tok.mp3",
                "keydex": "24"
            },
            {
                "name": "Sanctuary",
                "artist": "EnV",
                "album": "EnV 2016",
                "url": "./songs/ENV/521252_EnV---Sanctuary.mp3",
                "keydex": "25"
            },
            {
                "name": "Green-With-Me",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/525196_EnV---Green-With-Me.mp3",
                "keydex": "26"
            },
            {
                "name": "Valiant",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/527560_EnV---Valiant.mp3",
                "keydex": "27"
            },
            {
                "name": "BloomRadio-Ed",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/532991_EnV---BloomRadio-Ed.mp3",
                "keydex": "28"
            },
            {
                "name": "Wakkawakka-Rem",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/534977_Envy-Wakkawakka-Rem.mp3",
                "keydex": "29"
            },
            {
                "name": "Sanctuary (Dylnmatrix Remix)",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/535710_EnV-Sanctuary-DM-Re.mp3",
                "keydex": "30"
            },
            {
                "name": "Vee",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/538354_EnV---Vee.mp3",
                "keydex": "31"
            },
            {
                "name": "Paladin",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/539635_EnV---Paladin.mp3",
                "keydex": "32"
            },
            {
                "name": "Pearlescent",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/547884_EnV---Pearlescent.mp3",
                "keydex": "33"
            },
            {
                "name": "Streetlights",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/548239_EnV---Streetlights.mp3",
                "keydex": "34"
            },
            {
                "name": "Shinto",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/550961_EnV---Shinto.mp3",
                "keydex": "35"
            },
            {
                "name": "6000 Strong",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/597399_EnV---5000-Strong.mp3",
                "keydex": "36"
            },
            {
                "name": "Ginseng",
                "artist": "EnV",
                "album": "EnV 2014",
                "url": "./songs/ENV/643474_EnV---Ginseng.mp3",
                "keydex": "37"
            },
            {
                "name": "The-IcePack-Rises",
                "artist": "EnV",
                "album": "EnV 2016",
                "url": "./songs/ENV/665115_EnV---The-IcePack-Rises.mp3",
                "keydex": "38"
            },
            {
                "name": "Microburst",
                "artist": "EnV",
                "album": "EnV 2016",
                "url": "./songs/ENV/695257_EnV---Microburst.mp3",
                "keydex": "39"
            },
            {
                "name": "It's-a-Me (Super Mario World)",
                "artist": "RobKTA",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/01 It's-a-Me (Super Mario World).mp3",
                "keydex": "40"
            },
            {
                "name": "Where the Wild Things Are (New Super Mario Bros. Wii)",
                "artist": "RobKTA",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/02 Where the Wild Things Are (New Super Mario Bros. Wii).mp3",
                "keydex": "41"
            },
            {
                "name": "Star Power (New Super Mario Bros. 2)",
                "artist": "bLind, Beatdrop",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/03 Star Power (New Super Mario Bros. 2).mp3",
                "keydex": "42"
            },
            {
                "name": "Caravan Bowser (Super Mario 3D World)",
                "artist": "Flexstyle",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/04 Caravan Bowser (Super Mario 3D World).mp3",
                "keydex": "43"
            },
            {
                "name": "Eet's a Nu World (Super Mario World)",
                "artist": "RobKTA",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/05 Eet's a Nu World (Super Mario World).mp3",
                "keydex": "44"
            },
            {
                "name": "Herculean (Super Mario Bros. 3)",
                "artist": "RobKTA",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/06 Herculean (Super Mario Bros. 3).mp3",
                "keydex": "45"
            },
            {
                "name": "Underground Pipe Society (Super Mario Bros. 3)",
                "artist": "Flexstyle",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/07 Underground Pipe Society (Super Mario Bros. 3).mp3",
                "keydex": "46"
            },
            {
                "name": "The Other Side (Super Mario Bros. 3)",
                "artist": "bLind, Beatdrop",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/08 The Other Side (Super Mario Bros. 3).mp3",
                "keydex": "47"
            },
            {
                "name": "Do Yoshi What I See? (Super Mario World 2: Yoshi's Island)",
                "artist": "Flexstyle",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/09 Do Yoshi What I See (Super Mario World 2 - Yoshi's Island).mp3",
                "keydex": "48"
            },
            {
                "name": "2D Beat (Super Mario 3D Land)",
                "artist": "bLind, Beatdrop",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/10 2D Beat (Super Mario 3D Land).mp3",
                "keydex": "49"
            },
            {
                "name": "Greedbuilt (Wario Land)",
                "artist": "Flexstyle",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/11 Greedbuilt (Wario Land).mp3",
                "keydex": "50"
            },
            {
                "name": "Vanilla Underground (Super Mario World)",
                "artist": "RobKTA",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/12 Vanilla Underground (Super Mario World).mp3",
                "keydex": "51"
            },
            {
                "name": "Goomba Stomp (Super Mario 3D World)",
                "artist": "RobKTA",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/13 Goomba Stomp (Super Mario 3D World).mp3",
                "keydex": "52"
            },
            {
                "name": "Koopa Reaper (Super Mario World)",
                "artist": "bLind, Beatdrop",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/14 Koopa Reaper (Super Mario World).mp3",
                "keydex": "53"
            },
            {
                "name": "PL41|\| (New Super Mario Bros.)",
                "artist": "Flexstyle",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/15 PL41N (New Super Mario Bros.).mp3",
                "keydex": "54"
            },
            {
                "name": "Heatrave (New Super Mario Bros. 2)",
                "artist": "Flexstyle",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/16 Heatrave (New Super Mario Bros. 2).mp3",
                "keydex": "55"
            },
            {
                "name": "Invincible (Super Mario World)",
                "artist": "bLind, Beatdrop",
                "album": "Super Cartography Bros.",
                "url": "./songs/Super Cartography Bros/17 Invincible (Super Mario World).mp3",
                "keydex": "56"
            },
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
let playBar = document.getElementById('ProgressBack');
sethandlers();
let playing = 0;
let shuffleval = 0;
uniArtists = [];
uniAlbums = [];
uniGenres = [];
ready=true;
playlistType.options.length = 0;
let option = document.createElement("option");
option.text = "Default";
playlistType.add(option);
option = document.createElement("option");
option.text = "Artist";
playlistType.add(option);
option = document.createElement("option");
option.text = "Album";
playlistType.add(option);

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
    document.getElementById("ProgressBuff").addEventListener("click", songAdjust);
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
    var offset = playBar.getBoundingClientRect();
    console.log(offset);
    var x = event.pageX - offset.left;
    console.log(x);

    Amplitude.setSongPlayedPercentage( ( parseFloat( x ) / parseFloat( playBar.offsetWidth) ) * 100 );
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

                    let songBufferedPercentage = Amplitude.getBuffered();
                    bufferedBar.style.paddingRight = (songBufferedPercentage * 3) + 'px';
                }
            }, 'songs': mainList,
        });
        maxLen = Amplitude.getSongs().length;
        window.requestAnimationFrame(updateInfo);
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

                let songBufferedPercentage = Amplitude.getBuffered();
                bufferedBar.style.paddingRight = (songBufferedPercentage * 3) + 'px';
            }
        }, 'songs': newList,
    });
    maxLen = Amplitude.getSongs().length;
    Amplitude.setRepeat();
    window.requestAnimationFrame(updateInfo);

};

