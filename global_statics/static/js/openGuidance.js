function displayFileNameModal() {
    var input      = document.getElementById('file-upload-modal');
    var display    = document.getElementById('selectedFileNameModal');
    var titleInput = document.getElementById('title-input');

    if (input.files.length > 0) {
        if (!input.files[0].name.toLowerCase().endsWith('.pdf')) {
            alert('Por favor, selecione um arquivo PDF válido.');
            input.value = '';
            display.textContent = '';
        } else {
            display.textContent = 'Arquivo Selecionado: ' + input.files[0].name;
            titleInput.value = input.files[0].name;
        }
    } else {
        display.textContent = '';
    }
}

function openFileUploadModal() {
    $('#fileUploadModal').modal('show');
}

function submitFormModal() {
    document.getElementById('uploadForm').submit();
}