const express = require('express')
const path = require('path');

const app = express()
const port = 3000

app.use(express.static('static'))

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/index.html'));
})

app.listen(port, '0.0.0.0', () => {
  console.log(`Example app listening on port ${port}`)
})