// DocuMind Home Page JavaScript

// Function to handle the "Go to the Application" button click
function goToApplication() {
    // Navigate to the main application page
    window.location.href = '/app';
}

// Add smooth animations on page load
document.addEventListener('DOMContentLoaded', function() {
    // Feature cards are now animated with CSS animations
    // Add additional interactive effects
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        // Add hover sound effect (visual feedback)
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add smooth scrolling for any future navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add tech tag hover effects
    const techTags = document.querySelectorAll('.tech-tag');
    techTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.background = 'rgba(59, 130, 246, 0.2)';
        });
        
        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.background = 'rgba(59, 130, 246, 0.1)';
        });
    });
});
