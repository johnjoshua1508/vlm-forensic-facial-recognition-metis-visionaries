// Evaluation JavaScript - Futuristic Theme

document.addEventListener("DOMContentLoaded", () => {
    // Tab switching with animation
    const tabButtons = document.querySelectorAll(".tab-button")
    const tabPanes = document.querySelectorAll(".tab-pane")
  
    tabButtons.forEach((button) => {
      button.addEventListener("click", function () {
        // Remove active class from all buttons and panes
        tabButtons.forEach((btn) => btn.classList.remove("active"))
        tabPanes.forEach((pane) => {
          pane.classList.remove("active")
          pane.style.display = "none"
        })
  
        // Add active class to clicked button and corresponding pane
        this.classList.add("active")
        const tabId = this.getAttribute("data-tab")
        const activePane = document.getElementById(tabId + "-tab")
  
        // Fade in animation
        setTimeout(() => {
          activePane.style.display = "block"
          activePane.classList.add("active")
        }, 50)
      })
    })
  
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
  
    // Handle range sliders with visual feedback
    const sliders = document.querySelectorAll(".slider")
  
    sliders.forEach((slider) => {
      const valueDisplay = slider.nextElementSibling
  
      // Set initial value
      if (valueDisplay && valueDisplay.classList.contains("slider-value")) {
        valueDisplay.textContent = slider.value
      }
  
      // Update value on change with visual feedback
      slider.addEventListener("input", function () {
        if (valueDisplay && valueDisplay.classList.contains("slider-value")) {
          valueDisplay.textContent = this.value
  
          // Add pulse animation
          valueDisplay.style.animation = "none"
          setTimeout(() => {
            valueDisplay.style.animation = "pulse 0.5s ease"
          }, 10)
        }
      })
    })
  
    // Animate metrics cards with staggered delay
    const metricCards = document.querySelectorAll(".metric-card")
  
    metricCards.forEach((card, index) => {
      card.style.opacity = "0"
      card.style.transform = "translateY(20px)"
  
      setTimeout(() => {
        card.style.transition = "opacity 0.5s ease, transform 0.5s ease"
        card.style.opacity = "1"
        card.style.transform = "translateY(0)"
      }, 100 * index)
    })
  })
  
  