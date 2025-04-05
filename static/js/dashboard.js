// Dashboard JavaScript

document.addEventListener("DOMContentLoaded", () => {
    // Add animation to stat cards
    const statCards = document.querySelectorAll(".stat-card")
  
    statCards.forEach((card, index) => {
      setTimeout(() => {
        card.style.opacity = "1"
        card.style.transform = "translateY(0)"
      }, 100 * index)
    })
  
    // Add animation to action cards
    const actionCards = document.querySelectorAll(".action-card")
  
    actionCards.forEach((card, index) => {
      setTimeout(() => {
        card.style.opacity = "1"
        card.style.transform = "translateY(0)"
      }, 200 * index)
    })
  })
  
  