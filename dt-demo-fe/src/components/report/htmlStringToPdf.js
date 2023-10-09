import html2canvas from "html2canvas";
import jsPDF from "jspdf";

const HtmlStringToPdf = async (htmlString, pdfRef) => {
    let iframe = document.createElement("iframe");
    iframe.style.visibility = "hidden";
    document.body.appendChild(iframe);
    let iframedoc = iframe.contentDocument || iframe.contentWindow.document;
    iframedoc.body.innerHTML = htmlString;

    let canvas = await html2canvas(iframedoc.body, {
        windowWidth: 800,
    });
    let imgData = canvas.toDataURL("image/png");

    const doc = new jsPDF({
        format: "a4",
        unit: "mm",
    });

    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();

    const widthRatio = pageWidth / canvas.width;
    const customHeight = canvas.height * widthRatio;

    doc.addImage(imgData, "png", 0, 0, pageWidth, customHeight);

    let heightLeft = customHeight;
    let heightAdd = -pageHeight;

    // over 1 page
    while (heightLeft >= pageHeight) {
        doc.addPage();
        doc.addImage(imgData, "png", 0, heightAdd, pageWidth, customHeight);
        heightLeft -= pageHeight;
        heightAdd -= pageHeight;
    }

    let pdfBlob = doc.output("blob");
    pdfRef.current.src = URL.createObjectURL(pdfBlob);

    return pdfRef;
};

export default HtmlStringToPdf;
