// Index Page JavaScript - Enhanced Futuristic Theme

document.addEventListener("DOMContentLoaded", () => {
  // Animate hero section
  const heroContent = document.querySelector(".hero-content")
  const heroImage = document.querySelector(".hero-image")

  if (heroContent) {
    heroContent.style.opacity = "1"
    heroContent.style.transform = "translateY(0)"
  }

  if (heroImage) {
    setTimeout(() => {
      heroImage.style.opacity = "1"
      heroImage.style.transform = "translateY(0)"
    }, 300)
  }

  // Animate feature cards with staggered delay
  const featureCards = document.querySelectorAll(".feature-card")

  featureCards.forEach((card, index) => {
    setTimeout(
      () => {
        card.style.opacity = "1"
        card.style.transform = "translateY(0)"
      },
      300 + 100 * index,
    )
  })

  // Animate workflow steps with staggered delay
  const workflowSteps = document.querySelectorAll(".workflow-step")

  workflowSteps.forEach((step, index) => {
    setTimeout(
      () => {
        step.style.opacity = "1"
        step.style.transform = "translateX(0)"
      },
      600 + 150 * index,
    )
  })

  // Add interactive hover effects to feature cards
  featureCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-10px)"
      card.style.boxShadow = "var(--glass-shadow), var(--neon-glow)"

      // Highlight icon
      const icon = card.querySelector(".feature-icon")
      if (icon) {
        icon.style.textShadow = "var(--neon-glow), var(--neon-glow)"
        icon.style.transform = "scale(1.1)"
        icon.style.transition = "all 0.3s ease"
      }
    })

    card.addEventListener("mouseleave", () => {
      card.style.transform = "translateY(0)"
      card.style.boxShadow = "var(--glass-shadow)"

      // Reset icon
      const icon = card.querySelector(".feature-icon")
      if (icon) {
        icon.style.textShadow = "var(--neon-glow)"
        icon.style.transform = "scale(1)"
      }
    })
  })

  // Add interactive hover effects to workflow steps
  workflowSteps.forEach((step) => {
    step.addEventListener("mouseenter", () => {
      const number = step.querySelector(".step-number")
      if (number) {
        number.style.transform = "scale(1.1)"
        number.style.boxShadow = "0 0 30px var(--primary-color)"
        number.style.transition = "all 0.3s ease"
      }
    })

    step.addEventListener("mouseleave", () => {
      const number = step.querySelector(".step-number")
      if (number) {
        number.style.transform = "scale(1)"
        number.style.boxShadow = "var(--neon-glow)"
      }
    })
  })

  // Initialize particles.js for the CTA section
  if (document.getElementById("particles-js")) {
    // Check if particlesJS is a function before calling it
    if (typeof particlesJS === "function") {
      particlesJS("particles-js", {
        particles: {
          number: {
            value: 80,
            density: {
              enable: true,
              value_area: 800,
            },
          },
          color: {
            value: "#00c8ff",
          },
          shape: {
            type: "circle",
            stroke: {
              width: 0,
              color: "#000000",
            },
          },
          opacity: {
            value: 0.5,
            random: true,
            anim: {
              enable: true,
              speed: 1,
              opacity_min: 0.1,
              sync: false,
            },
          },
          size: {
            value: 3,
            random: true,
            anim: {
              enable: true,
              speed: 2,
              size_min: 0.1,
              sync: false,
            },
          },
          line_linked: {
            enable: true,
            distance: 150,
            color: "#00c8ff",
            opacity: 0.4,
            width: 1,
          },
          move: {
            enable: true,
            speed: 1,
            direction: "none",
            random: true,
            straight: false,
            out_mode: "out",
            bounce: false,
          },
        },
        interactivity: {
          detect_on: "canvas",
          events: {
            onhover: {
              enable: true,
              mode: "grab",
            },
            onclick: {
              enable: true,
              mode: "push",
            },
            resize: true,
          },
          modes: {
            grab: {
              distance: 140,
              line_linked: {
                opacity: 1,
              },
            },
            push: {
              particles_nb: 4,
            },
          },
        },
        retina_detect: true,
      })
    } else {
      console.warn("particlesJS is not a function. Ensure particles.js library is correctly loaded.")
    }
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()

      const targetId = this.getAttribute("href")
      if (targetId === "#") return

      const targetElement = document.querySelector(targetId)
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80, // Adjust for header height
          behavior: "smooth",
        })
      }
    })
  })

  // Add data point animation
  const dataPoints = document.querySelectorAll(".data-point")
  dataPoints.forEach((point, index) => {
    point.style.animationDelay = `${index * 0.4}s`
  })

  // Add advantage item hover effects
  const advantageItems = document.querySelectorAll(".advantage-item")
  advantageItems.forEach((item) => {
    item.addEventListener("mouseenter", () => {
      item.style.transform = "translateY(-5px)"
      item.style.boxShadow = "var(--neon-glow)"
      item.style.borderColor = "rgba(0, 200, 255, 0.3)"
    })

    item.addEventListener("mouseleave", () => {
      item.style.transform = "translateY(0)"
      item.style.boxShadow = "none"
      item.style.borderColor = "rgba(255, 255, 255, 0.05)"
    })
  })

  // Ensure smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()

      const targetId = this.getAttribute("href")
      if (targetId === "#") return

      const targetElement = document.querySelector(targetId)
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })
})

