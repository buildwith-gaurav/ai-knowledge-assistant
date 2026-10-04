const uploadBtn = document.getElementById("uploadBtn");
const askBtn = document.getElementById("askBtn");

const pdfFile = document.getElementById("pdfFile");
const questionInput = document.getElementById("question");

const uploadStatus = document.getElementById("uploadStatus");
const answerBox = document.getElementById("answer");
const sourcesList = document.getElementById("sources");


/* =========================
   PDF UPLOAD
========================= */

uploadBtn.addEventListener("click", async () => {

    const file = pdfFile.files[0];

    if (!file) {
        uploadStatus.textContent = "Please select a PDF first.";
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    uploadStatus.textContent = "Uploading and processing...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (data.error) {
            uploadStatus.textContent = data.error;
            return;
        }

        uploadStatus.textContent =
            `${data.filename} uploaded successfully. ${data.chunks} chunks created.`;

    } catch (error) {

        uploadStatus.textContent =
            "Could not connect to the backend.";

        console.error(error);
    }
});


/* =========================
   ASK QUESTION
========================= */

askBtn.addEventListener("click", async () => {

    const question = questionInput.value.trim();

    if (!question) {
        answerBox.textContent = "Please enter a question.";
        return;
    }

    answerBox.textContent = "Thinking...";
    sourcesList.innerHTML = "";

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/chat?question=${encodeURIComponent(question)}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (data.error) {
            answerBox.textContent = data.error;
            return;
        }

        answerBox.textContent = data.answer;

        data.sources.forEach(source => {

            const li = document.createElement("li");

            li.textContent = source;

            sourcesList.appendChild(li);
        });

    } catch (error) {

        answerBox.textContent =
            "Could not connect to the backend.";

        console.error(error);
    }
});