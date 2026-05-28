```javascript
// utils.js
function handleButtonClick(event) {
    event.preventDefault();
    if (event.target.classList.contains('submit-btn')) {
        const email = document.getElementById('email-input').value;
        const message = document.getElementById('message-input').value;
        
        console.log(`Email: ${email}, Message: ${message}`);
        // Add API call to send information here
    }
}

// scripts.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#luxury-car-form');
  if(form) {
    form.onclick = (e) => handleButtonClick(e);
    
    document.querySelectorAll('.submit-btn').forEach(button => button.addEventListener('mouseover', () => console.log(`Mouse over`)));
    document.querySelectorAll('.submit-btn').forEach(button => button.addEventListener('mouseout', () => console.log(`Mouse out`)));
  }
  
  const heroWelcome = document.querySelector('.hero-welcome');
  if(heroWelcome) {
    setTimeout(() => {
      heroWelcome.classList.add('animate-welcome');
    }, 500);
  }
  
  document.querySelectorAll('.contact-info__item').forEach(item => item.addEventListener('click', () => console.log(`Contact info clicked`)));
});
```