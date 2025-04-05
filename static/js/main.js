// Main JavaScript for Forensic Face Recognition System - Futuristic Theme

// Close flash messages
document.addEventListener("DOMContentLoaded", () => {
    const closeButtons = document.querySelectorAll(".flash-message .close-btn")
  
    closeButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const flashMessage = this.closest(".flash-message")
        flashMessage.style.opacity = "0"
        setTimeout(() => {
          flashMessage.style.display = "none"
        }, 300)
      })
    })
  
    // Auto-hide flash messages after 5 seconds
    setTimeout(() => {
      const flashMessages = document.querySelectorAll(".flash-message")
      flashMessages.forEach((message) => {
        message.style.opacity = "0"
        setTimeout(() => {
          message.style.display = "none"
        }, 300)
      })
    }, 5000)
  
    // Add futuristic cursor effect
    const cursor = document.createElement("div")
    cursor.classList.add("cursor-fx")
    document.body.appendChild(cursor)
  
    document.addEventListener("mousemove", (e) => {
      cursor.style.left = e.clientX + "px"
      cursor.style.top = e.clientY + "px"
    })
  
    // Add hover effect for interactive elements
    const interactiveElements = document.querySelectorAll("a, button, input, select, textarea, .btn")
  
    interactiveElements.forEach((element) => {
      element.addEventListener("mouseenter", () => {
        cursor.classList.add("cursor-hover")
      })
  
      element.addEventListener("mouseleave", () => {
        cursor.classList.remove("cursor-hover")
      })
    })
  
    // Handle range sliders
    const sliders = document.querySelectorAll(".slider")
  
    sliders.forEach((slider) => {
      const valueDisplay = slider.nextElementSibling
  
      // Set initial value
      if (valueDisplay && valueDisplay.classList.contains("slider-value")) {
        valueDisplay.textContent = slider.value
      }
  
      // Update value on change
      slider.addEventListener("input", function () {
        if (valueDisplay && valueDisplay.classList.contains("slider-value")) {
          valueDisplay.textContent = this.value
        }
      })
    })
  
    // Animate stat cards and action cards
    const statCards = document.querySelectorAll(".stat-card")
    const actionCards = document.querySelectorAll(".action-card")
  
    statCards.forEach((card, index) => {
      setTimeout(() => {
        card.classList.add("animated")
      }, 100 * index)
    })
  
    actionCards.forEach((card, index) => {
      setTimeout(() => {
        card.classList.add("animated")
      }, 200 * index)
    })
  
    // Add particle background
    createParticleBackground()
  })
  
  // Create particle background
  function createParticleBackground() {
    const canvas = document.createElement("canvas")
    canvas.id = "particle-background"
    canvas.style.position = "fixed"
    canvas.style.top = "0"
    canvas.style.left = "0"
    canvas.style.width = "100%"
    canvas.style.height = "100%"
    canvas.style.pointerEvents = "none"
    canvas.style.zIndex = "-1"
    document.body.appendChild(canvas)
  
    const ctx = canvas.getContext("2d")
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  
    const particles = []
    const particleCount = 50
    const colors = ["rgba(0, 200, 255, ", "rgba(114, 9, 183, "]
  
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 2 + 1,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: Math.random() * 0.5 + 0.1,
        speed: Math.random() * 0.5 + 0.1,
        direction: Math.random() * 360,
      })
    }
  
    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
  
      particles.forEach((particle) => {
        ctx.beginPath()
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2)
        ctx.fillStyle = particle.color + particle.alpha + ")"
        ctx.fill()
  
        // Move particle
        const radian = (particle.direction * Math.PI) / 180
        particle.x += Math.cos(radian) * particle.speed
        particle.y += Math.sin(radian) * particle.speed
  
        // Bounce off edges
        if (particle.x < 0 || particle.x > canvas.width) {
          particle.direction = 180 - particle.direction
        }
        if (particle.y < 0 || particle.y > canvas.height) {
          particle.direction = 360 - particle.direction
        }
      })
  
      // Draw connections
      ctx.strokeStyle = "rgba(255, 255, 255, 0.05)"
      ctx.lineWidth = 0.5
  
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x
          const dy = particles[i].y - particles[j].y
          const distance = Math.sqrt(dx * dx + dy * dy)
  
          if (distance < 150) {
            ctx.beginPath()
            ctx.moveTo(particles[i].x, particles[i].y)
            ctx.lineTo(particles[j].x, particles[j].y)
            ctx.stroke()
          }
        }
      }
  
      requestAnimationFrame(drawParticles)
    }
  
    drawParticles()
  
    // Resize canvas when window is resized
    window.addEventListener("resize", () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    })
  }
  
  