// Add Subject JavaScript - Futuristic Theme

document.addEventListener("DOMContentLoaded", () => {
  // File upload preview with enhanced visual feedback
  const fileInputs = document.querySelectorAll('input[type="file"]')

  fileInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const preview = this.closest(".file-upload").querySelector(".file-preview")

      if (preview) {
        preview.innerHTML = ""

        if (this.files && this.files[0]) {
          const reader = new FileReader()

          reader.onload = (e) => {
            const img = document.createElement("img")
            img.src = e.target.result
            img.alt = "Preview"
            img.style.opacity = "0"
            preview.appendChild(img)

            // Fade in animation for image
            setTimeout(() => {
              img.style.transition = "opacity 0.3s ease"
              img.style.opacity = "1"
            }, 50)
          }

          reader.readAsDataURL(this.files[0])

          // Add file name with animation
          const fileName = document.createElement("p")
          fileName.textContent = this.files[0].name
          fileName.classList.add("file-name")
          fileName.style.color = "var(--primary-color)"
          fileName.style.marginTop = "10px"
          fileName.style.opacity = "0"
          preview.appendChild(fileName)

          setTimeout(() => {
            fileName.style.transition = "opacity 0.3s ease"
            fileName.style.opacity = "1"
          }, 100)
        }
      }
    })
  })

  // Drag and drop for file uploads with enhanced visual feedback
  const fileUploads = document.querySelectorAll(".file-upload")

  fileUploads.forEach((upload) => {
    const input = upload.querySelector('input[type="file"]')
    const label = upload.querySelector(".file-upload-label")
    ;["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
      upload.addEventListener(eventName, preventDefaults, false)
    })

    function preventDefaults(e) {
      e.preventDefault()
      e.stopPropagation()
    }
    ;["dragenter", "dragover"].forEach((eventName) => {
      upload.addEventListener(eventName, highlight, false)
    })
    ;["dragleave", "drop"].forEach((eventName) => {
      upload.addEventListener(eventName, unhighlight, false)
    })

    function highlight() {
      upload.classList.add("highlight")
      upload.style.boxShadow = "var(--neon-glow)"
      upload.style.borderColor = "var(--primary-color)"
    }

    function unhighlight() {
      upload.classList.remove("highlight")
      upload.style.boxShadow = ""
      upload.style.borderColor = ""
    }

    upload.addEventListener("drop", handleDrop, false)

    function handleDrop(e) {
      const dt = e.dataTransfer
      const files = dt.files

      if (files.length > 0) {
        input.files = files

        // Trigger change event
        const event = new Event("change", { bubbles: true })
        input.dispatchEvent(event)
      }
    }
  })

  // Form validation with enhanced visual feedback
  const form = document.querySelector(".add-subject-form")

  if (form) {
    form.addEventListener("submit", (e) => {
      const frontImage = document.getElementById("front_image")
      const sideImage = document.getElementById("side_image")

      let isValid = true

      if (!frontImage.files || frontImage.files.length === 0) {
        e.preventDefault()
        isValid = false

        // Visual feedback for error
        const frontUpload = frontImage.closest(".file-upload")
        frontUpload.style.borderColor = "var(--danger-color)"
        frontUpload.style.boxShadow = "0 0 10px var(--danger-color)"

        // Reset after delay
        setTimeout(() => {
          frontUpload.style.borderColor = ""
          frontUpload.style.boxShadow = ""
        }, 2000)
      }

      if (!sideImage.files || sideImage.files.length === 0) {
        e.preventDefault()
        isValid = false

        // Visual feedback for error
        const sideUpload = sideImage.closest(".file-upload")
        sideUpload.style.borderColor = "var(--danger-color)"
        sideUpload.style.boxShadow = "0 0 10px var(--danger-color)"

        // Reset after delay
        setTimeout(() => {
          sideUpload.style.borderColor = ""
          sideUpload.style.boxShadow = ""
        }, 2000)
      }

      if (!isValid) {
        // Create a floating error message
        const errorMsg = document.createElement("div")
        errorMsg.textContent = "Please upload both front and side images"
        errorMsg.style.position = "fixed"
        errorMsg.style.top = "20px"
        errorMsg.style.left = "50%"
        errorMsg.style.transform = "translateX(-50%)"
        errorMsg.style.backgroundColor = "rgba(239, 71, 111, 0.9)"
        errorMsg.style.color = "white"
        errorMsg.style.padding = "10px 20px"
        errorMsg.style.borderRadius = "5px"
        errorMsg.style.zIndex = "9999"
        errorMsg.style.boxShadow = "0 0 20px rgba(239, 71, 111, 0.5)"
        document.body.appendChild(errorMsg)

        // Remove after 3 seconds
        setTimeout(() => {
          errorMsg.style.opacity = "0"
          errorMsg.style.transition = "opacity 0.5s ease"
          setTimeout(() => {
            document.body.removeChild(errorMsg)
          }, 500)
        }, 3000)
      }
    })

    form.addEventListener("submit", function (e) {
      // Get feet and inches values
      const feet = document.getElementById("height_feet").value || "0"
      const inches = document.getElementById("height_inches").value || "0"

      // Create a hidden input to store the combined height value
      const heightInput = document.createElement("input")
      heightInput.type = "hidden"
      heightInput.name = "height"
      heightInput.value = `${feet} ft. ${inches.padStart(2, "0")} in.`

      // Add the hidden input to the form
      this.appendChild(heightInput)
    })
  }

  // Add animation to form sections
  const formSections = document.querySelectorAll(".form-section")

  formSections.forEach((section, index) => {
    section.style.opacity = "0"
    section.style.transform = "translateY(20px)"

    setTimeout(() => {
      section.style.transition = "opacity 0.5s ease, transform 0.5s ease"
      section.style.opacity = "1"
      section.style.transform = "translateY(0)"
    }, 200 * index)
  })
})

