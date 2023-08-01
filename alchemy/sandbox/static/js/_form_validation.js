#!/usr/bin/node

function checkForm(form){
    import("../../../static/js/_forms.mjs").then(module => {
      const checkForm = module.checkForm;
      return checkForm(form);
    });
}