document.getElementById("cvForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const content = generateCVContent(formData);
  
    const resultWindow = window.open('', '_blank');
    resultWindow.document.write('<html><head><title>CV Output</title></head><body>' + content + '</body></html>');
  });
  
  function generateCVContent(formData) {
    let content = `<div id="cvOutput"><h1>${formData.get("fullName")}</h1>`;
    content += `<p><strong>Email:</strong> ${formData.get("email")} | <strong>Phone:</strong> ${formData.get("phone")}</p>`;
    content += `<p><strong>GitHub:</strong> ${formData.get("github")} | <strong>Portfolio:</strong> ${formData.get("portfolio")}</p>`;
    content += `<h3>Career Objective</h3><p>${formData.get("objective")}</p>`;
    content += `<h3>Education</h3><p>${formData.get("education")}</p>`;
    content += `<h3>Technical Skills</h3><p>${formData.get("skills")}</p>`;
    content += `<h3>Projects</h3><p>${formData.get("projects")}</p>`;
    content += `<h3>Strengths</h3><p>${formData.get("strengths")}</p>`;
    content += `<h3>Personal Details</h3><p>${formData.get("details")}</p></div>`;
    return content;
  }
  
  function downloadCV() {
    const format = document.getElementById("fileFormat").value;
    const formData = new FormData(document.getElementById("cvForm"));
    const content = generateCVContent(formData);
    const container = document.createElement("div");
    container.innerHTML = content;
    document.body.appendChild(container);
  
    if (format === "pdf") {
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      doc.html(container, {
        callback: function (pdf) {
          pdf.save("cv.pdf");
          document.body.removeChild(container);
        },
        x: 10,
        y: 10
      });
    } else if (format === "png") {
      html2canvas(container.querySelector("#cvOutput")).then(canvas => {
        const link = document.createElement("a");
        link.href = canvas.toDataURL("image/png");
        link.download = "cv.png";
        link.click();
        document.body.removeChild(container);
      });
    } else if (format === "doc") {
      const blob = new Blob([container.innerHTML], { type: "application/msword" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "cv.doc";
      link.click();
      document.body.removeChild(container);
    }
  }
  