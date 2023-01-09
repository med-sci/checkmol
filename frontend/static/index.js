// add down arrow in circle to scroll

let interactionTask  = [
    {
        "header": "Select Task",
        "type": "Task",
        "options": [
            {
                "option": "Interaction",
                "optionClass": "interaction",
                "imgpath": "./img/EGFR.png",
                "descriptionSmall": "Small molecule - protein interaction"
            }
        ]
    },
    {
        "header": "Choose target protein",
        "type": "Protein",
        "options": [
            {
                "option": "NR3C4",
                "optionClass": "NR3C4",
                "imgpath": "./img/NR3C4.png",
                "descriptionSmall": "Androgen receptor\n"
            },
            {
                "option": "EGFR",
                "optionClass": "EGFR",
                "imgpath": "./img/EGFR.png",
                "descriptionSmall": "Epidermal growth factor receptor"
            },
            {
                "option": "VEGFR2",
                "optionClass": "VEGFR2",
                "imgpath": "./img/VEGFR2.png",
                "descriptionSmall": "Vascular endothelial growth factor receptor 2"
            }
        ]
    },
    {
        "header": "Select interaction constant",
        "type": "Constant",
        "options": [
            {
                "option": "IC 50",
                "optionClass": "IC-50",
                "imgpath": "./img/EGFR.png",
                "descriptionSmall": "Half maximal inhibitory concentration"
            },
            {
                "option": "pIC 50",
                "optionClass": "pIC-50",
                "imgpath": "./img/EGFR.png",
                "descriptionSmall": "Negative logarithm of IC 50"
            }
        ]
    },
    {
        "header": "Set model mode",
        "type": "Mode",
        "options": [
            {
                "option": "Regression",
                "optionClass": "regression",
                "imgpath": "./img/EGFR.png",
                "descriptionSmall": "R2 score mean on cross-validation: 0.6"
            }
        ]
    }
]

const apiUrl = "http://api.lupuslucis.fvds.ru/"
// ------interface------
const sideMenu = document.querySelector("aside")
const menuBtn = document.querySelector("#menu-btn")
const closeBtn = document.querySelector("#close-btn")
const themeTogggler = document.querySelector(".theme-toggler")
const sideBar = document.querySelectorAll('.sidebar-item')
const setUpTaskBtn = document.getElementById('setUpTaskBtn')
const getResultsBtn = document.getElementById('getResultsBtn')
const taskIdBtn = document.getElementById('taskIdBtn')
const taskIdInput = document.getElementById('taskIdInput')
const scrollDownBtn = document.getElementById("scrollDownBtn")

let theme = 'light'

scrollDownBtn.addEventListener('click', () => {
    window.scrollTo(0, document.body.scrollHeight)
})

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
    if (theme === 'light'){
        theme = 'dark'
    } else if (theme === 'dark'){
        theme = 'light'
    }
    if (document.querySelector('.smiles-form .form-submit')){
        grecaptcha.reset({"theme": theme})
    }
} )
// ------END interface------

// ---------side bar--------

getResultsBtn.addEventListener('click', () => {
    document.querySelector('main').style.display = 'none'
    document.querySelector('section.get-results').style.display = 'block'
    document.querySelector('.right .task-config').style.display = 'none'
    let notification = document.querySelector('.notification')
    if (notification) {
        removeInfoBlock()
    }
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
        document.querySelector('.options .option.selected').style.width = '15rem'
        document.querySelector('.options .option.selected .image').style.background = 'var(--color-white)'
        document.querySelector('.options .option.selected small').style.display = 'none'
        let level = Number(option.getAttribute('level'))
        option.classList.remove('selected')
        removeTaskConfigItem(level)
        removeRowsBelow(option.parentNode.parentNode)
    }else{
        checkSelection()
        option.classList.add('selected')
        document.querySelector('.options .option.selected .image').style.background = 'var(--color-primary)'
        document.querySelector('.options .option.selected small').style.display = 'block'
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
            let [widgetId, smilesForm] =  createSmilesForm(level+2)
            document.querySelector('main').appendChild(smilesForm)
        }
        // let scrollposition = option.offsetTop -(0.3*option.offsetTop)
        // console.log(scrollposition)
        // window.scrollTo(0, scrollposition)
    }
}

function checkSelection() {
    let elements = document.querySelectorAll(".selected")
    for (let element of elements){
        if (element.classList.contains("selected")) {
            document.querySelector('.options .option.selected .image').style.background = 'var(--color-white)'
            document.querySelector('.options .option.selected small').style.display = 'none'
            element.classList.remove("selected")
            if (element.style.width === '100%') {
                element.style.width = '13rem'
            }
        }
    }
}

function createElementWithClass(tag, className=null, content=null, html=false) {
    let element = document.createElement(tag)
    if (className !== null){
        element.setAttribute('class', className)
    }
    if (content !== null) {
        if (html === true) {
            element.innerHTML = content
        } else {
            element.textContent = content
        }
    }
    return element
}

