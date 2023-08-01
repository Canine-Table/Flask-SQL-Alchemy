#!/usr/bin/node

function loadForm(form){
    import("../../../static/js/_forms.mjs").then(module => {
      const loadingForm = module.loadingForm;
      return loadingForm(form);
    });
}