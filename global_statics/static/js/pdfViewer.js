// No seu arquivo pdfViewer.js

// Importando o módulo inteiro (não apenas PDFViewer)
import pdfjsLib from 'https://cdn.jsdelivr.net/npm/pdfjs-dist@4.0.189/+esm';

const pdfPath = document.getElementById('pdf-path').value;
console.log(pdfPath)

var loadingTask = pdfjsLib.getDocument(pdfPath);


loadingTask.promise.then(function(pdf) {
  console.log("ESTOU AQUI");
});