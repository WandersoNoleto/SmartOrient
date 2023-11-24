var pdfUrl = document.getElementById("pdfUrl").value;

const url = "/media/guidance_articles/ProjetoTCC_-_PartII.pdf";

let doc;
let currentPage = 1;

(async function () {
    pdfjsLib.GlobalWorkerOptions.workerSrc = "/media/pdf.js/build/pdf.worker.js";
    doc = await pdfjsLib.getDocument(url).promise;

    // Renderizar todas as páginas
    for (let i = 1; i <= doc._pdfInfo.numPages; i++) {
        await getPage(doc, i);
    }
})();

async function getPage(doc, pageNumber) {
    if (pageNumber >= 1 && pageNumber <= doc._pdfInfo.numPages) {
        const page = await doc.getPage(pageNumber);

        // Criar um novo contêiner para cada página
        const pageContainer = document.createElement("div");
        pageContainer.className = "pdf-page";

        // Adicionar o contêiner da página ao contêiner principal
        document.getElementById("pdfPages").appendChild(pageContainer);

        // Get the dimensions of the mainContent element
        const mainContent = document.querySelector('.content-wrapper');
        const mainContentRect = mainContent.getBoundingClientRect();

        // Set the viewport based on the dimensions of the mainContent
        const viewport = page.getViewport({ scale: 1 });
        const scale = Math.min(mainContentRect.width / viewport.width, mainContentRect.height / viewport.height);
        const scaledViewport = page.getViewport({ scale });

        // Criar um novo elemento de canvas para cada página
        const canvas = document.createElement("canvas");
        canvas.className = "pdf-canvas";
        pageContainer.appendChild(canvas);

        // Set the canvas dimensions to the scaled viewport dimensions
        const context = canvas.getContext("2d");
        canvas.height = scaledViewport.height;
        canvas.width = scaledViewport.width;

        // Render the PDF page into the canvas context
        await page.render({
            canvasContext: context,
            viewport: scaledViewport
        }).promise;
    } else {
        console.log("Please specify a valid page number");
    }
}
