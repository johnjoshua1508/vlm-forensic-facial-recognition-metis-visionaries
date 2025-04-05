// Results Page JavaScript - Forensic Face Recognition System

document.addEventListener("DOMContentLoaded", () => {
  // Store all result data for modal display
  const resultData = []

  // Collect data from all result cards
  document.querySelectorAll(".result-card").forEach((card) => {
    // Get subject ID and distance
    const subjectId = card.getAttribute("data-subject-id")
    const distance = card.getAttribute("data-distance")

    // Store data for this result
    const resultItem = {
      subjectId: subjectId,
      image: card.querySelector(".result-image img").src,
      distance: distance,
    }

    // Add metadata if available
    if (card.hasAttribute("data-metadata")) {
      try {
        resultItem.metadata = JSON.parse(card.getAttribute("data-metadata"))
      } catch (e) {
        console.error("Error parsing metadata:", e)
      }
    }

    resultData.push(resultItem)

    // Add click event to show modal
    card.addEventListener("click", () => {
      showSubjectDetails(subjectId)
    })
  })

  // Modal elements
  const modal = document.getElementById("subjectDetailModal")
  const backdrop = document.getElementById("modalBackdrop")
  const closeBtn = modal.querySelector(".modal-close")

  // Close modal when clicking the close button
  closeBtn.addEventListener("click", closeModal)

  // Close modal when clicking outside
  backdrop.addEventListener("click", closeModal)

  // Function to show subject details in modal
  function showSubjectDetails(subjectId) {
    // Find the result data for this subject
    const result = resultData.find((item) => item.subjectId === subjectId)
    if (!result) return

    // Set modal content
    document.getElementById("modalImage").src = result.image
    document.getElementById("modalDistance").textContent = result.distance
    document.getElementById("modalSubjectId").textContent = `SUBJECT ID: ${result.subjectId}`

    // Show modal first to avoid layout issues
    modal.classList.add("active")
    backdrop.classList.add("active")

    // Prevent body scrolling
    document.body.style.overflow = "hidden"

    // Fetch additional details via AJAX
    fetch(`/subject/${subjectId}/details`)
      .then((response) => response.json())
      .then((data) => {
        // Fill in the details
        document.getElementById("modalSex").textContent = data.Sex || "Unknown"
        document.getElementById("modalHeight").textContent = data.Height || "Unknown"
        document.getElementById("modalWeight").textContent = data.Weight || "Unknown"
        document.getElementById("modalHair").textContent = data.Hair || "Unknown"
        document.getElementById("modalEyes").textContent = data.Eyes || "Unknown"
        document.getElementById("modalRace").textContent = data.Race || "Unknown"
        document.getElementById("modalSexOffender").textContent = data["Sex Offender"] || "Unknown"
        document.getElementById("modalOffense").textContent = data.Offense || "None"
      })
      .catch((error) => {
        console.error("Error fetching subject details:", error)
        // Fallback to using metadata if available
        if (result.metadata) {
          document.getElementById("modalSex").textContent = result.metadata.Sex || "Unknown"
          document.getElementById("modalHeight").textContent = result.metadata.Height || "Unknown"
          document.getElementById("modalWeight").textContent = result.metadata.Weight || "Unknown"
          document.getElementById("modalHair").textContent = result.metadata.Hair || "Unknown"
          document.getElementById("modalEyes").textContent = result.metadata.Eyes || "Unknown"
          document.getElementById("modalRace").textContent = result.metadata.Race || "Unknown"
          document.getElementById("modalSexOffender").textContent = result.metadata["Sex Offender"] || "Unknown"
          document.getElementById("modalOffense").textContent = result.metadata.Offense || "None"
        }
      })
  }

  // Function to close modal
  function closeModal() {
    modal.classList.remove("active")
    backdrop.classList.remove("active")

    // Re-enable body scrolling
    document.body.style.overflow = ""
  }

  // Add keyboard support for closing modal with Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) {
      closeModal()
    }
  })

  // Animate result cards with staggered delay
  const resultCards = document.querySelectorAll(".result-card")

  resultCards.forEach((card, index) => {
    setTimeout(() => {
      card.style.opacity = "1"
      card.style.transform = "translateY(0)"
    }, 100 * index)
  })

  // Add interactive hover effects to result cards
  resultCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      // Enhance glow effect
      card.style.boxShadow = "var(--glass-shadow), 0 0 30px rgba(0, 200, 255, 0.4)"

      // Scale up image slightly
      const image = card.querySelector(".result-image img")
      if (image) {
        image.style.transform = "scale(1.05)"
        image.style.transition = "transform 0.3s ease"
      }

      // Highlight score badge
      const badge = card.querySelector(".score-badge")
      if (badge) {
        badge.style.boxShadow = "0 0 20px var(--primary-color)"
        badge.style.transition = "box-shadow 0.3s ease"
      }
    })

    card.addEventListener("mouseleave", () => {
      // Reset effects
      card.style.boxShadow = "var(--glass-shadow)"

      const image = card.querySelector(".result-image img")
      if (image) {
        image.style.transform = "scale(1)"
      }

      const badge = card.querySelector(".score-badge")
      if (badge) {
        badge.style.boxShadow = "var(--neon-glow)"
      }
    })
  })

  // Animate search info section
  const searchInfo = document.querySelector(".search-info-bar")
  if (searchInfo) {
    searchInfo.style.opacity = "0"
    searchInfo.style.transform = "translateY(-10px)"

    setTimeout(() => {
      searchInfo.style.transition = "opacity 0.5s ease, transform 0.5s ease"
      searchInfo.style.opacity = "1"
      searchInfo.style.transform = "translateY(0)"
    }, 300)
  }

  // Log to confirm script is running
  console.log("Results script initialized")
})

