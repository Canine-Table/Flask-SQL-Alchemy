#!/usr/bin/node

document.getElementById('paddingDiv').classList.remove('container-fluid');

function dateDisplay() {
    let setDate = document.getElementById('DateandTime');
    let date = new Date();
    let hours = date.getHours();
    let hour = hours > 12 ? hours % 12 : hours
    let amPM = hours < 12 ? 'AM' : 'PM';
    let minutes = date.getMinutes();
    let minute = minutes <= 9 ? '0' + minutes : minutes;
    let seconds = date.getSeconds();
    let second = seconds <= 9 ? '0' + seconds : seconds;
    let year = date.getFullYear()
    let months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    let month = date.getMonth()
    let weeks = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    let week = date.getDay();
    let day = date.getDate();
    setDate.innerText = `${weeks[week]}, ${months[month]} ${day}, ${year}, ${hour}:${minute}:${second} ${amPM}`
}

setInterval(dateDisplay, 1000);
