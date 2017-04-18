//引入express
var express = require('express');

//分离路由处理控制器后引入路由控制器
var userController = require('./../controllers/userController');

//新建“用户”路由
var userRouter = express.Router();

//给路由定义请求方法和逻辑控制器
userRouter.route('')
	.get(userController.handleGetNewestUser)
	.post(userController.handleAddUser)
	.put(userController.handleUpdateUser)
	.delete(userController.handleDelUser);

userRouter.route('/:id')
	.get(userController.handleGetUser);

//导出路由定义
module.exports = userRouter;