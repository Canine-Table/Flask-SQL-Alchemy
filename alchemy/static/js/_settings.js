#!/usr/bin/node

document.getElementById("SaveChanges_id").addEventListener("click", () => {

    document.getElementById("ShowSavedChanges_id").addEventListener("click", () => {

        document.getElementById("SavedChanges_id").click()

        let first_name = document.getElementById('edit_first_name').value
        let last_name = document.getElementById('edit_last_name').value
        let email_address = document.getElementById('edit_email_address').value
        let phone_number = document.getElementById('edit_phone_number').value

        document.getElementById('first_name').innerHTML = first_name
        document.getElementById('last_name').innerHTML =  last_name
        document.getElementById('email_address').innerHTML = email_address
        document.getElementById('phone_number').innerHTML = phone_number

        document.getElementById("BackSavedChangesConfirmed_id").addEventListener("click", () => {
            document.getElementById("SaveChanges_id").click()
        })

        document.getElementById("SavedChangesConfirmed_id").addEventListener("click", () => {

            let first_name = document.getElementById('edit_first_name').value
            let last_name = document.getElementById('edit_last_name').value
            let full_name = `${first_name} ${last_name}`
            let email_address = document.getElementById('edit_email_address').value
            let phone_number = document.getElementById('edit_phone_number').value

            document.getElementById('full_name_display').innerHTML = ` ${full_name}`
            document.getElementById('email_address_display').innerHTML = ` ${email_address}`
            document.getElementById('phone_number_display').innerHTML = ` ${phone_number}`

        })
    })
})

document.getElementById('save_image_file').addEventListener("click", () => {
    let filename = document.getElementById('selected_image').value
    filename = filename.replace('C:\\fakepath\\','')
    document.getElementById('image_file_path').value = filename
    if(filename != ''){
        document.getElementById('image_form_id').disabled = false
    }
})
