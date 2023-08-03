#!/usr/bin/node

export function loadingForm(form,submit){

    new Map([
        ["disabled","true"],
        ["value",""],
        ["aria-hidden","true"],
    ]).forEach((value, key) => {
        form[submit].setAttribute(key,value)
    })
    new Map([
        ["height", "32px"],
        ["backgroundColor", "transparent"],
        ["width", "32px"],
        ["marginInline", "12px"],
        ["borderRadius", "50px"],
        ["borderStyle","dotted dashed groove double"],
    ]).forEach((value, key) => {
        form[submit].style[key] = value;
    })

    form[submit].classList.add("spinner-border");
    return true;
}

