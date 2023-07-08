#!/usr/bin/node

document.getElementById("SaveChanges_id").addEventListener("click", () => {

    let first_name = document.getElementById('inputGroupPrepend40').value
    let last_name = document.getElementById('inputGroupPrepend41').value
    let email_address = document.getElementById('inputGroupPrepend50').value
    let phone_number = document.getElementById('inputGroupPrepend60').value

    document.getElementById('first_name').innerHTML = first_name
    document.getElementById('last_name').innerHTML =  last_name
    document.getElementById('email_address').innerHTML = email_address
    document.getElementById('phone_number').innerHTML = phone_number

})
