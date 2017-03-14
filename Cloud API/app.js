//引入express
var express = require('express');

//分离路由后引入路由配置文件
var userRouter = require('./routes/userRouter');

var bodyParser = require('body-parser');

//引入mongoose
var mongoose = require('mongoose');

//连接MongoDB服务器
var db = mongoose.connect("mongodb://localhost/vlc_demo");

//初始化express
var app = express();

//配置服务器监听
app.listen(3000, function(){
	console.log('MongoDB API server is running on port 3000')
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

//配置路由
//回调函数中，req表示请求，res表示响应
app.get('/', function(req, res){
	//请求req的一些常用信息
	console.log(req.headers);
	console.log(req.url);
	console.log(req.method);
	console.log(req.params);
	console.log(req.query);
	//发送响应信息
	res.send("Message");
});

//使用路由
app.use('/user', userRouter);