const menu = document.querySelector(".main-menu");
const menuCityWarszawa = document.getElementById("hide-main-warszawa");
const menuCityKrakow = document.getElementById("hide-main-krakow");
const menuKrakow = document.getElementById("hide-krakow");
const menuWarszawa = document.getElementById("hide-warszawa");


menuKrakow.style.opacity = '0';
menuWarszawa.style.opacity = '0';
menuCityKrakow.style.opacity = '0';
menuCityWarszawa.style.opacity = '0';

menu.addEventListener('click', hideShowMainWarszawa, false);
menu.addEventListener('click', hideShowMainKrakow, false);
menuCityWarszawa.addEventListener('click', hideShowWarszawa, false);
menuCityKrakow.addEventListener('click', hideShowKrakow, false);



function hideShowMainKrakow() {
    if(menuCityKrakow.style.opacity == '0'){
   menuCityKrakow.style.opacity = '1';
   menuCityKrakow.style.cursor = 'pointer';
   menuCityKrakow.style.pointerEvents = 'auto';
   } else {
   menuCityKrakow.style.opacity = '0';
   menuCityKrakow.style.cursor = 'default';
   menuCityKrakow.style.pointerEvents = 'none';
   if (menuKrakow.style.opacity == '1'){
   hideShowKrakow();
   }
   }
}

function hideShowMainWarszawa() {
if(menuCityWarszawa.style.opacity == '0'){
   menuCityWarszawa.style.opacity = '1';
   menuCityWarszawa.style.cursor = 'pointer';
   menuCityWarszawa.style.pointerEvents = 'auto';
   } else {
   menuCityWarszawa.style.opacity = '0';
   menuCityWarszawa.style.cursor = 'default';
   menuCityWarszawa.style.pointerEvents = 'none';
   if (menuWarszawa.style.opacity == '1'){
   hideShowWarszawa();
   }
   }
}

function hideShowKrakow() {
   if(menuKrakow.style.opacity == '0'){
   menuKrakow.style.opacity = '1';
   menuKrakow.style.cursor = 'pointer';
   menuKrakow.style.pointerEvents = 'auto';
   } else {
   menuKrakow.style.opacity = '0';
   menuKrakow.style.cursor = 'default';
   menuKrakow.style.pointerEvents = 'none';
   }
}

function hideShowWarszawa() {
   if(menuWarszawa.style.opacity == '0'){
   menuWarszawa.style.opacity = '1';
   menuWarszawa.style.cursor = 'pointer';
   menuWarszawa.style.pointerEvents = 'auto';
   } else {
   menuWarszawa.style.opacity = '0';
   menuWarszawa.style.cursor = 'default';
   menuWarszawa.style.pointerEvents = 'none';
   }
}