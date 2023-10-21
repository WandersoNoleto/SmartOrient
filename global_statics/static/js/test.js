// Url do arquivo pdf
var url = 'media/HIstoricoParcial.pdf';

// Carrega via <script> tag, cria endereço para acesso ao PDF.js exports.
var pdfjsLib = window['media/pdf.js/build/pdf.js'];


// Asynchronous download do PDF
var loadingTask = pdfjsLib.getDocument(url);

function renderizaPagina(pageNumber) {

    loadingTask.promise.then(function(pdf) {
        console.log('PDF loaded');
       
        // Pega primeira page
        pdf.getPage(pageNumber).then(function(page) {
        console.log('Page loaded: '+ pageNumber );
        
        var scale = 1.5;
        var viewport = page.getViewport({scale: scale});

        // Prepara canvas usando as dimensões da página PDF
        var canvas = document.getElementById('the-canvas');
        var context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // Renderiza página PDF para canvas 
        var renderContext = {
        canvasContext: context,
        viewport: viewport
        };
        var renderTask = page.render(renderContext);

            renderTask.promise.then(function () {
            console.log('Página renderizada!');
        });
    });
    }, function (reason) {
    // Mostra erro
    console.error(reason);
    });

}

var pageNumber = 1;
//mostra a primeira página do arquivo pdf
pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
    pdfDoc = pdfDoc_;
    document.getElementById('page_count').textContent = pdfDoc.numPages;
    document.getElementById('page_num').textContent = pageNumber;  
 
    // Chamando a renderizacao da página 1
    renderizaPagina(pageNumber);
  });