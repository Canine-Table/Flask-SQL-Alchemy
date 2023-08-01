#!/usr/bin/bash

function fetchQueryLog(md5_hash){
    $('#pending_query_id').val('fetchQueryLog')
    $('#md5_hash_id').val(md5_hash)
    $("input[name='inlineRadioOptions'][value='query_query_dump']").prop('checked', true)
    $('#submit_query_choice').click()
}

function deleteQueryEntry(md5_hash,file_path,radio_option){
    $('#pending_query_id').val('deleteQueryEntry')
    $('#md5_hash_id').val(md5_hash)
    $('#file_path_id').val(file_path)
    if(radio_option === 'query_query_dump'){
        $("input[name='inlineRadioOptions'][value='query_query_dump']").prop('checked', true)
    } else if(radio_option === 'query_error_dump'){
        $("input[name='inlineRadioOptions'][value='query_error_dump']").prop('checked', true)
    }
    $('#submit_query_choice').click()
}

function loadForm(form){
    import("../../../static/js/_forms.mjs").then(module => {
      const loadingForm = module.loadingForm;
      return loadingForm(form);
    });
}