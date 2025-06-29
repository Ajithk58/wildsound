// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  });
});

// Scroll to Top Button Functionality
const scrollToTopButton = document.createElement('button');
scrollToTopButton.innerText = '↑';
scrollToTopButton.classList.add('scroll-to-top');
document.body.appendChild(scrollToTopButton);

// Show or Hide Scroll to Top Button based on Scroll Position
window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    scrollToTopButton.style.display = 'block';
  } else {
    scrollToTopButton.style.display = 'none';
  }
});

// Scroll to Top when Button is Clicked
scrollToTopButton.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Form Validation for Contact Form
document.querySelector('form').addEventListener('submit', function (e) {
  e.preventDefault();
  
  const name = document.querySelector('#name').value.trim();
  const email = document.querySelector('#email').value.trim();
  const message = document.querySelector('#message').value.trim();

  if (name === '' || email === '' || message === '') {
    alert('Please fill in all fields.');
  } else if (!validateEmail(email)) {
    alert('Please enter a valid email address.');
  } else {
    alert('Thank you for contacting us! We will get back to you soon.');
    // Clear form after successful submission
    this.reset();
  }
});
const elements = document.querySelectorAll('.feature-item, .testimonial-item, .about p');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
    }
  });
}, { threshold: 0.5 });

elements.forEach(element => {
  observer.observe(element);
});

// Email Validation Function
function validateEmail(email) {
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(email);
}

// Optional: Animation for elements as they come into view (for better UX)
const elements = document.querySelectorAll('.feature-item, .testimonial-item, .about p');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
    }
  });
}, { threshold: 0.5 });

elements.forEach(element => {
  observer.observe(element);
});
