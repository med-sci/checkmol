function hideElement (element) {
    element.style.display = "none"
}

function showElement (element) {
    element.style.display = "block"
}


const smilesArea = document.getElementById("smilesArea")
const mainSpinner = document.getElementById("mainSpinner")
const mainButton = document.getElementById("mainButton")
const smilesAreaButton = document.getElementById("smilesAreaButton")
const results = document.getElementById("results")

mainButton.addEventListener("click", () => {
    hideElement(mainButton)
    showElement(smilesArea)
})

smilesAreaButton.addEventListener("click", () => {
    hideElement(smilesAreaButton)
    showElement(mainSpinner)
    hideElement(mainSpinner)
    showElement(results)
})

