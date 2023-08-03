#!/usr/bin/node


function loadForm(form,btn,inpt){

  new Map([
      ["disabled","true"],
      ["value",""],
      ["aria-hidden","true"],
  ]).forEach((value, key) => {
      form[btn].setAttribute(key,value)
  })
  new Map([
      ["height", "32px"],
      ["width", "32px"],
      ["position", "relative"],
      ["right", "0px"],
      ["zIndex", "-1"],
      ["borderRadius", "50px"],
      ["borderColor", "black"],
      ['marginRight', '50px'],
      ["borderStyle","dotted dashed groove double"],
  ]).forEach((value, key) => {
      form[btn].style[key] = value;
  })

  form[btn].classList.add("spinner-border");
  ["marginLeft", "50px"],

  button = document.getElementById(inpt)
  button.style.paddingRight = '50px'
  btn.classList.add('btn-outline-success')
  button.appendChild(form[btn])
  return true;
}

