const BAS_API_URL = 'https://d5dmp6be8f69rg8uso44.apigw.yandexcloud.net';

async function addItem(author, title, content) {
    let response = await fetch(`${BAS_API_URL}/items/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({author: author, text: content, title: title})
    });
    let result = await response.json();
    return result;
}


function createItemsInDoc(author, title, text, createdAt){
    let container = document.createElement('li');
    let titleEl = document.createElement('h2');
    let authorEl = document.createElement('p');
    let textEl = document.createElement('p');
    let createdAtEl = document.createElement('i');


    container.classList.add("item-list");
    container.classList.add("item-list");
    titleEl.textContent = title;
    textEl.textContent = text;
    authorEl.textContent = author;
    createdAtEl.textContent = createdAt;

    container.appendChild(titleEl);
    container.appendChild(authorEl);
    container.appendChild(textEl);
    container.appendChild(createdAtEl);

    return container;
}

async function getAllItems() {
    let response = await fetch(
        `${BAS_API_URL}/items/`,
        {method: 'GET'}
    );
    return await response.json();
}

getAllItems().then((response) => {
    let itemsListElement = document.querySelector(".items-list");
    console.log(response);
    response.sort((item1, item2) => new Date(item1.created_at) - new Date(item2.created_at));
    response.forEach( (item) => {
        let bookItem = createItemsInDoc(item.author, item.title, item.text, item.created_at);
        itemsListElement.appendChild(bookItem);
    });
});


function submitFormHandler(e) {
    e.preventDefault();

    const form = e.target;
    const formFields = form.elements;
    const fieldsToClear = [formFields.author, formFields.title, formFields.text];
    const author = formFields.author.value;
    const title = formFields.title.value;
    const content = formFields.text.value;

    if (!author || !title || !content){
        return;
    }

    let itemsListElement = document.querySelector(".items-list");

    addItem(author, title, content)
        .then((ad) => {
            let adItem = createItemsInDoc(ad.author,  ad.title, ad.text, ad.created_at);
            itemsListElement.appendChild(adItem);
            fieldsToClear.forEach(field => {
                field.value = "";
            })
        })
}

document.querySelector('.add-item-form').addEventListener('submit', submitFormHandler);



function showVersions(){
    const frontSpan = document.querySelector('.front-version');
    const backVSpan = document.querySelector('.back-version');
    const backNSpan = document.querySelector('.back-name');

    if (typeof FRONTEND_VERSION !== 'undefined') {
        frontSpan.textContent = FRONTEND_VERSION;
    }

    fetch(`${BAS_API_URL}/version/`, { method: 'GET' })
        .then(response => response.json())
        .then(version => {
            let backendVersion = version[0];
            let backendName = version[1];
            backVSpan.textContent = backendVersion;
            backNSpan.textContent = backendName;
        })
}

showVersions();