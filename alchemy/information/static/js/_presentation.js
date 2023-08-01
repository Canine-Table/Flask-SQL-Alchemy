#!/bin/usr/node

const qualityQueries = document.getElementById('qualityQueries');

function getRandomNumber(min,max){
    return Math.floor(Math.random() * (max - min + 1) ) + min;
}

function getHeight(){
    return qualityQueries.clientHeight - 25;
}

function getWidth(){
    return qualityQueries.clientWidth - 25;
}

function resetX(){
    return getRandomNumber(48,getWidth());
}

function resetY(){
    return getRandomNumber(48,getHeight());
}

class mysqlAnimation {

    constructor(){
        this.object = document.createElement("div");
        this.object.classList.add('mySqlImage');
        this.x = resetX();
        this.y = resetY();
        this.xDirection = this.x % 2 == 0 ? -1 : 1;
        this.yDirection = this.y % 2 == 0 ? -1 : 1;
        new Map([
                ["height", "32px"],
                ["width", "32px"],
                ["position", "absolute"],
                ["top", `${this.x}px`],
                ["left", `${this.y}px`],
            ]).forEach((value, key) => {
                this.object.style[key] = value;
        })
        qualityQueries.appendChild(this.object);
    }

    /**
     * @param {{ y: any; }} div
     */

    get getY(){
        return resetY();
    }


    /**
     * @param {{ x: any; }} div
    */

    get getX(){
        return resetX();
    }

}

for(let i=0;i<50;i++){
    setInterval(frame, 20, new mysqlAnimation());
}

function frame(movingDiv){

    movingDiv.x = movingDiv.x + movingDiv.xDirection;
    movingDiv.y = movingDiv.y + movingDiv.yDirection;

    if(movingDiv.x >= getWidth() - 7){
        movingDiv.xDirection = -1;
    }

    if(movingDiv.x <= 0){
        movingDiv.xDirection = 1;
    }

    if(movingDiv.x < 0 || movingDiv.x > getWidth())
        movingDiv.x = movingDiv.getX;

    if(movingDiv.y >= getHeight() - 7){
        movingDiv.yDirection = -1;
    }

    if(movingDiv.y <= 0){
        movingDiv.yDirection = 1;
    }

    if(movingDiv.y < 0 || movingDiv.y > getHeight()){
        movingDiv.y = movingDiv.getY;
    }

    movingDiv.object.style.top = movingDiv.y + "px";
    movingDiv.object.style.left = movingDiv.x + "px";
}




