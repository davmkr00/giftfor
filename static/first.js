const buttonFemale = document.querySelector('input.female');
const buttonMale = document.querySelector('input.male');

buttonFemale.addEventListener('click', () => {
  window.location.href = window.location.href + 'her';
});

buttonMale.addEventListener('click', () => {
  window.location.href = window.location.href + 'him';
});
