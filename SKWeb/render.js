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
            {
                "name": "01-dropkick_murphys-hang_em_high.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/01-dropkick_murphys-hang_em_high.mp3",
                "keydex": "0"
            },
            {
                "name": "02 - The State Of Massachusetts.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/02 - The State Of Massachusetts.mp3",
                "keydex": "1"
            },
            {
                "name": "02-dropkick_murphys-going_out_in_style.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/02-dropkick_murphys-going_out_in_style.mp3",
                "keydex": "2"
            },
            {
                "name": "03-dropkick_murphys-the_hardest_mile.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/03-dropkick_murphys-the_hardest_mile.mp3",
                "keydex": "3"
            },
            {
                "name": "06-dropkick_murphys-climbing_a_chair_to_bed.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/06-dropkick_murphys-climbing_a_chair_to_bed.mp3",
                "keydex": "4"
            },
            {
                "name": "08-dropkick_murphys-deeds_not_words.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/08-dropkick_murphys-deeds_not_words.mp3",
                "keydex": "5"
            },
            {
                "name": "09-dropkick_murphys-take_em_down.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/09-dropkick_murphys-take_em_down.mp3",
                "keydex": "6"
            },
            {
                "name": "10-dropkick_murphys-sunday_hardcore_matinee.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/10-dropkick_murphys-sunday_hardcore_matinee.mp3",
                "keydex": "7"
            },
            {
                "name": "12-dropkick_murphys-peg_o_my_heart.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/12-dropkick_murphys-peg_o_my_heart.mp3",
                "keydex": "8"
            },
            {
                "name": "13-dropkick_murphys-the_irish_rover.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/13-dropkick_murphys-the_irish_rover.mp3",
                "keydex": "9"
            },
            {
                "name": "14 - The Warriors Code.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/14 - The Warriors Code.mp3",
                "keydex": "10"
            },
            {
                "name": "20 - I'm Shipping Up To Boston (Feat. The Mighty Mighty Bosstones).mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/20 - I'm Shipping Up To Boston (Feat. The Mighty Mighty Bosstones).mp3",
                "keydex": "11"
            },
            {
                "name": "Dropkick Murphys - 01 - 21 Guitar Salute.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 01 - 21 Guitar Salute.mp3",
                "keydex": "12"
            },
            {
                "name": "Dropkick Murphys - 01 - Barroom Hero.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 01 - Barroom Hero.mp3",
                "keydex": "13"
            },
            {
                "name": "Dropkick Murphys - 01 - Boys On The Docks.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 01 - Boys On The Docks.mp3",
                "keydex": "14"
            },
            {
                "name": "Dropkick Murphys - 01 - Walk Away.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 01 - Walk Away.mp3",
                "keydex": "15"
            },
            {
                "name": "Dropkick Murphys - 02 - Blood And Whiskey.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 02 - Blood And Whiskey.mp3",
                "keydex": "16"
            },
            {
                "name": "Dropkick Murphys - 02 - Do Or Die.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 02 - Do Or Die.mp3",
                "keydex": "17"
            },
            {
                "name": "Dropkick Murphys - 02 - Fightstarter Karaoke.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 02 - Fightstarter Karaoke.mp3",
                "keydex": "18"
            },
            {
                "name": "Dropkick Murphys - 02 - Fortunate Son.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 02 - Fortunate Son.mp3",
                "keydex": "19"
            },
            {
                "name": "Dropkick Murphys - 02 - The Legend Of Finn Mac.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 02 - The Legend Of Finn Mac.mp3",
                "keydex": "20"
            },
            {
                "name": "Dropkick Murphys - 02 - Worker's Song.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 02 - Worker's Song.mp3",
                "keydex": "21"
            },
            {
                "name": "Dropkick Murphys - 03 - Boys On The Docks (Live).mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 03 - Boys On The Docks (Live).mp3",
                "keydex": "22"
            },
            {
                "name": "Dropkick Murphys - 03 - Get Up.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 03 - Get Up.mp3",
                "keydex": "23"
            },
            {
                "name": "Dropkick Murphys - 03 - John Law.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 03 - John Law.mp3",
                "keydex": "24"
            },
            {
                "name": "Dropkick Murphys - 03 - Nut Rocker.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 03 - Nut Rocker.mp3",
                "keydex": "25"
            },
            {
                "name": "Dropkick Murphys - 03 - Pipebomb On Lansdowne.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 03 - Pipebomb On Lansdowne.mp3",
                "keydex": "26"
            },
            {
                "name": "Dropkick Murphys - 03 - Which Side Are You On_.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 03 - Which Side Are You On_.mp3",
                "keydex": "27"
            },
            {
                "name": "Dropkick Murphys - 04 - Black Velvet Band.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 04 - Black Velvet Band.mp3",
                "keydex": "28"
            },
            {
                "name": "Dropkick Murphys - 04 - Never Alone.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 04 - Never Alone.mp3",
                "keydex": "29"
            },
            {
                "name": "Dropkick Murphys - 04 - Perfect Stranger.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 04 - Perfect Stranger.mp3",
                "keydex": "30"
            },
            {
                "name": "Dropkick Murphys - 04 - Regular Guy.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 04 - Regular Guy.mp3",
                "keydex": "31"
            },
            {
                "name": "Dropkick Murphys - 04 - The Rocky Road To Dublin.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 04 - The Rocky Road To Dublin.mp3",
                "keydex": "32"
            },
            {
                "name": "Dropkick Murphys - 04 - You're A Rebel.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 04 - You're A Rebel.mp3",
                "keydex": "33"
            },
            {
                "name": "Dropkick Murphys - 05 - Gonna Be A Blackout Tonight.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 05 - Gonna Be A Blackout Tonight.mp3",
                "keydex": "34"
            },
            {
                "name": "Dropkick Murphys - 05 - Heroes From Our Past.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 05 - Heroes From Our Past.mp3",
                "keydex": "35"
            },
            {
                "name": "Dropkick Murphys - 06 - Career Opportunities (Live).mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 06 - Career Opportunities (Live).mp3",
                "keydex": "36"
            },
            {
                "name": "Dropkick Murphys - 06 - Memories Remain.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 06 - Memories Remain.mp3",
                "keydex": "37"
            },
            {
                "name": "Dropkick Murphys - 06 - Upstarts And Broken Hearts.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 06 - Upstarts And Broken Hearts.mp3",
                "keydex": "38"
            },
            {
                "name": "Dropkick Murphys - 06 - Vengeance.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 06 - Vengeance.mp3",
                "keydex": "39"
            },
            {
                "name": "Dropkick Murphys - 07 - Buried Alive.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 07 - Buried Alive.mp3",
                "keydex": "40"
            },
            {
                "name": "Dropkick Murphys - 07 - Devil's Brigade.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 07 - Devil's Brigade.mp3",
                "keydex": "41"
            },
            {
                "name": "Dropkick Murphys - 07 - It's A Long Way To The Top (If You Wanna Rock 'N' Roll).mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 07 - It's A Long Way To The Top (If You Wanna Rock 'N' Roll).mp3",
                "keydex": "42"
            },
            {
                "name": "Dropkick Murphys - 07 - Road Of The Righteous.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 07 - Road Of The Righteous.mp3",
                "keydex": "43"
            },
            {
                "name": "Dropkick Murphys - 07 - The Gauntlet.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 07 - The Gauntlet.mp3",
                "keydex": "44"
            },
            {
                "name": "Dropkick Murphys - 08 - Take It Or Leave It.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 08 - Take It Or Leave It.mp3",
                "keydex": "45"
            },
            {
                "name": "Dropkick Murphys - 08 - Warlords.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 08 - Warlords.mp3",
                "keydex": "46"
            },
            {
                "name": "Dropkick Murphys - 09 - Alcohol.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 09 - Alcohol.mp3",
                "keydex": "47"
            },
            {
                "name": "Dropkick Murphys - 09 - Fields Of Athenry.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 09 - Fields Of Athenry.mp3",
                "keydex": "48"
            },
            {
                "name": "Dropkick Murphys - 09 - Homeward Bound.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 09 - Homeward Bound.mp3",
                "keydex": "49"
            },
            {
                "name": "Dropkick Murphys - 10 - Front Seat.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 10 - Front Seat.mp3",
                "keydex": "50"
            },
            {
                "name": "Dropkick Murphys - 10 - Going Strong.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 10 - Going Strong.mp3",
                "keydex": "51"
            },
            {
                "name": "Dropkick Murphys - 11 - As One.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 11 - As One.mp3",
                "keydex": "52"
            },
            {
                "name": "Dropkick Murphys - 11 - The Fighting 69th.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 11 - The Fighting 69th.mp3",
                "keydex": "53"
            },
            {
                "name": "Dropkick Murphys - 11 - The Fortunes Of War.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 11 - The Fortunes Of War.mp3",
                "keydex": "54"
            },
            {
                "name": "Dropkick Murphys - 12 - A Few Good Men.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 12 - A Few Good Men.mp3",
                "keydex": "55"
            },
            {
                "name": "Dropkick Murphys - 12 - Billy's Bones.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 12 - Billy's Bones.mp3",
                "keydex": "56"
            },
            {
                "name": "Dropkick Murphys - 12 - Boston Asphalt.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 12 - Boston Asphalt.mp3",
                "keydex": "57"
            },
            {
                "name": "Dropkick Murphys - 12 - Mob Mentality.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 12 - Mob Mentality.mp3",
                "keydex": "58"
            },
            {
                "name": "Dropkick Murphys - 12 - This Is Your Life.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 12 - This Is Your Life.mp3",
                "keydex": "59"
            },
            {
                "name": "Dropkick Murphys - 13 - Finnegan's Wake.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 13 - Finnegan's Wake.mp3",
                "keydex": "60"
            },
            {
                "name": "Dropkick Murphys - 13 - Informer.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 13 - Informer.mp3",
                "keydex": "61"
            },
            {
                "name": "Dropkick Murphys - 13 - Time To Go.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 13 - Time To Go.mp3",
                "keydex": "62"
            },
            {
                "name": "Dropkick Murphys - 14 - Caps And Bottles.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 14 - Caps And Bottles.mp3",
                "keydex": "63"
            },
            {
                "name": "Dropkick Murphys - 14 - Gang's All Here (Live).mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 14 - Gang's All Here (Live).mp3",
                "keydex": "64"
            },
            {
                "name": "Dropkick Murphys - 14 - The Only Road.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 14 - The Only Road.mp3",
                "keydex": "65"
            },
            {
                "name": "Dropkick Murphys - 15 - Amazing Grace.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 15 - Amazing Grace.mp3",
                "keydex": "66"
            },
            {
                "name": "Dropkick Murphys - 15 - Rock 'n' Roll.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 15 - Rock 'n' Roll.mp3",
                "keydex": "67"
            },
            {
                "name": "Dropkick Murphys - 16 - The Spicy McHaggis Jig.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 16 - The Spicy McHaggis Jig.mp3",
                "keydex": "68"
            },
            {
                "name": "Dropkick Murphys - 17 - Never Again.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 17 - Never Again.mp3",
                "keydex": "69"
            },
            {
                "name": "Dropkick Murphys - 18 - Halloween.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 18 - Halloween.mp3",
                "keydex": "70"
            },
            {
                "name": "Dropkick Murphys - 21 - Working.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 21 - Working.mp3",
                "keydex": "71"
            },
            {
                "name": "Dropkick Murphys - 22 - Victory.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 22 - Victory.mp3",
                "keydex": "72"
            },
            {
                "name": "Dropkick Murphys - 23 - We Got The Power.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - 23 - We Got The Power.mp3",
                "keydex": "73"
            },
            {
                "name": "Dropkick Murphys - Captain Kelly's Kitchen.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - Captain Kelly's Kitchen.mp3",
                "keydex": "74"
            },
            {
                "name": "Dropkick Murphys - Citizen C.I.A.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - Citizen C.I.A.mp3",
                "keydex": "75"
            },
            {
                "name": "Dropkick Murphys - I'm Shipping Up To Boston.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - I'm Shipping Up To Boston.mp3",
                "keydex": "76"
            },
            {
                "name": "Dropkick Murphys - Sunshine Highway.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - Sunshine Highway.mp3",
                "keydex": "77"
            },
            {
                "name": "Dropkick Murphys - Take It and Run.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - Take It and Run.mp3",
                "keydex": "78"
            },
            {
                "name": "Dropkick Murphys - The Last Letter Home.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - The Last Letter Home.mp3",
                "keydex": "79"
            },
            {
                "name": "Dropkick Murphys - Walking Dead.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - Walking Dead.mp3",
                "keydex": "80"
            },
            {
                "name": "Dropkick Murphys - Wicked Sensitive Crew.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - Wicked Sensitive Crew.mp3",
                "keydex": "81"
            },
            {
                "name": "Dropkick Murphys - Your Spirit's Alive.mp3",
                "artist": "Dropkick Murphys",
                "album": "",
                "url": "./songs/Dropkick Murphys/Dropkick Murphys - Your Spirit's Alive.mp3",
                "keydex": "82"
            },
            {
                "name": "105753_Heaven_remix.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/105753_Heaven_remix.mp3",
                "keydex": "83"
            },
            {
                "name": "498830_EnV---FireFrost.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/498830_EnV---FireFrost.mp3",
                "keydex": "84"
            },
            {
                "name": "509762_EnV---RPM.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/509762_EnV---RPM.mp3",
                "keydex": "85"
            },
            {
                "name": "513064_EnV---Uprise.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/513064_EnV---Uprise.mp3",
                "keydex": "86"
            },
            {
                "name": "516336_EnV---Pneumatic-Tok.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/516336_EnV---Pneumatic-Tok.mp3",
                "keydex": "87"
            },
            {
                "name": "521252_EnV---Sanctuary.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/521252_EnV---Sanctuary.mp3",
                "keydex": "88"
            },
            {
                "name": "525196_EnV---Green-With-Me.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/525196_EnV---Green-With-Me.mp3",
                "keydex": "89"
            },
            {
                "name": "527560_EnV---Valiant.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/527560_EnV---Valiant.mp3",
                "keydex": "90"
            },
            {
                "name": "532991_EnV---BloomRadio-Ed.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/532991_EnV---BloomRadio-Ed.mp3",
                "keydex": "91"
            },
            {
                "name": "534977_Envy-Wakkawakka-Rem.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/534977_Envy-Wakkawakka-Rem.mp3",
                "keydex": "92"
            },
            {
                "name": "535710_EnV-Sanctuary-DM-Re.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/535710_EnV-Sanctuary-DM-Re.mp3",
                "keydex": "93"
            },
            {
                "name": "538354_EnV---Vee.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/538354_EnV---Vee.mp3",
                "keydex": "94"
            },
            {
                "name": "539635_EnV---Paladin.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/539635_EnV---Paladin.mp3",
                "keydex": "95"
            },
            {
                "name": "547884_EnV---Pearlescent.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/547884_EnV---Pearlescent.mp3",
                "keydex": "96"
            },
            {
                "name": "548239_EnV---Streetlights.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/548239_EnV---Streetlights.mp3",
                "keydex": "97"
            },
            {
                "name": "550961_EnV---Shinto.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/550961_EnV---Shinto.mp3",
                "keydex": "98"
            },
            {
                "name": "597399_EnV---5000-Strong.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/597399_EnV---5000-Strong.mp3",
                "keydex": "99"
            },
            {
                "name": "643474_EnV---Ginseng.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/643474_EnV---Ginseng.mp3",
                "keydex": "100"
            },
            {
                "name": "665115_EnV---The-IcePack-Rises.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/665115_EnV---The-IcePack-Rises.mp3",
                "keydex": "101"
            },
            {
                "name": "695257_EnV---Microburst.mp3",
                "artist": "EnV",
                "album": "",
                "url": "./songs/EnV/695257_EnV---Microburst.mp3",
                "keydex": "102"
            },
            {
                "name": "01 - Five Iron Frenzy - Kamikaze - Cheeses Of Nazareth.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/01 - Five Iron Frenzy - Kamikaze - Cheeses Of Nazareth.mp3",
                "keydex": "103"
            },
            {
                "name": "01 - Five Iron Frenzy - Pre-Ex-Girlfriend.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/01 - Five Iron Frenzy - Pre-Ex-Girlfriend.mp3",
                "keydex": "104"
            },
            {
                "name": "01 - Five Iron Frenzy - The Old West.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/01 - Five Iron Frenzy - The Old West.mp3",
                "keydex": "105"
            },
            {
                "name": "02 - Five Iron Frenzy - Far, Far Away.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/02 - Five Iron Frenzy - Far, Far Away.mp3",
                "keydex": "106"
            },
            {
                "name": "02 - Five Iron Frenzy - Me Oh My.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/02 - Five Iron Frenzy - Me Oh My.mp3",
                "keydex": "107"
            },
            {
                "name": "02 - Five Iron Frenzy - Rhubarb Pie - Cheeses Of Nazareth.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/02 - Five Iron Frenzy - Rhubarb Pie - Cheeses Of Nazareth.mp3",
                "keydex": "108"
            },
            {
                "name": "02 - Five Iron Frenzy - Where is Micah.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/02 - Five Iron Frenzy - Where is Micah.mp3",
                "keydex": "109"
            },
            {
                "name": "02 - Five Iron Frenzy - Where Zero Meets Fifteen.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/02 - Five Iron Frenzy - Where Zero Meets Fifteen.mp3",
                "keydex": "110"
            },
            {
                "name": "03 - Five Iron Frenzy - Cool Enough For You.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/03 - Five Iron Frenzy - Cool Enough For You.mp3",
                "keydex": "111"
            },
            {
                "name": "03 - Five Iron Frenzy - Marty - Cheeses Of Nazareth.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/03 - Five Iron Frenzy - Marty - Cheeses Of Nazareth.mp3",
                "keydex": "112"
            },
            {
                "name": "03 - Five Iron Frenzy - Solidarity.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/03 - Five Iron Frenzy - Solidarity.mp3",
                "keydex": "113"
            },
            {
                "name": "03 - Five Iron Frenzy - Superpowers.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/03 - Five Iron Frenzy - Superpowers.mp3",
                "keydex": "114"
            },
            {
                "name": "03 - Five Iron Frenzy - You Can't Handle This.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/03 - Five Iron Frenzy - You Can't Handle This.mp3",
                "keydex": "115"
            },
            {
                "name": "03-Five Iron Frenzy - Handbook For The Sellout.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/03-Five Iron Frenzy - Handbook For The Sellout.mp3",
                "keydex": "116"
            },
            {
                "name": "04 - Five Iron Frenzy - Anthem.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/04 - Five Iron Frenzy - Anthem.mp3",
                "keydex": "117"
            },
            {
                "name": "04 - Five Iron Frenzy - Farsighted.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/04 - Five Iron Frenzy - Farsighted.mp3",
                "keydex": "118"
            },
            {
                "name": "04 - Five Iron Frenzy - One Girl Army.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/04 - Five Iron Frenzy - One Girl Army.mp3",
                "keydex": "119"
            },
            {
                "name": "04 - Five Iron Frenzy - The Phantom Mullet.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/04 - Five Iron Frenzy - The Phantom Mullet.mp3",
                "keydex": "120"
            },
            {
                "name": "05 - Five Iron Frenzy - Faking Life.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/05 - Five Iron Frenzy - Faking Life.mp3",
                "keydex": "121"
            },
            {
                "name": "05 - Five Iron Frenzy - Suckerpunch.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/05 - Five Iron Frenzy - Suckerpunch.mp3",
                "keydex": "122"
            },
            {
                "name": "05 - Five Iron Frenzy - Sweet Talkin' Woman.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/05 - Five Iron Frenzy - Sweet Talkin' Woman.mp3",
                "keydex": "123"
            },
            {
                "name": "05 - Five Iron Frenzy - Ugly Day.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/05 - Five Iron Frenzy - Ugly Day.mp3",
                "keydex": "124"
            },
            {
                "name": "07 - Five Iron Frenzy - Arnold, and Willis, and Mr. Drumondd.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/07 - Five Iron Frenzy - Arnold, and Willis, and Mr. Drumondd.mp3",
                "keydex": "125"
            },
            {
                "name": "07 - Five Iron Frenzy - Blue Comb '78.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/07 - Five Iron Frenzy - Blue Comb '78.mp3",
                "keydex": "126"
            },
            {
                "name": "07 - Five Iron Frenzy - Four-Fifty-One.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/07 - Five Iron Frenzy - Four-Fifty-One.mp3",
                "keydex": "127"
            },
            {
                "name": "07 - Five Iron Frenzy - Get Your Riot Gear.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/07 - Five Iron Frenzy - Get Your Riot Gear.mp3",
                "keydex": "128"
            },
            {
                "name": "07 - Five Iron Frenzy - Juggernaut.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/07 - Five Iron Frenzy - Juggernaut.mp3",
                "keydex": "129"
            },
            {
                "name": "08 - Five Iron Frenzy - Banner Year.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/08 - Five Iron Frenzy - Banner Year.mp3",
                "keydex": "130"
            },
            {
                "name": "08 - Five Iron Frenzy - I Feel Lucky.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/08 - Five Iron Frenzy - I Feel Lucky.mp3",
                "keydex": "131"
            },
            {
                "name": "08 - Five Iron Frenzy - Plan B.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/08 - Five Iron Frenzy - Plan B.mp3",
                "keydex": "132"
            },
            {
                "name": "08 - Five Iron Frenzy - The Untimely Death of Brad.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/08 - Five Iron Frenzy - The Untimely Death of Brad.mp3",
                "keydex": "133"
            },
            {
                "name": "08 - Five Iron Frenzy - You Probably Shouldn't Move Here.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/08 - Five Iron Frenzy - You Probably Shouldn't Move Here.mp3",
                "keydex": "134"
            },
            {
                "name": "09 - Five Iron Frenzy - Blue Mix.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/09 - Five Iron Frenzy - Blue Mix.mp3",
                "keydex": "135"
            },
            {
                "name": "09 - Five Iron Frenzy - Milestone.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/09 - Five Iron Frenzy - Milestone.mp3",
                "keydex": "136"
            },
            {
                "name": "09 - Five Iron Frenzy - Oh Canada.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/09 - Five Iron Frenzy - Oh Canada.mp3",
                "keydex": "137"
            },
            {
                "name": "09 - Five Iron Frenzy - Second Season.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/09 - Five Iron Frenzy - Second Season.mp3",
                "keydex": "138"
            },
            {
                "name": "10 - Five Iron Frenzy - Beautiful America.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/10 - Five Iron Frenzy - Beautiful America.mp3",
                "keydex": "139"
            },
            {
                "name": "10 - Five Iron Frenzy - Giants.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/10 - Five Iron Frenzy - Giants.mp3",
                "keydex": "140"
            },
            {
                "name": "10 - Five Iron Frenzy - It's Not Unusual.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/10 - Five Iron Frenzy - It's Not Unusual.mp3",
                "keydex": "141"
            },
            {
                "name": "10 - Five Iron Frenzy - Litmus.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/10 - Five Iron Frenzy - Litmus.mp3",
                "keydex": "142"
            },
            {
                "name": "10 - Five Iron Frenzy - Vultures.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/10 - Five Iron Frenzy - Vultures.mp3",
                "keydex": "143"
            },
            {
                "name": "11 - Five Iron Frenzy - Car.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/11 - Five Iron Frenzy - Car.mp3",
                "keydex": "144"
            },
            {
                "name": "11 - Five Iron Frenzy - Combat Chuck.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/11 - Five Iron Frenzy - Combat Chuck.mp3",
                "keydex": "145"
            },
            {
                "name": "11 - Five Iron Frenzy - Left - Cheeses Of Nazareth.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/11 - Five Iron Frenzy - Left - Cheeses Of Nazareth.mp3",
                "keydex": "146"
            },
            {
                "name": "11 - Five Iron Frenzy - Oh, Canada.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/11 - Five Iron Frenzy - Oh, Canada.mp3",
                "keydex": "147"
            },
            {
                "name": "12 - Five Iron Frenzy - All The Hype.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/12 - Five Iron Frenzy - All The Hype.mp3",
                "keydex": "148"
            },
            {
                "name": "12 - Five Iron Frenzy - Eulogy.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/12 - Five Iron Frenzy - Eulogy.mp3",
                "keydex": "149"
            },
            {
                "name": "13 - Five Iron Frenzy - Everywhere I Go.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/13 - Five Iron Frenzy - Everywhere I Go.mp3",
                "keydex": "150"
            },
            {
                "name": "14 - Five Iron Frenzy - A Flowery Song.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/14 - Five Iron Frenzy - A Flowery Song.mp3",
                "keydex": "151"
            },
            {
                "name": "14 - Five Iron Frenzy - A New Hope.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/14 - Five Iron Frenzy - A New Hope.mp3",
                "keydex": "152"
            },
            {
                "name": "15 - Five Iron Frenzy - World Without End.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/15 - Five Iron Frenzy - World Without End.mp3",
                "keydex": "153"
            },
            {
                "name": "Five Iron Frenzy - 02 - At Least I'm Not Like All Those Othe.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 02 - At Least I'm Not Like All Those Othe.mp3",
                "keydex": "154"
            },
            {
                "name": "Five Iron Frenzy - 03 - So Far, So Bad.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 03 - So Far, So Bad.mp3",
                "keydex": "155"
            },
            {
                "name": "Five Iron Frenzy - 05 - American Kryptonite.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 05 - American Kryptonite.mp3",
                "keydex": "156"
            },
            {
                "name": "Five Iron Frenzy - 06 - It Was Beautiful.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 06 - It Was Beautiful.mp3",
                "keydex": "157"
            },
            {
                "name": "Five Iron Frenzy - 07 - Wizard Needs Food, Badly.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 07 - Wizard Needs Food, Badly.mp3",
                "keydex": "158"
            },
            {
                "name": "Five Iron Frenzy - 08 - Farewell to Arms.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 08 - Farewell to Arms.mp3",
                "keydex": "159"
            },
            {
                "name": "Five Iron Frenzy - 09 - See the Flames Begin to Crawl.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 09 - See the Flames Begin to Crawl.mp3",
                "keydex": "160"
            },
            {
                "name": "Five Iron Frenzy - 11 - Something Like Laughter.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 11 - Something Like Laughter.mp3",
                "keydex": "161"
            },
            {
                "name": "Five Iron Frenzy - 12 - That's How the Story Ends.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 12 - That's How the Story Ends.mp3",
                "keydex": "162"
            },
            {
                "name": "Five Iron Frenzy - 13 - On Distant Shores.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - 13 - On Distant Shores.mp3",
                "keydex": "163"
            },
            {
                "name": "Five Iron Frenzy - It Was A Dark And Stormy Night.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy - It Was A Dark And Stormy Night.mp3",
                "keydex": "164"
            },
            {
                "name": "Five Iron Frenzy-Mama Mia-Rarities.mp3",
                "artist": "Five Iron Frenzy",
                "album": "",
                "url": "./songs/Five Iron Frenzy/Five Iron Frenzy-Mama Mia-Rarities.mp3",
                "keydex": "165"
            },
            {
                "name": "The Sword - Celestial Crown.mp3",
                "artist": "The Sword",
                "album": "",
                "url": "./songs/Sword, The/The Sword - Celestial Crown.mp3",
                "keydex": "166"
            },
            {
                "name": "The Sword - Freya.mp3",
                "artist": "The Sword",
                "album": "",
                "url": "./songs/Sword, The/The Sword - Freya.mp3",
                "keydex": "167"
            },
            {
                "name": "The Sword - Gods Of The Earth - 02 - How Heavy This Axe.mp3",
                "artist": "The Sword",
                "album": "",
                "url": "./songs/Sword, The/The Sword - Gods Of The Earth - 02 - How Heavy This Axe.mp3",
                "keydex": "168"
            },
            {
                "name": "The Sword - The Black River.mp3",
                "artist": "The Sword",
                "album": "",
                "url": "./songs/Sword, The/The Sword - The Black River.mp3",
                "keydex": "169"
            },
            {
                "name": "The Sword-Iron Swan.mp3",
                "artist": "The Sword",
                "album": "",
                "url": "./songs/Sword, The/The Sword-Iron Swan.mp3",
                "keydex": "170"
            },
            {
                "name": "The Sword-Maiden, Mother And Crone.mp3",
                "artist": "The Sword",
                "album": "",
                "url": "./songs/Sword, The/The Sword-Maiden, Mother And Crone.mp3",
                "keydex": "171"
            },
            {
                "name": "&quot;I Feel Fantastic&quot; music video.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/&quot;I Feel Fantastic&quot; music video.mp3",
                "keydex": "172"
            },
            {
                "name": "06 - Track 6.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/06 - Track 6.mp3",
                "keydex": "173"
            },
            {
                "name": "07 - Track 7.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/07 - Track 7.mp3",
                "keydex": "174"
            },
            {
                "name": "07. The Impression That I Get.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/07. The Impression That I Get.mp3",
                "keydex": "175"
            },
            {
                "name": "08. All My Best Friends Are Metalheads.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/08. All My Best Friends Are Metalheads.mp3",
                "keydex": "176"
            },
            {
                "name": "09. Run Around.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/09. Run Around.mp3",
                "keydex": "177"
            },
            {
                "name": "10. Nowhere Near.mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/10. Nowhere Near.mp3",
                "keydex": "178"
            },
            {
                "name": "11 - Track 11.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/11 - Track 11.mp3",
                "keydex": "179"
            },
            {
                "name": "12. Here We Go.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/12. Here We Go.mp3",
                "keydex": "180"
            },
            {
                "name": "15. Let's Kick It up.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/15. Let's Kick It up.mp3",
                "keydex": "181"
            },
            {
                "name": "16. Going Digital.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/16. Going Digital.mp3",
                "keydex": "182"
            },
            {
                "name": "17. Stranger.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/17. Stranger.mp3",
                "keydex": "183"
            },
            {
                "name": "18 - Track 18.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/18 - Track 18.mp3",
                "keydex": "184"
            },
            {
                "name": "2 Unlimited - Get Ready For This.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/2 Unlimited - Get Ready For This.mp3",
                "keydex": "185"
            },
            {
                "name": "3 doors down - kryptonite (lyrics).mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/3 doors down - kryptonite (lyrics).mp3",
                "keydex": "186"
            },
            {
                "name": "370307_GaMetal___Koopa_s_Road.mp3",
                "artist": "TechnoX",
                "album": "The Game Corner",
                "url": "./songs/XYZ/370307_GaMetal___Koopa_s_Road.mp3",
                "keydex": "187"
            },
            {
                "name": "80s Karate Kid Soundtrack - You're The Best.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/80s Karate Kid Soundtrack - You're The Best.mp3",
                "keydex": "188"
            },
            {
                "name": "Afroman - Colt 45.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Afroman - Colt 45.mp3",
                "keydex": "189"
            },
            {
                "name": "Aha - Take On Me.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Aha - Take On Me.mp3",
                "keydex": "190"
            },
            {
                "name": "Angel Witch - Angel Witch.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Angel Witch - Angel Witch.mp3",
                "keydex": "191"
            },
            {
                "name": "Angel Witch - Baphomet.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Angel Witch - Baphomet.mp3",
                "keydex": "192"
            },
            {
                "name": "Angel Witch - Gorgon.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Angel Witch - Gorgon.mp3",
                "keydex": "193"
            },
            {
                "name": "Apache - Gangster Bitch.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Apache - Gangster Bitch.mp3",
                "keydex": "194"
            },
            {
                "name": "AWOLNATION- &quot;Burn It Down&quot; (with lyrics).mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/AWOLNATION- &quot;Burn It Down&quot; (with lyrics).mp3",
                "keydex": "195"
            },
            {
                "name": "Bachman Turner Overdrive-Taking care of business.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Bachman Turner Overdrive-Taking care of business.mp3",
                "keydex": "196"
            },
            {
                "name": "Barenaked Ladies - One Week.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Barenaked Ladies - One Week.mp3",
                "keydex": "197"
            },
            {
                "name": "Becoming Popular (The Pony Everypony Should Know).mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/Becoming Popular (The Pony Everypony Should Know).mp3",
                "keydex": "198"
            },
            {
                "name": "Blondie - Funky Town.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Blondie - Funky Town.mp3",
                "keydex": "199"
            },
            {
                "name": "Bloodhound Gang - Discovery Channel(1).mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Bloodhound Gang - Discovery Channel(1).mp3",
                "keydex": "200"
            },
            {
                "name": "Blur -  Song 2.mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/Blur -  Song 2.mp3",
                "keydex": "201"
            },
            {
                "name": "Buckethead - Jordan.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/Buckethead - Jordan.mp3",
                "keydex": "202"
            },
            {
                "name": "Busdriver - Avantcore.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Busdriver - Avantcore.mp3",
                "keydex": "203"
            },
            {
                "name": "Bustin.mp3",
                "artist": "TubeX",
                "album": "Actual Tubes",
                "url": "./songs/XYZ/Bustin.mp3",
                "keydex": "204"
            },
            {
                "name": "Crash Kings - You Got Me.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Crash Kings - You Got Me.mp3",
                "keydex": "205"
            },
            {
                "name": "Cruiserweight - To Be Quite Honest - Saints Row.mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/Cruiserweight - To Be Quite Honest - Saints Row.mp3",
                "keydex": "206"
            },
            {
                "name": "Cruis_n World Soundtrack_ Main Theme.mp3",
                "artist": "TubeX",
                "album": "The Jokes",
                "url": "./songs/XYZ/Cruis_n World Soundtrack_ Main Theme.mp3",
                "keydex": "207"
            },
            {
                "name": "DaRude - Castles In The Sky.mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/DaRude - Castles In The Sky.mp3",
                "keydex": "208"
            },
            {
                "name": "Darude - Rush.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/Darude - Rush.mp3",
                "keydex": "209"
            },
            {
                "name": "Darude - SandStorm.mp3",
                "artist": "XYZ",
                "album": "Digital World",
                "url": "./songs/XYZ/Darude - SandStorm.mp3",
                "keydex": "210"
            },
            {
                "name": "Disco - Le Chic - Freak Out(1).mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Disco - Le Chic - Freak Out(1).mp3",
                "keydex": "211"
            },
            {
                "name": "Dragon Force - Soldiers of the Wasteland.mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Dragon Force - Soldiers of the Wasteland.mp3",
                "keydex": "212"
            },
            {
                "name": "Dragon Force - Through The Fire And Flames.mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Dragon Force - Through The Fire And Flames.mp3",
                "keydex": "213"
            },
            {
                "name": "Dragon Force - Valley of the Damned.mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Dragon Force - Valley of the Damned.mp3",
                "keydex": "214"
            },
            {
                "name": "Duran Duran (01) - The Reflex.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Duran Duran (01) - The Reflex.mp3",
                "keydex": "215"
            },
            {
                "name": "Dwarf Hole (Diggy Diggy Hole) Fan Song and Animation.mp3",
                "artist": "TubeX",
                "album": "Actual Tubes",
                "url": "./songs/XYZ/Dwarf Hole (Diggy Diggy Hole) Fan Song and Animation.mp3",
                "keydex": "216"
            },
            {
                "name": "Elvis Presley - Hound Dog.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Elvis Presley - Hound Dog.mp3",
                "keydex": "217"
            },
            {
                "name": "Europe - The Final Countdown(1).mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Europe - The Final Countdown(1).mp3",
                "keydex": "218"
            },
            {
                "name": "Everclear - Everything To Everyone.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Everclear - Everything To Everyone.mp3",
                "keydex": "219"
            },
            {
                "name": "Everclear - Father of Mine.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Everclear - Father of Mine.mp3",
                "keydex": "220"
            },
            {
                "name": "Everclear - I've Seen Better Days.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Everclear - I've Seen Better Days.mp3",
                "keydex": "221"
            },
            {
                "name": "Everclear - She likes me for me.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Everclear - She likes me for me.mp3",
                "keydex": "222"
            },
            {
                "name": "Face Down - Red Jumpsuit Apparatus (Lyrics &amp; Song ).mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Face Down - Red Jumpsuit Apparatus (Lyrics &amp; Song ).mp3",
                "keydex": "223"
            },
            {
                "name": "Feeder- Renegades Saints Row the Third OST-1.mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/Feeder- Renegades Saints Row the Third OST-1.mp3",
                "keydex": "224"
            },
            {
                "name": "Feeder- Renegades Saints Row the Third OST.mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/Feeder- Renegades Saints Row the Third OST.mp3",
                "keydex": "225"
            },
            {
                "name": "Feels So Good.mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Feels So Good.mp3",
                "keydex": "226"
            },
            {
                "name": "Find A Pet Song.mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/Find A Pet Song.mp3",
                "keydex": "227"
            },
            {
                "name": "Firehouse - Overnight Sensation.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Firehouse - Overnight Sensation.mp3",
                "keydex": "228"
            },
            {
                "name": "Foozogz - Find A Pet (Candy Mix).mp3",
                "artist": "TubeX",
                "album": "Four Legs",
                "url": "./songs/XYZ/Foozogz - Find A Pet (Candy Mix).mp3",
                "keydex": "229"
            },
            {
                "name": "Gay Pimp - Soccer Practice.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Gay Pimp - Soccer Practice.mp3",
                "keydex": "230"
            },
            {
                "name": "Ghost Nappa Theme Full.mp3",
                "artist": "TubeX",
                "album": "The Jokes",
                "url": "./songs/XYZ/Ghost Nappa Theme Full.mp3",
                "keydex": "231"
            },
            {
                "name": "Gloria Gaynor - I Will Survive.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Gloria Gaynor - I Will Survive.mp3",
                "keydex": "232"
            },
            {
                "name": "Gloryhammer - Angus McFife (Lyrics).mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Gloryhammer - Angus McFife (Lyrics).mp3",
                "keydex": "233"
            },
            {
                "name": "Haddaway - What Is Love.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Haddaway - What Is Love.mp3",
                "keydex": "234"
            },
            {
                "name": "Happy_Birthday_To_Me (Part 2).mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Happy_Birthday_To_Me (Part 2).mp3",
                "keydex": "235"
            },
            {
                "name": "Harry Belafonte -- Jump in the Line.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Harry Belafonte -- Jump in the Line.mp3",
                "keydex": "236"
            },
            {
                "name": "Herb Alpert - Fandango.mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Herb Alpert - Fandango.mp3",
                "keydex": "237"
            },
            {
                "name": "I would walk 500 miles - The Proclaimers.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/I would walk 500 miles - The Proclaimers.mp3",
                "keydex": "238"
            },
            {
                "name": "Imagine (Part 5).mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Imagine (Part 5).mp3",
                "keydex": "239"
            },
            {
                "name": "IT'S THE END OF THE WORLD (AS WE KNOW IT) LYRIC VIDEO.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/IT'S THE END OF THE WORLD (AS WE KNOW IT) LYRIC VIDEO.mp3",
                "keydex": "240"
            },
            {
                "name": "James Brown - I Feel Good.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/James Brown - I Feel Good.mp3",
                "keydex": "241"
            },
            {
                "name": "Joan Jett - Bad Reputation.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Joan Jett - Bad Reputation.mp3",
                "keydex": "242"
            },
            {
                "name": "Journey - Separate Ways.mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Journey - Separate Ways.mp3",
                "keydex": "243"
            },
            {
                "name": "Journey singing _Now you_re a man_ by DVDA.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Journey singing _Now you_re a man_ by DVDA.mp3",
                "keydex": "244"
            },
            {
                "name": "Kansas - Carry on my Wayward Son.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Kansas - Carry on my Wayward Son.mp3",
                "keydex": "245"
            },
            {
                "name": "Kingswood - Ohio.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Kingswood - Ohio.mp3",
                "keydex": "246"
            },
            {
                "name": "Look At Me (I'm A Winner).mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/Look At Me (I'm A Winner).mp3",
                "keydex": "247"
            },
            {
                "name": "Loverboy - Working For The Weekend.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Loverboy - Working For The Weekend.mp3",
                "keydex": "248"
            },
            {
                "name": "Lyrics Born-Callin' Out.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Lyrics Born-Callin' Out.mp3",
                "keydex": "249"
            },
            {
                "name": "Mindless Self Indulgence - Shut Me Up.mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Mindless Self Indulgence - Shut Me Up.mp3",
                "keydex": "250"
            },
            {
                "name": "Monty Python - Knights of the Round Table.mp3",
                "artist": "TubeX",
                "album": "The Jokes",
                "url": "./songs/XYZ/Monty Python - Knights of the Round Table.mp3",
                "keydex": "251"
            },
            {
                "name": "Monty Python - The Pirate Song (Rutles with George Harrison & Eric Idle).mp3",
                "artist": "TubeX",
                "album": "The Jokes",
                "url": "./songs/XYZ/Monty Python - The Pirate Song (Rutles with George Harrison & Eric Idle).mp3",
                "keydex": "252"
            },
            {
                "name": "mulan - I_ll make a man out of you lyrics.mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/mulan - I_ll make a man out of you lyrics.mp3",
                "keydex": "253"
            },
            {
                "name": "Mumford & Sons - The Wolf (Official Audio).mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Mumford & Sons - The Wolf (Official Audio).mp3",
                "keydex": "254"
            },
            {
                "name": "MY LITTLE PONY - WINTER WRAP UP (DJ AMAYA VS. GROOVEBOT EXTE.mp3",
                "artist": "TubeX",
                "album": "Four Legs",
                "url": "./songs/XYZ/MY LITTLE PONY - WINTER WRAP UP (DJ AMAYA VS. GROOVEBOT EXTE.mp3",
                "keydex": "255"
            },
            {
                "name": "My little Pony Winter wrap up.mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/My little Pony Winter wrap up.mp3",
                "keydex": "256"
            },
            {
                "name": "My Little Pony_ Friendship is Magic _ At the Gala (Best Nigh.mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/My Little Pony_ Friendship is Magic _ At the Gala (Best Nigh.mp3",
                "keydex": "257"
            },
            {
                "name": "New No More Kings music video for &quot;Michael (Jump In)&quot;.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/New No More Kings music video for &quot;Michael (Jump In)&quot;.mp3",
                "keydex": "258"
            },
            {
                "name": "no more kings - critical hit.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/no more kings - critical hit.mp3",
                "keydex": "259"
            },
            {
                "name": "no more kings - someday.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/no more kings - someday.mp3",
                "keydex": "260"
            },
            {
                "name": "Nyan Cat.mp3",
                "artist": "TubeX",
                "album": "The Jokes",
                "url": "./songs/XYZ/Nyan Cat.mp3",
                "keydex": "261"
            },
            {
                "name": "Ok Go - Here It Goes Again    (Lyrics).mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Ok Go - Here It Goes Again    (Lyrics).mp3",
                "keydex": "262"
            },
            {
                "name": "Pantera - Vulgar Display Of Power - 03 - Walk.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Pantera - Vulgar Display Of Power - 03 - Walk.mp3",
                "keydex": "263"
            },
            {
                "name": "Paul Stanley - Live to win.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Paul Stanley - Live to win.mp3",
                "keydex": "264"
            },
            {
                "name": "Pinkie Pie_s No Fear Song.mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/Pinkie Pie_s No Fear Song.mp3",
                "keydex": "265"
            },
            {
                "name": "Plain White T's - Hate (I Really Don't Like You).mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/Plain White T's - Hate (I Really Don't Like You).mp3",
                "keydex": "266"
            },
            {
                "name": "Plain White T's - Revenge.mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/Plain White T's - Revenge.mp3",
                "keydex": "267"
            },
            {
                "name": "Push It To The Limit (scarface).mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Push It To The Limit (scarface).mp3",
                "keydex": "268"
            },
            {
                "name": "Rarity_s song_ Art of the Dress (with lyrics).mp3",
                "artist": "XYZ",
                "album": "",
                "url": "./songs/XYZ/Rarity_s song_ Art of the Dress (with lyrics).mp3",
                "keydex": "269"
            },
            {
                "name": "Riot - Narita.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Riot - Narita.mp3",
                "keydex": "270"
            },
            {
                "name": "Riot - Road Racin'.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Riot - Road Racin'.mp3",
                "keydex": "271"
            },
            {
                "name": "Rock and Roll  Queen - The Subways.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Rock and Roll  Queen - The Subways.mp3",
                "keydex": "272"
            },
            {
                "name": "Rocky Balboa -  Eye of the tiger.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Rocky Balboa -  Eye of the tiger.mp3",
                "keydex": "273"
            },
            {
                "name": "Running in the 90's.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Running in the 90's.mp3",
                "keydex": "274"
            },
            {
                "name": "Russkaja - Energia.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/Russkaja - Energia.mp3",
                "keydex": "275"
            },
            {
                "name": "Safety Dance - Men Without Hats Official Video.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Safety Dance - Men Without Hats Official Video.mp3",
                "keydex": "276"
            },
            {
                "name": "Sam-cha_Seong-jing (Part 3).mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Sam-cha_Seong-jing (Part 3).mp3",
                "keydex": "277"
            },
            {
                "name": "Saun Paul - We Be Burning.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Saun Paul - We Be Burning.mp3",
                "keydex": "278"
            },
            {
                "name": "Scatman John - Scat Man.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Scatman John - Scat Man.mp3",
                "keydex": "279"
            },
            {
                "name": "Swagberg ft. Maros - Pony Swag (OFFICIAL VIDEO) (HD Audio Ed.mp3",
                "artist": "TubeX",
                "album": "Four Legs",
                "url": "./songs/XYZ/Swagberg ft. Maros - Pony Swag (OFFICIAL VIDEO) (HD Audio Ed.mp3",
                "keydex": "280"
            },
            {
                "name": "System Of A Down - Killing In The Name.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/System Of A Down - Killing In The Name.mp3",
                "keydex": "281"
            },
            {
                "name": "Temptations - You Make Me Wanna Shout.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Temptations - You Make Me Wanna Shout.mp3",
                "keydex": "282"
            },
            {
                "name": "Tenacious D - Master Exploder.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Tenacious D - Master Exploder.mp3",
                "keydex": "283"
            },
            {
                "name": "Tenacious D - The Metal.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Tenacious D - The Metal.mp3",
                "keydex": "284"
            },
            {
                "name": "The Adored - T.V Riot.mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/The Adored - T.V Riot.mp3",
                "keydex": "285"
            },
            {
                "name": "The Datsuns - System Overload.mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/The Datsuns - System Overload.mp3",
                "keydex": "286"
            },
            {
                "name": "The KickDrums - Breathe Again.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/The KickDrums - Breathe Again.mp3",
                "keydex": "287"
            },
            {
                "name": "The Kooks - Bad Habit.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/The Kooks - Bad Habit.mp3",
                "keydex": "288"
            },
            {
                "name": "The Last Royals - Crystal Vases.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/The Last Royals - Crystal Vases.mp3",
                "keydex": "289"
            },
            {
                "name": "The President of the United States of America - Lump.mp3",
                "artist": "XYZ",
                "album": "Saints Radio",
                "url": "./songs/XYZ/The President of the United States of America - Lump.mp3",
                "keydex": "290"
            },
            {
                "name": "The Pretty Reckless - Miss Nothing.mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/The Pretty Reckless - Miss Nothing.mp3",
                "keydex": "291"
            },
            {
                "name": "The Ramones - Blitzkreig Bop.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/The Ramones - Blitzkreig Bop.mp3",
                "keydex": "292"
            },
            {
                "name": "The Rolling Stones - Satisfaction.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/The Rolling Stones - Satisfaction.mp3",
                "keydex": "293"
            },
            {
                "name": "There_She_Is (Part 1).mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/There_She_Is (Part 1).mp3",
                "keydex": "294"
            },
            {
                "name": "The_Llama_Song.mp3",
                "artist": "TubeX",
                "album": "The Jokes",
                "url": "./songs/XYZ/The_Llama_Song.mp3",
                "keydex": "295"
            },
            {
                "name": "Timbuk 3 - The Future's So Bright, I Gotta Wear Shades.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Timbuk 3 - The Future's So Bright, I Gotta Wear Shades.mp3",
                "keydex": "296"
            },
            {
                "name": "Van Halen - Jump.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Van Halen - Jump.mp3",
                "keydex": "297"
            },
            {
                "name": "Van Halen - Summer Nights .mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Van Halen - Summer Nights .mp3",
                "keydex": "298"
            },
            {
                "name": "Van Halen - Unchained.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Van Halen - Unchained.mp3",
                "keydex": "299"
            },
            {
                "name": "VanHalen - Panama.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/VanHalen - Panama.mp3",
                "keydex": "300"
            },
            {
                "name": "Village People - Kung Fu Fighting.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Village People - Kung Fu Fighting.mp3",
                "keydex": "301"
            },
            {
                "name": "Village People - Macho Man.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Village People - Macho Man.mp3",
                "keydex": "302"
            },
            {
                "name": "Villiage People - YMCA.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Villiage People - YMCA.mp3",
                "keydex": "303"
            },
            {
                "name": "Warrent - Warrant - Cherry pie.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/Warrent - Warrant - Cherry pie.mp3",
                "keydex": "304"
            },
            {
                "name": "We Didn't Start the Fire w_ Lyrics.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/We Didn't Start the Fire w_ Lyrics.mp3",
                "keydex": "305"
            },
            {
                "name": "Wolfmother- Women.mp3",
                "artist": "XYZ",
                "album": "Oldies",
                "url": "./songs/XYZ/Wolfmother- Women.mp3",
                "keydex": "306"
            },
            {
                "name": "Wolsik (Part 4).mp3",
                "artist": "XYZ",
                "album": "XYZ ABC",
                "url": "./songs/XYZ/Wolsik (Part 4).mp3",
                "keydex": "307"
            },
            {
                "name": "Yer a Champ 2.mp3",
                "artist": "TubeX",
                "album": "The Jokes",
                "url": "./songs/XYZ/Yer a Champ 2.mp3",
                "keydex": "308"
            },
            {
                "name": "zombie me (with lyrics).mp3",
                "artist": "XYZ",
                "album": "From You",
                "url": "./songs/XYZ/zombie me (with lyrics).mp3",
                "keydex": "309"
            },
            {
                "name": "ZZ Top - Black Betty.mp3",
                "artist": "XYZ",
                "album": "True Classicdom",
                "url": "./songs/XYZ/ZZ Top - Black Betty.mp3",
                "keydex": "310"
            }
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

