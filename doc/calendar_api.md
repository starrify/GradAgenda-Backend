- Author: Ji Yang
- Contact: yangji9181[AT]gmail.com
- Changelog: 
    - 2014.07.20 Initial version.
    - 2014.08.01 Edited by Ji Yang
 
####一,URL说明
url相对路径  | HTTP variable | 功能 
----------     | ----------| -------- 
/addevent/     |    POST   |   新增事件
/geteventlist/ |    POST   |   获取自己的事件
/getevent/     |    POST   |   获取单个事件
/alterevent/   |    POST   |   修改事件
/deleteevent/  |    POST   |   删除事件

####二，数据格式

(1)新增事件：/addevent/

请求数据格式：
	
	{
	    token: string,		//登录时获得, required
	    name:  string,		//事件名称（可含描述）, optional, default 'Unknown'
	    startdatetime:  string,		//起始时间，required，格式为'2014-08-01T00:00:00Z'这样的标准形式
	    location:   string,	//地点, optional, defualt 'Unknown'
	    status: integer		//级别, optional, default 0
	}

返回数据格式：

	JSON:
	{
		status: string,
		message  : string,
	}
	
(2)获取自己的事件：/geteventlist/

请求数据格式：

	{
		token: 	string,		//required
		left:	string,		//起始时间下界，optional，格式为'2014-08-01T00:00:00Z'这样的标准形式
		right:	string,		//起始事件上届，optional，格式同上
	}

返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:		{
					id:		integer,	//事件id，访问/修改/删除/特定事件时需要
					user:	interger,	
					name:   string,		
					startdatetime:   string	,	
					location:	string,	
					status:		integer
					}
	}
(3)获取单个事件：/getevent/ 

请求数据格式：

	{
		token:	string,		//登录时获得, required
		id:		integer		//通过getevent获得, required		
	}

返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:		{
					id:		integer,
					user:	interger,	
					name:   string,		
					startdatetime:   string	,	
					location:	string,	
					status:		integer
					}
	}

(4)修改事件：/alterevent/ 

请求数据格式：

	{
		token:	string		//登录时获得, required
		id:		integer		//通过getevent获得, required		name:   string,		//optional, 默认Unknown
		startdatetime:   string	,	//required
		location:	string,		//optional, 默认Unknown
		status:		integer		//optional, 默认Unknown
	}
	
返回数据格式：

	JSON:
	{
		status: string,
		message  : string,
	}

(5)删除事件：/deletevent/

请求数据格式：

	{
		token:          string,		//登录时获得, required
		id:		integer		//required
	}
	
返回数据格式：

	JSON:
	{
		status: string,
		message  : string,
	}

####三，返回数据说明
#####1，status 字段
status code| 功能
---------- | ------------- 
"success" |    请求成功 
"fail"    |    请求失败（客户端提交数据错误等）    
"error"   |    服务器错误（数据库不一致等异常情况）

#####2，message 字段
用于请求发生错误时返回错误信息

#####3，data
部分请求中用于返回客户端所需的数据。

####四，解释说明
- 用户只能访问自己的事件，否则会引发'permission denied'错误
- 所有optional字段不传入会设定默认值，所有required字段不传入会引发'XXX data format error'错误