window.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("imagehandle");
  const submitBtn = document.getElementById("submit-btn");
  const loaderSpan = document.getElementById("loader-span");
  const btnText = document.getElementById("btn-text");
  const outputDiv = document.getElementById("output");
  const formEle = document.getElementById("form-ele");

  formEle.addEventListener("submit", (event) => {
    event.preventDefault();

    // hide the submit button text and show the loader
    btnText.style.display = "none";
    loaderSpan.style.display = "inline-block";

    // create FormData object and append the selected file to it
    const formData = new FormData();
    formData.append("img", fileInput.files[0]);

    // send a POST request to the server with the image data
    fetch("/process_image", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          return response.text();
        } else {
          throw new Error("Network response was not ok");
        }
      })
      .then((text) => {
        // show the processed image and plate number on the page
        outputDiv.innerHTML = text;
        btnText.style.display = "inline-block";
        loaderSpan.style.display = "none";
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});