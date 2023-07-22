#!/usr/bin/bash

function fetchQueryLog(){
    document.getElementById('pending_query').value = true
}

function deleteQueryEntry(id){
    console.log(document.getElementById(id))
}
