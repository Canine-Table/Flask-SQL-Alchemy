#!/usr/bin/node

function loadingForm(form){
    import("../../../static/js/_forms.mjs").then(module => {
      const loadingForm = module.loadingForm;
      return loadingForm(form);
    });
}