function createRow(level, task) {
    let localLevel = task[level]
    let row = createElementWithClass('div', 'row')
    let header = createElementWithClass('div', 'options-header')
    let optionsLogo = createElementWithClass('div', 'options-logo')
    optionsLogo.appendChild(createElementWithClass('p', null, String(level+1)))
    header.appendChild(optionsLogo)
    header.appendChild(createElementWithClass('h1', null, localLevel.header))
    row.appendChild(header)
    let options = createElementWithClass('div', 'options')
    for (let option of localLevel.options){
        let optionDiv = createElementWithClass('div', 'option')
        let optionHeader = createElementWithClass('div',  'header')
        let optionImage = createElementWithClass('img')
        let optionImageDiv = createElementWithClass('div', 'image')
        optionImage.setAttribute('src', option.imgpath)
        optionImageDiv.appendChild(optionImage)
        let optionRight = createElementWithClass('div',  'bottom')
        optionRight.appendChild(createElementWithClass('h2', null, option.option))
        let smallDescription = createElementWithClass('small', 'text-muted', option.descriptionSmall)
        smallDescription.style.display = 'none'
        optionRight.appendChild(smallDescription)
        optionHeader.appendChild(optionImageDiv)
        optionHeader.appendChild(optionRight)

        optionDiv.appendChild(optionHeader)
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

function createSmilesForm(level) {
    let smilesFormDiv = createElementWithClass('div', 'smiles-form')
    let smilesForm = createElementWithClass('form')
    let smilesTextArea = createElementWithClass('textarea', 'smiles-ta')
    let smilesHeader = createElementWithClass('div', 'options-header')
    let smilesLogo = createElementWithClass('div', 'options-logo')
    let formSubmit = createElementWithClass('div', 'form-submit')
    smilesLogo.appendChild(createElementWithClass('p', null, String(level)))
    smilesHeader.appendChild(smilesLogo)
    smilesHeader.appendChild(createElementWithClass('h1', null, 'Enter SMILES'))
    let smilesDescription = createElementWithClass('p', null, '*Have to be a valid coma separated SMILEs strings.')
    smilesTextArea.setAttribute('placeholder', 'O=C(C)Oc1ccccc1C(=O)O,')
    smilesTextArea.setAttribute('id', 'smilesTextArea')
    smilesTextArea.setAttribute('rows', '5')
    smilesForm.appendChild(smilesTextArea)
    smilesForm.appendChild(smilesDescription)
    smilesFormDiv.appendChild(smilesHeader)
    smilesFormDiv.appendChild(smilesForm)
    let widgetId = grecaptcha.render(
        formSubmit,
        {"sitekey": "6Ld2r8gjAAAAAP_QFG9k3v8YYMYkiOtOZz-7jtSq", "callback": sendRecaptcha, "theme": theme}
        )
    smilesFormDiv.appendChild(formSubmit)

    return [widgetId, smilesFormDiv]
}

async function sendRecaptcha(token) {
    const url = apiUrl + '/validate_captcha/' + token
    try {
        let response = await fetch(
            url, {
                method: 'POST'
            }
        )
        let responseJson = await response.json()
        if (responseJson.success == true){
            document.querySelector(".smiles-form .form-submit").style.display = 'none'
            console.log(document.querySelector(".smiles-form .form-submit"))
            let smilesBtn = document.querySelector(".smiles-form .smiles-btn")
            if  (smilesBtn == null){
                document.querySelector(".smiles-form").appendChild(createSmilesBtn())
            } else {
                smilesBtn.style.display = "flex"
            }
        }else{
            grecaptcha.reset()
        }
    } catch (error) {
        grecaptcha.reset()
    }
}

function createSmilesBtn() {
    let smilesBtn = createElementWithClass('div', 'smiles-btn', 'Set up task')
    smilesBtn.setAttribute('id', 'smilesBtn')
    smilesBtn.addEventListener('click', () =>{
        removeInfoBlock()
        let smiles = getAndParseSmiles()

        sendConfig(smiles, config)
        document.querySelector(".smiles-btn").style.display = 'none'
        document.querySelector(".smiles-form .form-submit").style.display = 'block'
        grecaptcha.reset()
    })
    return smilesBtn
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

async function sendConfig(smiles, config){
    const id = String(getRandomArbitrary(1e9, 1e10)).replace('.','')
    config['id'] = id
    config['smiles'] = smiles
    const targetUrl = apiUrl + 'runs/'+ id
    console.log(targetUrl)
    try{
        let response = await fetch(targetUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        })
        let status = response.status
        console.log(status)
        if (status === 200) {
            let responseJson = await response.json()
            console.log(responseJson)
            if (responseJson.status === 'Ok'){
                var infoBlock = generateInfoBlock('success', 'Success!', `Your task id: <span>${id}</span>`, id)
            } else if(responseJson.status === 'ValidationError') {
                var infoBlock = generateInfoBlock('danger', 'Invalid SMILES', 'Please, provide a valid SMILES')
            } else {
                var infoBlock = generateInfoBlock('danger', 'Oops..', 'Something is wrong. Try one more time')
            }
        } else {
            var infoBlock = generateInfoBlock('danger', 'Oops..', 'Something is wrong. Try one more time')
        }
    } catch(e){
        var infoBlock = generateInfoBlock('danger', 'Oops..', 'Something is wrong. Try one more time')
    }
    var smilesForm = document.querySelector('.smiles-form')
    smilesForm.insertBefore(infoBlock, document.querySelector('.smiles-form .form-submit'))
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

function generateInfoBlock(cls, header, message, taskId=null){
    let infoBlock = createElementWithClass('div', 'notification')
    let infoBlockContent = createElementWithClass('div', 'content')
    let infoCloseBlock = createElementWithClass('div', 'close')
    let infoCloseBtn = createElementWithClass('span', 'material-icons-sharp','close')
    infoCloseBtn.addEventListener('click', () => {
        removeInfoBlock()
    })
    infoCloseBlock.appendChild(infoCloseBtn)
    if (cls === 'success') {
        let infoCopyBtn = createElementWithClass('span', 'material-icons-sharp','copy')
        infoCopyBtn.addEventListener('click', () => {
            copyId(taskId)
        })
        infoCloseBlock.appendChild(infoCopyBtn)
    }
    infoBlockContent.appendChild(createElementWithClass('h1', null, header))
    infoBlockContent.appendChild(createElementWithClass('p', null, message, true))
    infoBlock.classList.add(cls)
    infoBlock.appendChild(infoBlockContent)
    infoBlock.appendChild(infoCloseBlock)
    return infoBlock
}

function removeInfoBlock(){
    let infoChild = document.querySelector('.notification')
    if (infoChild !== null) {
        document.querySelector('.container .smiles-form').removeChild(infoChild)
    }
}


taskIdBtn.addEventListener('click', async function(event){
    event.preventDefault()
    if (document.querySelector('.get-results .results-status')){
        removeTaskStatus()
    }
    if (document.querySelector('.get-results .results')){
        removeResults()
    }
    const taskId = taskIdInput.value
    const targetUrl = apiUrl + 'runs/'+ taskId
    try {
        let response = await fetch(targetUrl)
        let taskJson = await response.json()
        var taskStatus = await taskJson.status
        var taskResults = await taskJson.results
        var taskConstant = await taskJson.Constant
    } catch(e) {
        var taskStatus = 'Failed'
    }
    if (taskStatus === 'Succeeded'){
        var tstatus = 'Completed'
        var divClass = 'success'
    } else {
        var tstatus = 'Failed'
        var divClass = 'danger'
    }
    let getResultsSection = document.querySelector('section.get-results')
    getResultsSection.appendChild(generateStatusBlock(taskId, tstatus, divClass))
    if (taskStatus === 'Succeeded') {
        let resultsTable = generateResultsTable(taskResults, taskConstant)
        getResultsSection.appendChild(resultsTable)
    }
})

function generateStatusBlock(taskId, taskStatus, divClass){
    let resultsStatus = createElementWithClass('div', 'results-status')
    resultsStatus.classList.add(divClass)
    let message = createElementWithClass('div', 'message')
    message.appendChild(createElementWithClass('h2', null, `Your task ${taskId} status ${taskStatus}`))
    resultsStatus.appendChild(message)
    return resultsStatus
}

function generateResultsTable(data, constant){
    const results = createElementWithClass('div', 'results')
    results.appendChild(createElementWithClass('h2', null, 'Results'))
    const table = createElementWithClass('table')
    const tableHead = createElementWithClass('thead')
    const tableHeadRow = createElementWithClass('tr')
    const tableBody = createElementWithClass('tbody', )
    tableHeadRow.appendChild(createElementWithClass('th', null, 'SMILES'))
    tableHeadRow.appendChild(createElementWithClass('th', null, `Predicted ${constant}`))
    tableHead.appendChild(tableHeadRow)
    for (const [key, value] of Object.entries(data)) {
        let tableRow = createElementWithClass('tr')
        tableRow.appendChild(createElementWithClass('td', null, key))
        tableRow.appendChild(createElementWithClass('td', null, value))
        tableBody.appendChild(tableRow)
      }
    table.appendChild(tableHead)
    table.appendChild(tableBody)
    results.appendChild(table)
    return results
}

function copyId(taskId){
    if (window.isSecureContext && navigator.clipboard) {
        navigator.clipboard.writeText(content);
        alert("Copied the text: " + taskId)
      } else {
        alert(`Unable to copy ${taskId}`)
      }
}

function removeTaskStatus (){
    let getResultsSection = document.querySelector('.get-results')
    getResultsSection.removeChild(document.querySelector('.get-results .results-status'))
}

function removeResults (){
    let getResultsSection = document.querySelector('.get-results')
    getResultsSection.removeChild(document.querySelector('.get-results .results'))
}



