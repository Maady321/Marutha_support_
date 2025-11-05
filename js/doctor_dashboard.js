// Example interactivity for future use
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.addEventListener('click', () => {
      alert(`Opening ${card.querySelector('p').textContent} details...`);
    });
  });
});
