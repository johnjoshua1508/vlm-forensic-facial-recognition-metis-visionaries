// Login Page JavaScript - Futuristic Theme

document.addEventListener("DOMContentLoaded", () => {
    // Create canvas for network background
    const createNetworkBackground = () => {
      // Create canvas element
      const canvas = document.createElement("canvas")
      canvas.id = "network-background"
      canvas.className = "network-background"
      document.body.appendChild(canvas)
  
      // Set canvas size
      const resizeCanvas = () => {
        canvas.width = window.innerWidth
        canvas.height = window.innerHeight
      }
  
      resizeCanvas()
      window.addEventListener("resize", resizeCanvas)
  
      // Initialize canvas context
      const ctx = canvas.getContext("2d")
  
      // Network nodes and connections
      const nodes = []
      const numNodes = 50 // Number of nodes
      const connectionDistance = 150 // Maximum distance for connections
      const nodeSpeed = 0.3 // Speed of node movement
  
      // Create nodes
      for (let i = 0; i < numNodes; i++) {
        nodes.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 1.5 + 1,
          vx: Math.random() * nodeSpeed * 2 - nodeSpeed,
          vy: Math.random() * nodeSpeed * 2 - nodeSpeed,
          color: "rgba(0, 200, 255, " + (Math.random() * 0.5 + 0.2) + ")",
        })
      }
  
      // Animation function
      const animate = () => {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height)
  
        // Update and draw nodes
        for (let i = 0; i < nodes.length; i++) {
          const node = nodes[i]
  
          // Update position
          node.x += node.vx
          node.y += node.vy
  
          // Bounce off edges
          if (node.x < 0 || node.x > canvas.width) node.vx = -node.vx
          if (node.y < 0 || node.y > canvas.height) node.vy = -node.vy
  
          // Draw node
          ctx.beginPath()
          ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
          ctx.fillStyle = node.color
          ctx.fill()
  
          // Draw connections
          for (let j = i + 1; j < nodes.length; j++) {
            const otherNode = nodes[j]
            const dx = otherNode.x - node.x
            const dy = otherNode.y - node.y
            const distance = Math.sqrt(dx * dx + dy * dy)
  
            if (distance < connectionDistance) {
              // Calculate opacity based on distance
              const opacity = 1 - distance / connectionDistance
  
              // Draw line
              ctx.beginPath()
              ctx.moveTo(node.x, node.y)
              ctx.lineTo(otherNode.x, otherNode.y)
              ctx.strokeStyle = `rgba(0, 200, 255, ${opacity * 0.2})`
              ctx.lineWidth = 1
              ctx.stroke()
            }
          }
        }
  
        // Continue animation
        requestAnimationFrame(animate)
      }
  
      // Start animation
      animate()
    }
  
    // Create the network background
    createNetworkBackground()
  
    // Form validation with visual feedback
    const loginForm = document.querySelector(".login-form")
    if (loginForm) {
      loginForm.addEventListener("submit", (e) => {
        const username = document.getElementById("username")
        const password = document.getElementById("password")
        let isValid = true
  
        if (!username.value.trim()) {
          e.preventDefault()
          isValid = false
          username.style.borderColor = "var(--danger-color)"
          username.style.boxShadow = "0 0 10px var(--danger-color)"
  
          setTimeout(() => {
            username.style.borderColor = ""
            username.style.boxShadow = ""
          }, 2000)
        }
  
        if (!password.value.trim()) {
          e.preventDefault()
          isValid = false
          password.style.borderColor = "var(--danger-color)"
          password.style.boxShadow = "0 0 10px var(--danger-color)"
  
          setTimeout(() => {
            password.style.borderColor = ""
            password.style.boxShadow = ""
          }, 2000)
        }
  
        if (!isValid) {
          // Create a floating error message
          const errorMsg = document.createElement("div")
          errorMsg.textContent = "Please enter both username and password"
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
    }
  
    // Add glow effect to login button on hover
    const loginButton = document.querySelector(".login-form .btn-primary")
    if (loginButton) {
      loginButton.addEventListener("mouseenter", () => {
        loginButton.style.boxShadow = "0 0 20px var(--primary-color)"
      })
  
      loginButton.addEventListener("mouseleave", () => {
        loginButton.style.boxShadow = ""
      })
    }
  })
  
  