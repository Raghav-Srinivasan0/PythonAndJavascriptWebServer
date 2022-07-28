const express = require('express')

const app = express();

app.use(express.json({
    limit: "1mb",
}));
app.listen(3000, () => console.log("listening at 3000"));

app.post('/data', async function(request, response){
    const body = request.body
    app.get('/', function(request, response){
        response.send(body)
    })
    response.send('Received')
})