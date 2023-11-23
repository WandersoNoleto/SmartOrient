from django.shortcuts import get_object_or_404, render

from library.models import GuidanceArticle


def view_pdf(request, id):
    article = get_object_or_404(GuidanceArticle, id=id)

    context = {
        'article': article,
        'article_path': article.file.path
    }

    return render(request, "pdfViewer.html", context)