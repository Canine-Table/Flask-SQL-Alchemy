#!/usr/bin/node

function loadForm(form,submit){
    import("../../../static/js/_forms.mjs").then(module => {
      const loadingForm = module.loadingForm;
      return loadingForm(form,submit);
    });
}
