import interactionTask from './interactionTask.json' assert {type: 'json'}



// ------interface------
const sideMenu = document.querySelector("aside")
const menuBtn = document.querySelector("#menu-btn")
const closeBtn = document.querySelector("#close-btn")
const themeTogggler = document.querySelector(".theme-toggler")
const sideBar = document.querySelectorAll('.sidebar-item')
const setUpTaskBtn = document.getElementById('setUpTaskBtn')
const getResultsBtn = document.getElementById('getResultsBtn')

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})

themeTogggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables')
    themeTogggler.querySelector('span:nth-child(1)').classList.toggle('active')
    themeTogggler.querySelector('span:nth-child(2)').classList.toggle('active')
} )
// ------END interface------

// ---------side bar--------

getResultsBtn.addEventListener('click', () => {
    document.querySelector('main').style.display = 'none'
    document.querySelector('section.get-results').style.display = 'block'
    document.querySelector('.right .task-config').style.display = 'none'
})
setUpTaskBtn.addEventListener('click', () => {
    document.querySelector('main').style.display = 'block'
    document.querySelector('section.get-results').style.display = 'none'
    if ((window.innerWidth > 890)){
        document.querySelector('.right .task-config').style.display = 'block'
    } else {
        document.querySelector('.right .task-config').style.display = 'none'
    }
})

for (let sideBarItem of sideBar) {
    sideBarItem.addEventListener(
        'click', () =>{
            toggleSideBar()
            sideBarItem.classList.add('active')
        }
    )
}

// ----------options--------

let config = {}

function select(option) {
    if (option.classList.contains('selected')) {
        option.style.width = '100%'
        document.querySelector('.options .option.selected .description').style.display = 'none'
        let level = Number(option.getAttribute('level'))
        option.classList.remove('selected')
        removeTaskConfigItem(level)
        removeRowsBelow(option.parentNode.parentNode)
    }else{
        checkSelection()
        option.classList.add('selected')
        option.style.width = '100%'
        document.querySelector('.options .option.selected .description').style.display = 'block'
        let level = Number(option.getAttribute('level'))
        removeTaskConfigItem(level)
        document.querySelector('.task-config .items').appendChild(
            createTaskConfigItem(option.getAttribute('type'),
            document.querySelector('.options .option.selected h2').textContent,
            level)
        )
        removeRowsBelow()
        let nextLevel = level + 1
        if (nextLevel <= interactionTask.length-1){
            document.querySelector('main').appendChild(createRow(level+1, interactionTask))
        }else{
            document.querySelector('main').appendChild(createSmilesForm())
        }
        window.scrollTo(0, document.body.scrollHeight)
    }
}

function checkSelection() {
    let elements = document.querySelectorAll(".selected")
    for (let element of elements){
        if (element.classList.contains("selected")) {
            document.querySelector(".options .option.selected .description").style.display = 'none'
            element.classList.remove("selected")
            if (element.style.width === '100%') {
                element.style.width = '100%'
            }
        }
    }
}

function createElementWithClass(tag, className=null, content=null) {
    let element = document.createElement(tag)
    if (className !== null){
        element.setAttribute('class', className)
    }
    if (content !== null) {
        element.textContent = content
    }
    return element
}

function createRow(level, task) {
    let localLevel = task[level]
    let row = createElementWithClass('div', 'row')
    row.appendChild(createElementWithClass('h1', null, localLevel.header))
    let options = createElementWithClass('div', 'options')
    for (let option of localLevel.options){
        let optionDiv = createElementWithClass('div', 'option')
        let optionHeader = createElementWithClass('div',  'header')
        let optionIcon = createElementWithClass('div',  'icon')
        let optionRight = createElementWithClass('div',  'right')
        let optionDescription = createElementWithClass('div', 'description')

        optionIcon.appendChild(createElementWithClass('span', 'material-icons-sharp', option.spanValue))
        optionRight.appendChild(createElementWithClass('h2', null, option.option))
        optionRight.appendChild(createElementWithClass('small', 'text-muted', option.descriptionSmall))
        optionHeader.appendChild(optionIcon)
        optionHeader.appendChild(optionRight)
        optionDescription.appendChild(createElementWithClass('p', null, option.descriptionLong))

        optionDiv.appendChild(optionHeader)
        optionDiv.appendChild(optionDescription)
        optionDiv.addEventListener('click', () => {select(optionDiv)})
        optionDiv.setAttribute('type', localLevel.type)
        optionDiv.setAttribute('level', level)
        options.appendChild(optionDiv)
    }
    row.appendChild(options)
    return row
}

