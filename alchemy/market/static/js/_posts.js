#!/usr/bin/node

Array.from(document.getElementById('starRating').children).forEach(child => {
    document.getElementById('rating').value = 0
    child.addEventListener('mouseover', () => {
        for(let i=1;i<=child.id;i++){
            let element = document.getElementById(`${i}`)
            element.classList.add('checked')
        }
    })

    child.addEventListener('mouseleave', () => {
        for(let i=1;i<=child.id;i++){
            let element = document.getElementById(`${i}`)
            element.classList.remove('checked')
        }
    })
    child.addEventListener('click', () => {
        for(let i=1;i<=5;i++){
            let element = document.getElementById(`${i}`)
            element.classList.remove('selected')
        }
        for(let i=1;i<=child.id;i++){
            let element = document.getElementById(`${i}`)
            element.classList.add('selected')
            document.getElementById('rating').value = i
        }
    })
})
