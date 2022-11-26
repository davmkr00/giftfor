const buttonFemale = document.querySelector('input.female');
const buttonMale = document.querySelector('input.male');
const buttonFemaleText = document.querySelector('div.textf');
const buttonMaleText = document.querySelector('div.textm');

buttonFemale.addEventListener('click', () => {
  window.location.href = window.location.href + 'her';
});

buttonMale.addEventListener('click', () => {
  window.location.href = window.location.href + 'him';
});

buttonFemaleText.addEventListener('click', () => {
  window.location.href = window.location.href + 'her';
});

buttonMaleText.addEventListener('click', () => {
  window.location.href = window.location.href + 'him';
});
