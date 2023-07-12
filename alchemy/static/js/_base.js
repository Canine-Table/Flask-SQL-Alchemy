#!/usr/bin/node

document.getElementById("SaveChanges_id").addEventListener("click", () => {

    document.getElementById("ShowSavedChanges_id").addEventListener("click", () => {

        document.getElementById("SavedChanges_id").click()

        let first_name = document.getElementById('inputGroupPrepend40').value
        let last_name = document.getElementById('inputGroupPrepend41').value
        let email_address = document.getElementById('inputGroupPrepend50').value
        let phone_number = document.getElementById('inputGroupPrepend60').value

        document.getElementById('first_name').innerHTML = first_name
        document.getElementById('last_name').innerHTML =  last_name
        document.getElementById('email_address').innerHTML = email_address
        document.getElementById('phone_number').innerHTML = phone_number

        document.getElementById("BackSavedChangesConfirmed_id").addEventListener("click", () => {
            document.getElementById("SaveChanges_id").click()
        })

        document.getElementById("SavedChangesConfirmed_id").addEventListener("click", () => {

            let first_name = document.getElementById('inputGroupPrepend40').value
            let last_name = document.getElementById('inputGroupPrepend41').value
            let full_name = `${first_name} ${last_name}`
            let email_address = document.getElementById('inputGroupPrepend50').value
            let phone_number = document.getElementById('inputGroupPrepend60').value

            document.getElementById('full_name_display').innerHTML = ` ${full_name}`
            document.getElementById('email_address_display').innerHTML = ` ${email_address}`
            document.getElementById('phone_number_display').innerHTML = ` ${phone_number}`

        })
    })
})
