'use strict';
const element = document.getElementById('giftfor-cards');
const giftforContainer = document.querySelector('.giftfor');
const allCards = document.querySelectorAll('.giftfor--card');
const nope = document.getElementById('nope');
const love = document.getElementById('love');
const giftfor = window.location.pathname.slice(1);
var received = [];
const sid = (Math.random() + 1).toString(36).substring(2);

function handleCardClick(url) {
  window.open(url);
}

function createCards(id, title, image, url) {
  received.push(id);
  const cardDiv = document.createElement('div');
  cardDiv.url = url;
  cardDiv.id = id;
  cardDiv.className = 'giftfor--card';
  // cardDiv.addEventListener('dblclick', handleCardClick.bind(null, url));

  const cardP = document.createElement('p');
  cardP.innerText = title;
  const cardImg = document.createElement('img');
  cardImg.src = image;
  cardDiv.appendChild(cardImg);
  cardDiv.appendChild(cardP);
  element.appendChild(cardDiv);
  initCards();
  actionListener(cardDiv);
}

async function getCards(count) {
  const data = await postData('http://localhost:4000/product', {
    giftfor,
    count,
    received,
  });
  return data;
}

function feedback(action, id, sw = false) {
  postData('http://localhost:4000/feedback', {
    giftfor,
    action,
    id,
    sid,
    sw,
  });
}

async function postData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

async function createInitialCards() {
  const products = await getCards(5);
  products.forEach((product) => {
    createCards(product[0], product[1], product[3], product[4]);
  });
}

function initCards(card, index) {
  const newCards = document.querySelectorAll('.giftfor--card:not(.removed)');

  newCards.forEach(function (card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
    card.style.opacity = (10 - index) / 10;
  });
  giftforContainer.classList.add('loaded');
}

function actionListener(el) {
  const hammertime = new Hammer(el);

  hammertime.on('pan', function (event) {
    el.classList.add('moving');
  });

  hammertime.on('pan', function (event) {
    if (event.deltaX === 0) return;
    if (event.center.x === 0 && event.center.y === 0) return;

    giftforContainer.classList.toggle('giftfor_love', event.deltaX > 0);
    giftforContainer.classList.toggle('giftfor_nope', event.deltaX < 0);

    const xMulti = event.deltaX * 0.03;
    const yMulti = event.deltaY / 80;
    const rotate = xMulti * yMulti;

    event.target.style.transform =
      'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
  });

  hammertime.on('panend', function (event) {
    // element.removeEventListener('clcik', handleCardClick, true);
    el.classList.remove('moving');
    giftforContainer.classList.remove('giftfor_love');
    giftforContainer.classList.remove('giftfor_nope');

    const moveOutWidth = document.body.clientWidth;
    const keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

    if (keep) {
      event.target.style.transform = '';
    } else {
      const cards = document.querySelectorAll('.giftfor--card:not(.removed)');
      const card = cards[0];
      if (event.deltaX > 0) {
        feedback('liked', card.id, true);
        card.url && handleCardClick(card.url);
      } else {
        feedback('dislike', card.id, true);
      }
      const endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
      const toX = event.deltaX > 0 ? endX : -endX;
      const endY = Math.abs(event.velocityY) * moveOutWidth;
      const toY = event.deltaY > 0 ? endY : -endY;
      const xMulti = event.deltaX * 0.03;
      const yMulti = event.deltaY / 80;
      const rotate = xMulti * yMulti;

      event.target.style.transform =
        'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';

      addTheCard();
    }
    event.target.classList.toggle('removed', !keep);
  });
}

function createButtonListener(love) {
  return async function (event) {
    const cards = document.querySelectorAll('.giftfor--card:not(.removed)');
    const moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    const card = cards[0];

    card.classList.add('removed');

    if (love) {
      card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
      feedback('liked', card.id);
      card.url && handleCardClick(card.url);
    } else {
      card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
      feedback('dislike', card.id);
    }
    addTheCard();

    event.preventDefault();
  };
}

async function addTheCard() {
  const products = await getCards(1);
  if (products.length) {
    createCards(products[0][0], products[0][1], products[0][3], products[0][4]);
    initCards();
    return;
  }
  createCards(
    -1,
    'Oops! Our gifts for finished',
    'https://cdn.igp.com/f_auto,q_auto/cards/birthday-gifts-for-women.jpg'
  );
}

createInitialCards();
initCards();

const nopeListener = createButtonListener(false);
const loveListener = createButtonListener(true);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);
