var pdfUrl = document.getElementById("pdfUrl").value;

const url = pdfUrl;
let doc;
let pdfPages; // Adicione a declaração da variável pdfPages

(async function () {
    pdfjsLib.GlobalWorkerOptions.workerSrc = "/media/pdf.js/build/pdf.worker.js";
    doc = await pdfjsLib.getDocument(url).promise;

    // Renderizar todas as páginas
    for (let i = 1; i <= doc._pdfInfo.numPages; i++) {
        await getPage(doc, i);
    }

    // Inicialize pdfPages após a renderização das páginas
    pdfPages = document.querySelectorAll('.pdf-page');

    // Adicione um ouvinte de evento de rolagem ao elemento principal
    document.getElementById('pdfContainer').addEventListener('scroll', updateCurrentPage);

    // Atualize as informações da página após a renderização
    updatePageInfo();
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
        const mainContent = document.body;
        const mainContentRect = mainContent.getBoundingClientRect();

        // Set the viewport based on the dimensions of the mainContent
        const viewport = page.getViewport({ scale: 0.6 });
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

function updatePageInfo() {
  const container = document.getElementById('pdfContainer');
  const scrollTop = container.scrollTop;

  const containerHeight = container.offsetHeight;
  const totalHeight = container.scrollHeight;
  const partHeight = totalHeight / pdfPages.length;

  // Ajuste para garantir que currentPage esteja dentro dos limites válidos
  currentPage = Math.min(Math.max(1, Math.ceil(scrollTop / partHeight)), doc._pdfInfo.numPages);

  document.getElementById('currentPage').textContent = currentPage.toString();
  document.getElementById('totalPages').textContent = doc._pdfInfo.numPages.toString();
}




function updateCurrentPage() {
  const scrollTop = document.getElementById('pdfContainer').scrollTop;
  const containerHeight = document.getElementById('pdfContainer').offsetHeight;
  const partHeight = containerHeight / pdfPages.length;
  currentPage = Math.floor(scrollTop / partHeight) + 1;

  updatePageInfo(currentPage);
}
