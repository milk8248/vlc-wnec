//引入用户模型
var User = require('./../models/userModel');

var output = function(status, data, info){
	return JSON.stringify({status: status, data: data, info: info})
}

var userController = {
	handleGetNewestUser: function(req, res){
		User.find().sort({_id:-1}).limit(1).exec(function(err, users){
			if(err){
				res.send(output(false, null, 'Fail'));
			}else{
				res.send(output(true, users, 'Success'));
			}
		});
	},
	handleGetUserList: function(req, res){
		User.find(function(err, users){
			if(err){
				res.send(output(false, null, 'Fail'));
			}else{
				res.send(output(true, users, 'Success'));
			}
		});
	},
	handleGetUser: function(req, res){
		if(req.params && req.params.id){
			if(req.params.id == 'all'){
				User.find(function(err, users){
					if(err){
						res.send(output(false, null, 'Fail'));
					}else{
						res.send(output(true, users, 'Success'));
					}
				});
			}else{
				User.findById(req.params.id, function(err, user){
					if(err || !user){
						res.send(output(false, null, 'No Data'));
					}else{
						res.send(output(true, user, 'Request Success'));
					}
				});	
			}	
		}else{
			res.send(output(false, null, 'Request Error'));
		}
	},
	handleAddUser: function(req, res){
		var user = new User(req.body);
		user.save(function(err){
			if(err){
				res.send(output(false, null, 'Input Fail'));
			}else{
				User.find(function(err, users){
					if(err){
						res.send(output(false, user, 'Input Success'));
					}else{
						res.send(output(true, users, 'Input Success'));
					}
				});
			}
		});
	},
	handleUpdateUser: function(req, res){
		if(req.method === 'PUT'){
			if(req.body && req.body._id){
				User.findById(req.body._id, function(err, user){
					if(err || !user){
						res.send(output(false, null, 'No Data'));
					}else{
						user.id = req.body.id;
						user.name = req.body.name;
						user.age = req.body.age;
						user.gender = req.body.gender;
						user.job = req.body.job;

						user.save(function(err){
							if(err){
								res.send(output(false, null, 'Update Fail'));
							}else{
								res.send(output(true, user, 'Update Success'));
							}
						})
					}
				});
			}else{
				res.send(output(false, null, 'Request Error'));
			}
		}else{
			res.send(output(false, null, 'Request Error'));
		}
	},
	handleDelUser: function(req, res){
		if(req.method === 'DELETE'){
			if(req.body && req.body._id){
				User.findById(req.body._id, function(err, user){
					if(err || !user){
						res.send(output(false, null, 'No Data'));
					}else{
						user.remove(function(err){
							if(err){
								res.send(output(false, null, 'Delete Fail'));
							}else{
								User.find(function(err, users){
									if(err){
										res.send(output(false, null, 'Delete Success'));
									}else{
										res.send(output(true, users, 'Delete Success'));
									}
								});
							}
						})
					}
				});
			}else{
				res.send(output(false, null, 'Request Error'));
			}
		}
	}
};

module.exports = userController;