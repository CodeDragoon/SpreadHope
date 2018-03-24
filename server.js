const express = require('express')
const app = express()
const bodyParser = require('body-parser');
var PythonShell = require('python-shell');
 
app.set('view engine', 'ejs')
app.use(express.static('public'));



app.use(bodyParser.urlencoded({ extended: true }));


app.get('/', function (req, res) {
    res.render('index');
})
app.get('/index', function (req, res) {
    res.render('index');
})

app.get('/about',function(req,res){
	res.render('about')
})

app.get('/campaigns',function(req,res){
	res.render('campaigns')
})
app.get('/getinvolved',function(req,res){
		res.render('getinvolved')
})

// app.get('/result',function(req,res){
// 	res.render('result')
// })





app.post('/tada',function(req,res){

   name=req.body.fname
   console.log('-----------------------'+name)
	 var options = {
	 	scriptPath: '',
    args: [name],
  }
	 console.log('om namah shivaay')
	 // res.render('stats')

 PythonShell.run('code_fest.py', options, function (err, data) {
    if (err) res.send(err);
    res.render('stats')
    console.log('finished')
  });



})

app.listen(3000, function () {

  console.log('Example app listening on port 3000!')
})




app.post('/', function (req, res) {
  res.render('index');
  console.log('om namah shivaay don');


})







// var PythonShell = require('python-shell');
// var pyshell = new PythonShell('my_script.py');
 
// // sends a message to the Python script via stdin
// pyshell.send('hello');
 
// pyshell.on('message', function (message) {
//   // received a message sent from the Python script (a simple "print" statement)
//   console.log(message);
// });
 
// // end the input stream and allow the process to exit
// pyshell.end(function (err,code,signal) {
//   if (err) throw err;
//   console.log('The exit code was: ' + code);
//   console.log('The exit signal was: ' + signal);
//   console.log('finished');
//   console.log('finished');
// });