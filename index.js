const express = require('express')

const app = express();
var body = "";

app.use(express.json({
    limit: "1mb",
}));
app.listen(3000, () => console.log("listening at 3000"));

app.post('/data', async function(request, response){
    body = request.body
    app.get('/', function (req, res) {
        res.send(body)
        res.redirect("/")
    })
    console.log(body)
    response.send('Received')
})

app.post('/ip', async function(request, response){
    body = request.body
    app.get("/ips", function(req,res) {
        res.send(body)
        res.redirect("/ips")
    })
    console.log(body)
    response.send('Recieved')
})