function createTaskConfigItem(type, selection, level){

    let configItem = createElementWithClass('div', 'item')
    configItem.appendChild(
        createElementWithClass(
            'span',
            'material-icons-sharp',
            'check_circle'
            )
        )
    configItem.appendChild(
        createElementWithClass('h3', null, `${type}:`)
    )
    configItem.appendChild(
        createElementWithClass('p', null, selection)
    )
    configItem.setAttribute('level', level)
    config[type] = selection
    return configItem
}

function createSmilesForm() {
    let smilesFormDiv = createElementWithClass('div', 'smiles-form')
    let smilesForm = createElementWithClass('form')
    let smilesTextArea = createElementWithClass('textarea', 'smiles-ta')
    let smilesBtn = createElementWithClass('div', 'smiles-btn', 'Set up task')
    let smilesHeader = createElementWithClass('h1', null, 'Enter SMILEs')
    let smilesDescription = createElementWithClass('p', null, '*Have to be a valid coma separated SMILEs strings.')

    smilesBtn.setAttribute('id', 'smilesBtn')
    smilesBtn.addEventListener('click', () =>{
        let smiles = getAndParseSmiles()
        sendConfig(smiles, config)
    })
    smilesTextArea.setAttribute('placeholder', 'O=C(C)Oc1ccccc1C(=O)O,')
    smilesTextArea.setAttribute('id', 'smilesTextArea')
    smilesTextArea.setAttribute('rows', '5')
    smilesForm.appendChild(smilesTextArea)
    smilesForm.appendChild(smilesDescription)
    smilesForm.appendChild(smilesBtn)
    smilesFormDiv.appendChild(smilesHeader)
    smilesFormDiv.appendChild(smilesForm)

    return smilesFormDiv
}

function removeTaskConfigItem(level){
    let taskConfig = document.querySelector('.right .task-config .items')
    if (taskConfig.lastChild !== null) {
        while (taskConfig.lastChild !== null && Number(taskConfig.lastChild.getAttribute('level')) >= level) {
            taskConfig.removeChild(taskConfig.lastChild);
        }
    }
}

function getSelectedRow(){
    let selectedElement = document.querySelector('.option.selected')
    return selectedElement.parentNode.parentNode
}

function removeRowsBelow(row=null){
    let rows = document.querySelector('main')
    if (row === null){
        let selectedRow = getSelectedRow()
        while (rows.lastChild !== selectedRow) {
            rows.removeChild(rows.lastChild);
        }
    }else{
        while (rows.lastChild !== row) {
            rows.removeChild(rows.lastChild);
        }
    }
}

function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
  }

function sendConfig(smiles, config){
    config['id'] = String(getRandomArbitrary(1e9, 1e10))
    config['smiles'] = smiles
    console.log(config)
}

function toggleSideBar(){
    for (let sideBarItem of sideBar) {
        if (sideBarItem.classList.contains('active')){
            sideBarItem.classList.remove('active')
        }
    }
}

function getAndParseSmiles(){
    return document.getElementById('smilesTextArea').value.replace(/\s/g, '').replace(/[\r\n]/gm, '').split(',')
}
document.querySelector('main').appendChild(createRow(0, interactionTask))
document.querySelector('.task-config').appendChild(createElementWithClass('div', 'items'))

window.onresize = () => {
    if(window.innerWidth > 890) {
        sideMenu.style.display = 'block'
        if (document.querySelector('aside .sidebar .sidebar-item.active').getAttribute('id') === 'getResultsBtn'){
            document.querySelector('.right .task-config').style.display = 'none'
        }else{
        document.querySelector('.right .task-config').style.display = 'block'
        }
        }
    else{
        sideMenu.style.display = 'none'
        document.querySelector('.right .task-config').style.display = 'none'
    }
    }
