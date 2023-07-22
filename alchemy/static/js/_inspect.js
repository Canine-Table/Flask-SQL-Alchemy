#!/usr/bin/bash

function fetchQueryLog(md5_hash){
    $('#pending_query_id').val('True')
    $('#md5_hash_id').val(md5_hash)
}

function deleteQueryEntry(md5_hash){
    console.log(md5_hash)
}
