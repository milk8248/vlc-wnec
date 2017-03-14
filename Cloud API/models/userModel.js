//引入mongoose
var mongoose = require('mongoose');

//定义数据库模式
var Schema = mongoose.Schema;
//创建用户模型
var userModel = new Schema({
	id: Number,
	image_name: String,
	rx_rotation: [[Number]],
	rx_location: [Number],
	location_error: Number,
	user: String,
	phone_ip: String,
	origin_location : [Number]

});

module.exports = mongoose.model("User", userModel);