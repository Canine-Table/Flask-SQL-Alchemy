#!/usr/bin/node


document.getElementById("SaveChanges_id").addEventListener("click", () => {
    $('#ShowSavedChanges_id').prop('disabled', false);
    document.getElementById("ShowSavedChanges_id").addEventListener("click", () => {

        $("#SavedChanges_id").click();
        let first_name = $('#edit_first_name').val();
        let last_name = $('#edit_last_name').val();
        let email_address = $('#edit_email_address').val();
        let phone_number = $('#edit_phone_number').val();

        $('#first_name').html(first_name);
        $('#last_name').html(last_name);
        $('#email_address').html(email_address);
        $('#phone_number').html(phone_number);

        document.getElementById("BackSavedChangesConfirmed_id").addEventListener("click", () => {
            $("#SaveChanges_id").click();
            $('#BackSavedChangesConfirmed_id').prop('disabled', true);
            $('#ShowSavedChanges_id').prop('disabled', false);
        });

        document.getElementById("SavedChangesConfirmed_id").addEventListener("click", () => {

            let first_name = $('#edit_first_name').val();
            let last_name = $('#edit_last_name').val();
            let full_name = `${first_name} ${last_name}`;
            let email_address = $('#edit_email_address').val();
            let phone_number = $('#edit_phone_number').val();

            $('#full_name_display').html(` ${full_name}`);
            $('#email_address_display').html(` ${email_address}`);
            $('#phone_number_display').html(` ${phone_number}`);
            $('#SavedChangesConfirmed_id').prop('disabled', true);
        });

        $('#ShowSavedChanges_id').prop('disabled', true);
        $('#SavedChangesConfirmed_id').prop('disabled', false);
        $('#BackSavedChangesConfirmed_id').prop('disabled', false);

    });
});




document.getElementById('save_image_file').addEventListener("click", () => {
    let filename = $('#selected_image').val();
    filename = filename.replace('C:\\fakepath\\','');
    $('#image_file_path').val(filename);
    if(filename != ''){
        $('#image_form_id').prop('disabled', false);
        document.getElementById('image_form_id').addEventListener("click", () => {
            $('#image_form_id').prop('disabled', true);
        })

    }

})




document.getElementById('resetYourPassword_id').addEventListener("click", () => {
    $('#confirmResetingYourPassword_id').prop('disabled', false);
    document.getElementById('confirmResetingYourPassword_id').addEventListener("click", () => {
        $('#confirmResetingYourPassword_id').prop('disabled', true);
    })

})


document.getElementById('deletingAccount_id').addEventListener("click", () => {
    $('#confirmDeletingAccount_id').prop('disabled', false);
    document.getElementById('confirmDeletingAccount_id').addEventListener("click", () => {
        $('#confirmDeletingAccount_id').prop('disabled', true);
    })
})
