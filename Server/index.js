const express = require('express')

const app = express();

app.use(express.static('html'));
app.use(express.json({
    limit: "1mb",
}));
app.listen(3000, () => console.log("listening at 3000"));

app.post('/', function(request, result){
    console.log(request.body)
    result.send('Received')
})