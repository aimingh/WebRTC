'use strict';
var configuration = null;
// var roomURL = document.getElementById('url');
//html 에 있는 객체에 대한 참조를 가져온다. 
var video = document.querySelector('video'); //비디오 
var photo = document.getElementById('photo'); //사진 
var photoContext = photo.getContext('2d');   
var photoContextW;
var photoContextH;

/****************************************************************************
* User media (webcam)
****************************************************************************/
function grabWebCamVideo() {
  console.log('Getting user media (video) ...');
  
  //비동기 모드, 장치에 대한 접근이 허용되면  then 이하가 실행된다.
  //Initializes media stream. 
  navigator.mediaDevices.getUserMedia({
    audio: false,
    video: true  //비디오만 
  })
  .then(gotStream)  //스트립을 처리할 함수의 주소를 전달한다
  .catch(function(e) {
    alert('getUserMedia() error: ' + e.name);
  });
}

function gotStream(stream) {
  //여기서 스트림을 처리한다 
  console.log('getUserMedia video stream URL:', stream);
  window.stream = stream; // stream available to console
  video.srcObject = stream;
  //비디오가 준비가 되면 이
  video.onloadedmetadata = function() {
    photo.width = photoContextW = video.videoWidth;
    photo.height = photoContextH = video.videoHeight;
    console.log('gotStream with width and height:', photoContextW, photoContextH);
  };
  show(toggleBtn);
}

/****************************************************************************
* Aux functions, mostly UI-related
****************************************************************************/
function show() {
  Array.prototype.forEach.call(arguments, function(elem) {
    elem.style.display = null;
  });
}

function snapPhoto() {
  photoContext.drawImage(video, 0, 0, photo.width, photo.height);
  show(photo, toggleBtn);
}

//=========================================================================================================
// 추가
//=========================================================================================================
// 영상 저장 부분 http://127.0.0.1:8000/
//=========================================================================================================
var toggleBtn = document.getElementById('toggle');     // 기록 토글 버튼
var t = false;  // 토글 플레그
var recordId;

// 버튼 클릭시 이벤트 발생
toggleBtn.addEventListener('click', toggleRecord);  // 토글 이벤트리스너

function toggleRecord(){
  t = !t;
  if (t == true) startrecordBtnPhoto();
  else endrecordBtnPhoto();
}

function startrecordBtnPhoto() {
  var interval = document.getElementById('interval');
  var groupnameArea = document.getElementById('groupname');
  var dronenameArea = document.getElementById('dronename');
  // 기록 되는 동안 설정 바뀌지 않도록 비활성화
  interval.disabled = true;
  groupnameArea.disabled = true;
  dronenameArea.disabled = true;
  recordId = setInterval(record, 1000*interval.value);
}

function endrecordBtnPhoto() {
  if(recordId != null) {
    var interval = document.getElementById('interval');
    var groupnameArea = document.getElementById('groupname');
    var dronenameArea = document.getElementById('dronename');
    // 기록 종료 후 활성화
    interval.disabled = false;
    groupnameArea.disabled = false;
    dronenameArea.disabled = false;
    clearInterval(recordId);
  }
}

function record() {
  console.log('record start');
  snapPhoto();
  getGPS();
}

function getGPS(){
  navigator.geolocation.getCurrentPosition(function(pos) {
    var latitude = pos.coords.latitude;
    var longitude = pos.coords.longitude;
    getAdress(latitude, longitude);
    console.log('GPS');
    console.log(latitude + ', ' + longitude);
  });

}

function getAdress(latitude, longitude){
  $.ajax({
    type: "POST",
    headers:{"Authorization":'KakaoAK e872972db3d44f41a166d59a90196511'},
    url: "https://dapi.kakao.com/v2/local/geo/coord2address.json?x=" + longitude + "&y=" + latitude + "&input_coord=WGS84",  //받아서 저장하자 
  }).done(function(msg){ 
    // console.log(msg);
    var address = msg
    console.log(address['documents'][0]['address']['address_name']);
    sendPhoto(latitude, longitude, address)
  })
}

function sendPhoto(latitude, longitude, address){
  var groupname = document.getElementById('groupname').value;
  var dronename = document.getElementById('dronename').value;
  var dataURL = photo.toDataURL();
  $.ajax({
     type: "POST", 
     url:'/start',
     data: {'img': dataURL, 'latitude':latitude, 'longitude':longitude, 'address':address, 'groupname':groupname, 'dronename':dronename }      
  }).done(function(msg){ 
     console.log('ajax 전송'); 
  });
}
//=========================================================================================================
//=========================================================================================================
