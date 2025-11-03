// Get modals and buttons
const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');
const loginModal = document.getElementById('loginModal');
const signupModal = document.getElementById('signupModal');
const closeBtns = document.querySelectorAll('.close');

// Show modals
loginBtn.onclick = () => loginModal.style.display = 'block';
signupBtn.onclick = () => signupModal.style.display = 'block';

// Close modals
closeBtns.forEach(btn => {
  btn.onclick = () => {
    loginModal.style.display = 'none';
    signupModal.style.display = 'none';
  };
});

// Close modal when clicking outside
window.onclick = (e) => {
  if (e.target === loginModal) loginModal.style.display = 'none';
  if (e.target === signupModal) signupModal.style.display = 'none';
};
