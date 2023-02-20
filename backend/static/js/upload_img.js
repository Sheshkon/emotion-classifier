const processing = document.getElementById('processing')
processing.hidden = true

function process(frm) {
    const file = document.getElementById('id_input')
    let upload = document.getElementById('upload')

    upload.type = 'submit'
    if (file.checkValidity()) {
        processing.hidden = false

        frm.submit()
        console.log('processing')
    }
}
