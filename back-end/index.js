const express = require('express')
const app = express()

app.get("/",(req, res)=>{
    res.json({"user": ["userOne","userTwo", "userThree"]})
})


app.listen(5000, ()=>{console.log("server started on port 5000")})

